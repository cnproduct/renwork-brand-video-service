#!/usr/bin/env node
// ============================================================
// 品牌影片生成器 v2（心同书院 × 心同共生）
// 逐帧关键帧动画 + 封面 + 旁白配音(TTS) + 字幕 + 多样转场 + BGM
// 输出：out/videos/brand-film/  （竖版 + 横版 + 封面海报）
// ============================================================
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync, spawnSync } from 'node:child_process';
import { synthesizeTts, ttsFileExtension } from '../lib/tts.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FILM_PY = path.join(HERE, '..', 'lib', 'film_scene.py');
const OUT_DIR = path.join(HERE, '..', '..', 'out', 'videos', 'brand-film');

const FPS = 30;
const TRANSITION_DUR = 0.6;
const TRANSITIONS = ['fade', 'slideleft', 'slideup', 'wipeleft', 'circleopen', 'smoothleft'];

const PALETTE = {
  redTop: '#A0261C', redBottom: '#35100C',
  deepTop: '#6E1A14', deepBottom: '#1E0A08',
  gold: '#E0B060',
};

// 场景：封面 + 6 内容场景（narration 为旁白=字幕）
const SCENES = [
  { is_cover: true, dur: 3.0, bg: [PALETTE.redTop, PALETTE.redBottom], kicker: '心同书院 × 心同共生', headline: '心同共生', headline2: '定慧一体 · 隔离而协同', narration: '', subtitle: '' },
  { dur: 0, bg: [PALETTE.deepTop, PALETTE.deepBottom], kicker: '双轮文明工程', headline: '定慧一体', headline2: '隔离而协同', narration: '很多人以为，书院和公司，一个做公益，一个做生意，不过是松散的搭档。其实，心同书院与心同共生，是一套跨越百年的双轮文明工程。' },
  { dur: 0, bg: [PALETTE.redTop, PALETTE.redBottom], kicker: '使命', headline: '启世人公心', headline2: '化世界大同', narration: '书院守护纯粹的公心教育与文化信任场，共生则建立可持续的商业造血能力。一个让人安住本心，一个让人生起妙用，定慧一体，缺一不可。' },
  { dur: 0, bg: [PALETTE.deepTop, PALETTE.deepBottom], kicker: '双主体', headline: '书院守公心', headline2: '共生造妙用', narration: '它们共同服务于同一个使命：启世人公心，化世界大同。书院守公益、守公信，共生连资源、做产品、反哺公益。法律独立，财务隔离，治理协同，公开透明。' },
  { dur: 0, bg: [PALETTE.redTop, PALETTE.redBottom], kicker: '十年愿景', headline: '3000 书院', headline2: '10000 讲师 · 10000 场/年', narration: '沿着明白、做到、利他、共生四步路径，一步也不能跳。十年之后，建成三千所纯公益书院，培养一万名公益讲师，每年一万场公益分享。' },
  { dur: 0, bg: [PALETTE.deepTop, PALETTE.deepBottom], kicker: '协同元年', headline: '2026.9.28', headline2: '首届一日文化节 · 祭孔大典', narration: '二零二六年九月二十八日，首届一日文化节暨祭孔大典，正式开启协同元年。第一年做样板，第三年建网络，第五年成平台，第十年立生态。' },
  { dur: 0, bg: [PALETTE.redTop, PALETTE.redBottom], kicker: '心同共生', headline: '各自独立', headline2: '彼此成就', narration: '最好的协同，不是互相依赖，而是各自独立、彼此成就。书院让经济有了文化之根与公心方向，共生让公益理想有了资源、工具与长久的生命力。' },
];

const ffmpeg = (args) => execFileSync('ffmpeg', args, { stdio: 'pipe' });

const probeDur = (f) => Number(execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], { encoding: 'utf8' }).trim());

// 生成一个场景的动画帧序列
function renderFrames(scene, W, H, outDir, singleP = null) {
  const spec = {
    ...scene, out_dir: outDir, w: W, h: H, fps: FPS, dur: scene.dur,
    accent: PALETTE.gold, footer: '心同共生', subtitle: scene.narration,
  };
  if (singleP !== null) { spec.single_p = singleP; spec.fps = 1; spec.dur = 1; }
  const r = spawnSync('python3', [FILM_PY], { input: JSON.stringify(spec), encoding: 'utf8' });
  if (r.status !== 0) throw new Error(r.stderr || 'frame render failed');
}

function framesToClip(frameDir, clipPath) {
  ffmpeg(['-y', '-framerate', String(FPS), '-i', path.join(frameDir, 'f%04d.png'),
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-an', clipPath]);
}

// xfade 拼接（多样转场）
function xfadeConcat(clips, durations, outPath) {
  const n = clips.length;
  const inputs = clips.flatMap((c) => ['-i', c]);
  const chains = [];
  let prev = '[0:v]';
  let cum = 0;
  for (let i = 0; i < n - 1; i++) {
    cum += durations[i];
    const offset = cum - (i + 1) * TRANSITION_DUR;
    const trans = TRANSITIONS[i % TRANSITIONS.length];
    const outLabel = i === n - 2 ? '[vout]' : `[v${i}]`;
    chains.push(`${prev}[${i + 1}:v]xfade=transition=${trans}:duration=${TRANSITION_DUR}:offset=${offset.toFixed(3)}${outLabel}`);
    prev = outLabel;
  }
  ffmpeg(['-y', ...inputs, '-filter_complex', chains.join(';'),
    '-map', '[vout]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', String(FPS),
    '-movflags', '+faststart', '-an', outPath]);
}

// 生成 BGM（暖色五声调式铺底）
function genBgm(outWav, durSec) {
  const F = [110, 164.81, 220, 329.63];
  const inputs = F.map((f) => ['-f', 'lavfi', '-i', `sine=frequency=${f}:duration=${durSec + 4}`]).flat();
  const fc = `[0:a][1:a][2:a][3:a]amix=inputs=4:normalize=0,lowpass=f=900,` +
    `aecho=0.8:0.5:180:0.25,aecho=0.7:0.4:360:0.15,` +
    `afade=t=in:st=0:d=2.5,afade=t=out:st=${durSec - 1}:d=3,volume=0.55`;
  ffmpeg(['-y', ...inputs, '-filter_complex', fc, '-c:a', 'pcm_s16le', outWav]);
}

// 静音片段
function silence(outWav, dur) {
  ffmpeg(['-y', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', dur.toFixed(2), '-c:a', 'pcm_s16le', outWav]);
}

// 构建完整旁白轨（封面静音 + 各场景旁白按场景时长对齐）
function buildNarration(scenes, durations, outWav, tmp) {
  const parts = [];
  scenes.forEach((sc, i) => {
    const dur = durations[i];
    const part = path.join(tmp, `nar-${i}.wav`);
    if (sc.is_cover || !sc.narration) {
      silence(part, dur);
    } else {
      const raw = path.join(tmp, `tts-${i}.${ttsFileExtension()}`);
      synthesizeTts(sc.narration, raw);
      ffmpeg(['-y', '-i', raw, '-ar', '44100', '-ac', '1', '-af', 'apad', '-t', dur.toFixed(2), '-c:a', 'pcm_s16le', part]);
    }
    parts.push(part);
  });
  const list = path.join(tmp, 'nar-list.txt');
  fs.writeFileSync(list, parts.map((p) => `file '${p}'`).join('\n'), 'utf8');
  ffmpeg(['-y', '-f', 'concat', '-safe', '0', '-i', list, '-ar', '44100', '-ac', '1', '-c:a', 'pcm_s16le', outWav]);
}

function build({ W, H, label }) {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const tmp = fs.mkdtempSync(path.join(OUT_DIR, '.tmp-'));

  try {
    // 1) 旁白时长 → 场景时长
    const ttsDurs = SCENES.map((sc) => {
      if (sc.is_cover || !sc.narration) return 0;
      const raw = path.join(tmp, `probe.${ttsFileExtension()}`);
      synthesizeTts(sc.narration, raw);
      const d = probeDur(raw);
      fs.rmSync(raw, { force: true });
      return d;
    });
    const durations = SCENES.map((sc, i) => (sc.is_cover ? sc.dur : Math.max(3.5, ttsDurs[i] + 0.9)));
    const totalDur = durations.reduce((a, b) => a + b, 0);

    // 2) 逐场景渲染动画帧 → 片段
    console.log(`🎞️  ${label} 渲染 ${SCENES.length} 个场景...`);
    const clips = [];
    SCENES.forEach((sc, i) => {
      const frameDir = path.join(tmp, `fr-${i}`);
      renderFrames({ ...sc, dur: durations[i] }, W, H, frameDir);
      const clip = path.join(tmp, `c-${i}.mp4`);
      framesToClip(frameDir, clip);
      clips.push(clip);
      console.log(`   ✅ 场景 ${i + 1}/${SCENES.length} [${durations[i].toFixed(1)}s] ${sc.headline}`);
    });

    // 3) 多样转场拼接视频
    console.log('🎬 转场拼接...');
    const video = path.join(tmp, 'video.mp4');
    xfadeConcat(clips, durations, video);

    // 4) 旁白轨 + BGM
    console.log('🎙️  旁白配音 + BGM...');
    const nar = path.join(tmp, 'narration.wav');
    buildNarration(SCENES, durations, nar, tmp);
    const bgm = path.join(tmp, 'bgm.wav');
    genBgm(bgm, totalDur);

    // 5) 混合并封装（旁白为主，BGM 压低垫底）
    const outPath = path.join(OUT_DIR, `心同共生-品牌片-${label}.mp4`);
    ffmpeg(['-y', '-i', video, '-i', nar, '-i', bgm,
      '-filter_complex', '[2:a]volume=0.16[bg];[1:a][bg]amix=inputs=2:duration=first:normalize=0[a]',
      '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k',
      '-movflags', '+faststart', '-shortest', outPath]);
    console.log(`   ✅ ${path.basename(outPath)} (${probeDur(outPath).toFixed(1)}s)`);
    return outPath;
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

function coverPoster() {
  // 封面海报：取封面场景 p=1.0 的单帧高清图
  const tmp = fs.mkdtempSync(path.join(OUT_DIR, '.poster-'));
  try {
    renderFrames({ ...SCENES[0], dur: 3 }, 1080, 1920, tmp, 1.0);
    const png = path.join(tmp, 'f0000.png');
    const jpg = path.join(OUT_DIR, '心同共生-封面海报.jpg');
    execFileSync('ffmpeg', ['-y', '-i', png, '-q:v', '2', jpg], { stdio: 'pipe' });
    console.log(`   ✅ 封面海报 -> ${path.basename(jpg)}`);
    return jpg;
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

function run() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  console.log('🚀 生成品牌影片 v2（动画+配音+字幕+转场+BGM）\n');
  build({ W: 1080, H: 1920, label: '竖版' });
  console.log();
  build({ W: 1920, H: 1080, label: '横版' });
  console.log();
  coverPoster();
  console.log(`\n🎉 全部完成 -> ${OUT_DIR}`);
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) run();
