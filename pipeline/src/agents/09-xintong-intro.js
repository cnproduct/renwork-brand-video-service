#!/usr/bin/env node
// 心同共生介绍片：真实场景图 + 连贯旁白 + 字幕卡 + BGM + Ken Burns 动态
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync, spawnSync } from 'node:child_process';
import { synthesizeTts, ttsFileExtension } from '../lib/tts.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(HERE, '..', '..');
const CARD_PY = path.join(ROOT, 'src', 'lib', 'image_scene_card.py');
const IMAGE_DIR = path.join(ROOT, 'assets', 'xintong-scenes');
const OUT_DIR = path.join(ROOT, 'out', 'videos', 'xintong-intro');
const FPS = 30;
const OUTPUT_BASENAME = process.env.XINTONG_OUTPUT_NAME || '心同共生-真实场景介绍片-横版.mp4';

const images = (name) => path.join(IMAGE_DIR, name);

// 叙事顺序：讲师成长 → 共生简介 → 双主体协同。
// 微信图按上传顺序作为书院/活动照片使用；编号图按文件名语义使用。
const SCENES = [
  { image: images('01-brand-system.jpg'), kicker: '心同书院 × 心同共生', title: '此心相同，世界大同', subtitle: '讲师成长体系 · 共生简介 · 协同发展', narration: '心同书院，心同共生。此心相同，世界大同。' },
  { image: images('02-lecturer.jpg'), kicker: '一 · 讲师成长体系', title: '从分享员到城市导师', subtitle: '四级成长路径', narration: '先看心同书院的讲师成长体系。分享员、助教、公益讲师、城市导师，四级成长，走的是一条从参与服务到承担责任的进阶之路。' },
  { image: images('03-academy-event.jpg'), kicker: '一 · 讲师成长体系', title: '身份不是荣誉等级', subtitle: '服务能力与责任范围', narration: '在这里，晋级不以收费为条件，也不是购买一个身份。真实的服务记录、课程能力、实践表现和伙伴反馈，才是成长与认证的依据。' },
  { image: images('04-confucius-talk.png'), kicker: '一 · 讲师成长体系', title: '学习，最终要回到服务', subtitle: '年度复审 · 试讲 · 复训 · 申诉与撤任', narration: '讲师体系不是一次认证、终身有效，而是持续学习、年度复训和定期复审。身份越往上，意味着更大的服务能力，也意味着更重的责任。' },
  { image: images('12-office-materials.jpg'), kicker: '二 · 心同共生简介', title: '以文化启心，以共创促共生', subtitle: '同心 · 利他 · 包容 · 共创 · 笃行', narration: '心同共生，是心同双主体体系中的商业实践与科技、产业赋能主体。它以文化启心，以共创促共生，把公心价值带入真实的组织与社会行动。' },
  { image: images('09-wayfinding.jpg'), kicker: '二 · 心同共生简介', title: '道生万物', subtitle: '同，不是相同；是相通', narration: '它的标识讲述道生万物：开放的半圆，是本源、整体与共同世界；平等相遇的两个人，代表和而不同；暖金光芒，则代表相遇之后生成的智慧、希望与行动。' },
  { image: images('08-apparel-gifts.jpg'), kicker: '二 · 心同共生简介', title: '四条经营主线', subtitle: '文创 · 企业 · 城市 · 数字', narration: '心同共生沿着四条经营主线向外生长：文创与生活美学，企业文化与组织共创，文化活动与城市项目，以及数字内容与人工智能系统。' },
  { image: images('10-course-packaging.jpg'), kicker: '二 · 心同共生简介', title: '让文化成为可传播的资产', subtitle: '课程、礼赠、空间、内容', narration: '这些业务不是脱离文化的商业包装，而是把课程、礼赠、空间、活动和内容做成可信、可传播、可持续交付的共创产品。' },
  { image: images('05-academy-building.jpg'), kicker: '三 · 协同发展', title: '不是公益项目加一家公司', subtitle: '而是一套双轮文明工程', narration: '心同书院与心同共生，不是公益项目加一家公司，而是一套跨百年的双轮文明工程：书院守护公心教育与文化信任，共生建立商业造血与社会创新能力。' },
  { image: images('06-community.jpg'), kicker: '三 · 协同发展', title: '定慧一体，隔离而协同', subtitle: '法律独立 · 财务隔离 · 治理协同', narration: '两者使命相通，却必须法律独立、财务隔离、治理协同、公开透明。书院守公心，共生造妙用；彼此连接，但绝不混同。' },
  { image: images('07-event-site.jpg'), kicker: '三 · 协同发展', title: '六大工程，共同向外生长', subtitle: '文化内容 · 公益人才 · 城市书院 · 文化节 · 企业向善 · 数字文明', narration: '六大工程把分工变成协同：书院把关文化与公益，共生提供项目、产品和数字工具，最终共同形成可信、可传播、可持续的文化资产。' },
  { image: images('11-digital-media.jpg'), kicker: '三 · 协同发展', title: '从协同元年走向长期生态', subtitle: '2026.9.28 · 首届一日文化节暨祭孔大典', narration: '二零二六年九月二十八日，首届一日文化节暨祭孔大典开启协同元年。第一年做样板，第三年建网络，第五年成平台，第十年立生态。' },
  { image: images('01-brand-system.jpg'), kicker: '心同共生', title: '各自独立，彼此成就', subtitle: '让公益有根，让经济有方向', narration: '这就是心同书院与心同共生的关系：一个让公益有根，一个让经济有方向；各自独立，彼此成就，共赴大同。' },
];

const run = (command, args) => execFileSync(command, args, { stdio: 'pipe' });
const duration = (file) => Number(run('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', file]).toString().trim());

function renderCard(scene, cardPath) {
  const result = spawnSync('python3', [CARD_PY], {
    input: JSON.stringify({ ...scene, output: cardPath, width: 1920, height: 1080, gold: '#E0B060', red: '#A0261C' }),
    encoding: 'utf8',
  });
  if (result.status !== 0) throw new Error(result.stderr || 'image card render failed');
}

function makeMotionClip(card, output, seconds, index) {
  // 不同场景使用不同的推拉方向；画面仍保持真实照片，不做生成式改造。
  const direction = index % 2 === 0 ? 'in' : 'out';
  const zoom = direction === 'in'
    ? "min(zoom+0.00055,1.08)"
    : "if(eq(on,1),1.08,max(zoom-0.00055,1.0))";
  const vf = [
    `zoompan=z='${zoom}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=${FPS}`,
    `fade=t=in:st=0:d=0.35`,
    `fade=t=out:st=${Math.max(0.4, seconds - 0.35).toFixed(2)}:d=0.35`,
    'format=yuv420p',
  ].join(',');
  run('ffmpeg', ['-y', '-loop', '1', '-i', card, '-t', seconds.toFixed(2), '-vf', vf, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-an', output]);
}

function makeAudio(sceneDurations, tmp) {
  const parts = [];
  SCENES.forEach((scene, index) => {
    const out = path.join(tmp, `narration-${index}.wav`);
    const seconds = sceneDurations[index];
    if (scene.narration) {
      const rawPath = path.join(tmp, `tts-${index}.${ttsFileExtension()}`);
      synthesizeTts(scene.narration, rawPath);
      run('ffmpeg', ['-y', '-i', rawPath, '-ar', '44100', '-ac', '1', '-af', 'apad', '-t', seconds.toFixed(2), '-c:a', 'pcm_s16le', out]);
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
    console.log(`🎬 心同共生真实场景介绍片：${SCENES.length} 个场景 / 1920x1080`);
    const sceneDurations = [];
    const clips = [];
    SCENES.forEach((scene, index) => {
      const raw = path.join(tmp, `tts-probe-${index}.${ttsFileExtension()}`);
      if (scene.narration) {
        synthesizeTts(scene.narration, raw);
        sceneDurations[index] = Math.max(5.5, duration(raw) + 0.9);
      } else sceneDurations[index] = 5.0;
      const card = path.join(tmp, `card-${index}.png`);
      const clip = path.join(tmp, `clip-${index}.mp4`);
      renderCard(scene, card);
      makeMotionClip(card, clip, sceneDurations[index], index);
      clips.push(clip);
      console.log(`  ✅ ${String(index + 1).padStart(2, '0')}/${SCENES.length} ${scene.title} [${sceneDurations[index].toFixed(1)}s]`);
    });

    const list = path.join(tmp, 'video-list.txt');
    fs.writeFileSync(list, clips.map((p) => `file '${p}'`).join('\n'));
    const video = path.join(tmp, 'video.mp4');
    run('ffmpeg', ['-y', '-f', 'concat', '-safe', '0', '-i', list, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', '-an', video]);

    const audio = makeAudio(sceneDurations, tmp);
    const output = path.join(OUT_DIR, OUTPUT_BASENAME);
    run('ffmpeg', ['-y', '-i', video, '-i', audio.narration, '-i', audio.bgm,
      '-filter_complex', '[2:a]volume=0.16[bg];[1:a][bg]amix=inputs=2:duration=first:normalize=0[a]',
      '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', '-shortest', output]);

    fs.writeFileSync(path.join(OUT_DIR, 'scene-map.json'), JSON.stringify({
      format: '16:9', width: 1920, height: 1080, scenes: SCENES.map((s, i) => ({ scene: i + 1, image: s.image, title: s.title, duration_sec: sceneDurations[i] })),
      total_duration_sec: sceneDurations.reduce((a, b) => a + b, 0),
    }, null, 2));
    console.log(`\n✅ 成片：${output}`);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) main();
