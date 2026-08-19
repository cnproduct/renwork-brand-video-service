#!/usr/bin/env node
// 给真实场景介绍片添加可见封面，避免视频发送后第一帧是黑场。
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync, spawnSync } from 'node:child_process';
import { synthesizeTts, ttsFileExtension } from '../lib/tts.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(HERE, '..', '..');
const CARD_PY = path.join(ROOT, 'src', 'lib', 'image_scene_card.py');
const OUT_DIR = path.join(ROOT, 'out', 'videos', 'xintong-intro');
const SOURCE = path.join(OUT_DIR, '心同共生-真实场景介绍片-横版-云扬配音.mp4');
const OUTPUT = path.join(OUT_DIR, '心同共生-真实场景介绍片-横版-云扬配音-带封面.mp4');
const COVER_SECONDS = 4;

const run = (command, args) => execFileSync(command, args, { stdio: 'pipe' });

function renderCoverCard(output) {
  const image = path.join(ROOT, 'assets', 'xintong-scenes', '01-brand-system.jpg');
  const spec = {
    image,
    output,
    width: 1920,
    height: 1080,
    kicker: '心同书院 × 心同共生',
    title: '此心相同，世界大同',
    subtitle: '讲师成长体系 · 共生简介 · 协同发展',
    narration: '',
    gold: '#E0B060',
    red: '#A0261C',
    footer: '心同共生  ·  ONE HEART · GROWING TOGETHER',
  };
  const result = spawnSync('python3', [CARD_PY], { input: JSON.stringify(spec), encoding: 'utf8' });
  if (result.status !== 0) throw new Error(result.stderr || 'cover card render failed');
}

function main() {
  if (!fs.existsSync(SOURCE)) throw new Error(`找不到源视频：${SOURCE}`);
  const tmp = fs.mkdtempSync(path.join(OUT_DIR, '.cover-'));
  try {
    const card = path.join(tmp, 'cover.png');
    const rawVoice = path.join(tmp, `cover-voice.${ttsFileExtension()}`);
    const voice = path.join(tmp, 'cover-voice.wav');
    const coverVideo = path.join(tmp, 'cover-video.mp4');
    const coverWithAudio = path.join(tmp, 'cover-with-audio.mp4');
    const intro = '心同书院，心同共生。此心相同，世界大同。';

    renderCoverCard(card);
    synthesizeTts(intro, rawVoice);
    run('ffmpeg', ['-y', '-i', rawVoice, '-ar', '44100', '-ac', '1', '-af', 'apad', '-t', String(COVER_SECONDS), '-c:a', 'pcm_s16le', voice]);
    // 不加 fade，确保第 1 帧就是可见封面。
    run('ffmpeg', ['-y', '-loop', '1', '-i', card, '-t', String(COVER_SECONDS), '-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-an', coverVideo]);
    run('ffmpeg', ['-y', '-i', coverVideo, '-i', voice, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', coverWithAudio]);

    // 用 concat filter 重新编码，重建时间戳，避免播放器打不开或首帧异常。
    run('ffmpeg', [
      '-y', '-i', coverWithAudio, '-i', SOURCE,
      '-filter_complex',
      '[0:v]setpts=PTS-STARTPTS[v0];[1:v]setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0[v];' +
      '[0:a]aresample=44100,asetpts=PTS-STARTPTS[a0];[1:a]aresample=44100,asetpts=PTS-STARTPTS[a1];[a0][a1]concat=n=2:v=0:a=1[a]',
      '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-r', '30', '-pix_fmt', 'yuv420p',
      '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', OUTPUT,
    ]);
    console.log(`✅ 带封面视频已生成：${OUTPUT}`);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

main();
