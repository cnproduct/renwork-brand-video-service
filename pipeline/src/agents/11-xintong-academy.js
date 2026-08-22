#!/usr/bin/env node
// 心同书院介绍片：实拍视频混剪 + 照片场景卡 + Logo 封面 + PPT 内容旁白 + 字幕 + BGM
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync, spawnSync } from 'node:child_process';
import { synthesizeTts, ttsFileExtension } from '../lib/tts.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(HERE, '..', '..');
const CARD_PY = path.join(ROOT, 'src', 'lib', 'image_scene_card.py');
const OVERLAY_PY = path.join(ROOT, 'src', 'lib', 'overlay_text.py');
const ASSET_DIR = path.join(ROOT, 'assets', 'xintong-academy');

// 心同书院品牌色（从 design-tokens.json 提取）
const BRAND = {
  primary: '#9A2626',   // 书院朱红
  ink: '#1A1A1A',       // 墨
  paper: '#FFFBF5',     // 米白纸
  paper_warm: '#F7F0E6', // 宣纸
  gold: '#C9A227',      // 暖金（仅装饰）
  line: '#E8E2D8',      // 分隔线
};
const OUT_DIR = path.join(ROOT, 'out', 'videos', 'xintong-academy');
const FPS = 30;
const W = 1920, H = 1080;

const asset = (name) => path.join(ASSET_DIR, name);

// 12 场景：封面 + 10 内容 + 结尾 CTA
// type: cover=logo+封面图, photo=照片卡, video=实拍视频, cta=结尾
const SCENES = [
  { type: 'cover', image: asset('cover.jpg'), logo: asset('logo.png'), kicker: '心同书院', title: '此心相同，世界大同', subtitle: '纯公益讲学 · 滋润精神家园', narration: '心同书院。此心相同，世界大同。' },
  { type: 'photo', image: asset('photo-1.jpg'), kicker: '时代背景', title: '生逢盛世，感恩祖国', subtitle: '人民有信仰 · 国家有力量', narration: '我们生逢盛世。国家富强，社会和谐，人民有信仰，国家有力量。个人的每一份幸福，都离不开祖国的坚实后盾。' },
  { type: 'video', video: asset('vid-1.mp4'), kicker: '书院缘起', title: '由爱心人士共同发起', subtitle: '热爱中国传统文化', narration: '心同书院，由热爱中国传统文化的爱心人士共同发起。' },
  { type: 'photo', image: asset('photo-2.jpg'), kicker: '公益定位', title: '纯公益讲学', subtitle: '滋润精神家园', narration: '纯公益讲学，滋润精神家园。助力家庭和谐、身心健康、企业发展。' },
  { type: 'video', video: asset('vid-2.mp4'), kicker: '神圣使命', title: '启世人公心，化世界大同', subtitle: '人人有道 · 人人有德', narration: '启世人公心，化世界大同。遵循人人有道，人人有德，互敬互爱，互帮互助，天下为公，世界大同。' },
  { type: 'photo', image: asset('photo-3.jpg'), kicker: '宏伟蓝图', title: '3000 书院 · 10000 讲师 · 10000 场', subtitle: '让国学经典走进千家万户', narration: '宏伟蓝图：三千所纯公益书院，一万名国学讲师，每年一万场公益分享。让国学经典走进千家万户，构建精神家园。' },
  { type: 'photo', image: asset('photo-4.jpg'), kicker: '十大方向', title: '十大教育方向', subtitle: '爱国 · 企业 · 公益 · 自然 · 生命', narration: '十大教育方向：爱国教育、企业文化、社会公益、自然教育、呵护生命、书香家庭、师资培养、传统文化、中医养生、经典研读。' },
  { type: 'photo', image: asset('photo-5.jpg'), kicker: '智慧之根', title: '大学之道，在明明德', subtitle: '博学 · 审问 · 慎思 · 明辨 · 笃行', narration: '大学之道，在明明德，在亲民，在止于至善。博学之，审问之，慎思之，明辨之，笃行之。' },
  { type: 'video', video: asset('vid-3.mp4'), kicker: '仁爱之心', title: '老吾老，以及人之老', subtitle: '视天下为一家', narration: '老吾老，以及人之老；幼吾幼，以及人之幼。视天下为一家，共筑社会和谐。' },
  { type: 'photo', image: asset('photo-6.jpg'), kicker: '立此宏愿', title: '大道之行，天下为公', subtitle: '启世人公心 · 化世界大同', narration: '大道之行，天下为公。誓以启世人公心为己任，以化世界大同为毕生追寻。' },
  { type: 'photo', image: asset('photo-7.jpg'), kicker: '每日践行', title: '睡前祈祷文', subtitle: '此心相同，世界大同', narration: '每日践行，睡前祈祷。此心相同，世界大同。' },
  { type: 'cta', image: asset('cover.jpg'), logo: asset('logo.png'), kicker: '心同书院', title: '欢迎加入，共筑精神家园', subtitle: '此心相同 · 世界大同', narration: '欢迎加入心同书院，共筑精神家园。' },
];

const run = (command, args) => execFileSync(command, args, { stdio: 'pipe' });
const duration = (file) => Number(run('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', file]).toString().trim());

function renderCard(scene, cardPath) {
  const result = spawnSync('python3', [CARD_PY], {
    input: JSON.stringify({ ...scene, output: cardPath, width: W, height: H, gold: BRAND.gold, red: BRAND.primary }),
    encoding: 'utf8',
  });
  if (result.status !== 0) throw new Error(result.stderr || 'card render failed');
}

function renderOverlay(scene, overlayPath) {
  const result = spawnSync('python3', [OVERLAY_PY], {
    input: JSON.stringify({ ...scene, output: overlayPath, width: W, height: H, gold: BRAND.gold, red: BRAND.primary }),
    encoding: 'utf8',
  });
  if (result.status !== 0) throw new Error(result.stderr || 'overlay render failed');
}

// 照片/封面场景：卡片 + Ken Burns（首帧不做淡入，避免黑场）
function makePhotoClip(card, output, seconds, index) {
  const direction = index % 2 === 0 ? 'in' : 'out';
  const zoom = direction === 'in'
    ? "min(zoom+0.00055,1.08)"
    : "if(eq(on,1),1.08,max(zoom-0.00055,1.0))";
  const fadeIn = index === 0 ? '' : 'fade=t=in:st=0:d=0.35,';
  const vf = [
    `zoompan=z='${zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=${W}x${H}:fps=${FPS}`,
    `${fadeIn}fade=t=out:st=${Math.max(0.4, seconds - 0.35).toFixed(2)}:d=0.35`,
    'format=yuv420p',
  ].join(',');
  run('ffmpeg', ['-y', '-loop', '1', '-i', card, '-t', seconds.toFixed(2), '-vf', vf, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-an', output]);
}

// 实拍视频场景：缩放 + 暗化 + 文字叠加 + 淡入淡出
function makeVideoClip(scene, output, seconds) {
  const overlay = path.join(path.dirname(output), 'overlay.png');
  renderOverlay(scene, overlay);
  const vf = [
    `scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2`,
    'eq=brightness=-0.12:saturation=0.95',
    `fade=t=in:st=0:d=0.35`,
    `fade=t=out:st=${Math.max(0.4, seconds - 0.35).toFixed(2)}:d=0.35`,
    'format=yuv420p',
  ].join(',');
  run('ffmpeg', ['-y', '-i', scene.video, '-t', seconds.toFixed(2), '-vf', vf, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-an', path.join(path.dirname(output), 'base.mp4')]);
  // 叠加文字
  run('ffmpeg', ['-y', '-i', path.join(path.dirname(output), 'base.mp4'), '-i', overlay,
    '-filter_complex', '[0:v][1:v]overlay=0:0:format=auto[v]',
    '-map', '[v]', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-an', output]);
}

function makeAudio(sceneDurations, tmp) {
  const parts = [];
  SCENES.forEach((scene, index) => {
    const out = path.join(tmp, `narration-${index}.wav`);
    const seconds = sceneDurations[index];
    if (scene.narration) {
      const raw = path.join(tmp, `tts-${index}.${ttsFileExtension()}`);
      synthesizeTts(scene.narration, raw);
      run('ffmpeg', ['-y', '-i', raw, '-ar', '44100', '-ac', '1', '-af', 'apad', '-t', seconds.toFixed(2), '-c:a', 'pcm_s16le', out]);
    } else {
      run('ffmpeg', ['-y', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', seconds.toFixed(2), '-ar', '44100', '-ac', '1', '-c:a', 'pcm_s16le', out]);
    }
    parts.push(out);
  });
  const list = path.join(tmp, 'audio-list.txt');
  fs.writeFileSync(list, parts.map((p) => `file '${p}'`).join('\n'));
  const narration = path.join(tmp, 'narration.wav');
  run('ffmpeg', ['-y', '-f', 'concat', '-safe', '0', '-i', list, '-ar', '44100', '-ac', '1', '-c:a', 'pcm_s16le', narration]);

  const total = sceneDurations.reduce((a, b) => a + b, 0);
  const bgm = path.join(tmp, 'bgm.wav');
  const freqs = [110, 164.81, 220, 329.63];
  const inputs = freqs.flatMap((f) => ['-f', 'lavfi', '-i', `sine=frequency=${f}:duration=${total + 3}`]);
  run('ffmpeg', ['-y', ...inputs, '-filter_complex',
    `[0:a][1:a][2:a][3:a]amix=inputs=4:normalize=0,lowpass=f=900,aecho=0.8:0.5:180:0.25,afade=t=in:st=0:d=2.5,afade=t=out:st=${Math.max(1, total - 2)}:d=2,volume=0.42`,
    '-ar', '44100', '-ac', '1', '-c:a', 'pcm_s16le', bgm]);
  return { narration, bgm, total };
}

function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  const tmp = fs.mkdtempSync(path.join(OUT_DIR, '.tmp-'));
  try {
    console.log(`🎬 心同书院介绍片：${SCENES.length} 场景 / ${W}x${H}`);
    const sceneDurations = [];
    const clips = [];
    SCENES.forEach((scene, index) => {
      const raw = path.join(tmp, `tts-probe-${index}.${ttsFileExtension()}`);
      if (scene.narration) {
        synthesizeTts(scene.narration, raw);
        sceneDurations[index] = Math.max(5.5, duration(raw) + 0.9);
      } else sceneDurations[index] = 5.0;
      const clip = path.join(tmp, `clip-${index}.mp4`);
      if (scene.type === 'video') {
        makeVideoClip(scene, clip, sceneDurations[index]);
      } else {
        const card = path.join(tmp, `card-${index}.png`);
        renderCard(scene, card);
        makePhotoClip(card, clip, sceneDurations[index], index);
      }
      clips.push(clip);
      console.log(`  ✅ ${String(index + 1).padStart(2, '0')}/${SCENES.length} ${scene.title} [${sceneDurations[index].toFixed(1)}s]`);
    });

    const list = path.join(tmp, 'video-list.txt');
    fs.writeFileSync(list, clips.map((p) => `file '${p}'`).join('\n'));
    const video = path.join(tmp, 'video.mp4');
    run('ffmpeg', ['-y', '-f', 'concat', '-safe', '0', '-i', list, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', '-an', video]);

    const audio = makeAudio(sceneDurations, tmp);
    const output = path.join(OUT_DIR, '心同书院-介绍片-混剪版.mp4');
    run('ffmpeg', ['-y', '-i', video, '-i', audio.narration, '-i', audio.bgm,
      '-filter_complex', '[2:a]volume=0.16[bg];[1:a][bg]amix=inputs=2:duration=first:normalize=0[a]',
      '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', '-shortest', output]);

    fs.writeFileSync(path.join(OUT_DIR, 'scene-map.json'), JSON.stringify({
      format: '16:9', width: W, height: H,
      scenes: SCENES.map((s, i) => ({ scene: i + 1, type: s.type, title: s.title, duration_sec: sceneDurations[i] })),
      total_duration_sec: sceneDurations.reduce((a, b) => a + b, 0),
    }, null, 2));
    console.log(`\n✅ 成片：${output}`);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) main();