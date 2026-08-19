#!/usr/bin/env node
// ============================================================
// 品牌视频打包生成器（心同书院 × 心同共生）
// 一次产出：竖版带音乐 / 横版16:9带音乐 / 6个单场景竖屏 / BGM素材
// 输出目录：out/videos/brand/
// ============================================================
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync, spawnSync } from 'node:child_process';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FRAME_PY = path.join(HERE, '..', 'lib', 'brand_frame.py');
const OUT_DIR = path.join(HERE, '..', '..', 'out', 'videos', 'brand');
const SPLIT_DIR = path.join(OUT_DIR, '单场景竖屏');

const FPS = 30, FADE = 0.4;

// 品牌色板（从上传的品牌视觉图提取）
const PALETTE = {
  redTop: '#A0261C',
  redBottom: '#35100C',
  deepTop: '#6E1A14',
  deepBottom: '#1E0A08',
  gold: '#E0B060',
};

// 场景脚本
const SCENES = [
  { dur: 3.5, slug: '01-定慧一体-隔离而协同', bg: [PALETTE.redTop, PALETTE.redBottom], kicker: '心同书院 × 心同共生', headline: '定慧一体', headline2: '隔离而协同', subtitle: '双轮文明工程 · 十年规划 V1.0' },
  { dur: 4.0, slug: '02-启世人公心-化世界大同', bg: [PALETTE.deepTop, PALETTE.deepBottom], kicker: '使命', headline: '启世人公心', headline2: '化世界大同', subtitle: '明白 → 做到 → 利他 → 共生' },
  { dur: 4.5, slug: '03-书院守公心-共生造妙用', bg: [PALETTE.redTop, PALETTE.redBottom], kicker: '双主体', headline: '书院守公心', headline2: '共生造妙用', subtitle: '公益主体 × 社会企业 · 法律独立 财务隔离 治理协同' },
  { dur: 4.5, slug: '04-十年愿景-3000书院', bg: [PALETTE.deepTop, PALETTE.deepBottom], kicker: '十年愿景', headline: '3000 书院', headline2: '10000 讲师 · 10000 场/年', subtitle: '第一年样板 · 第三年网络 · 第五年平台 · 第十年生态' },
  { dur: 4.0, slug: '05-协同元年-20260928', bg: [PALETTE.redTop, PALETTE.redBottom], kicker: '协同元年', headline: '2026.9.28', headline2: '首届一日文化节 · 祭孔大典', subtitle: '验证 → 标准 → 复制 · 边界白皮书与影响力季报' },
  { dur: 4.5, slug: '06-各自独立-彼此成就', bg: [PALETTE.deepTop, PALETTE.deepBottom], kicker: '心同共生', headline: '各自独立', headline2: '彼此成就', subtitle: '让公益有根 · 让经济有方向' },
];

const ffmpeg = (args) => execFileSync('ffmpeg', args, { stdio: 'pipe' });

function renderFrame(scene, W, H, outPath) {
  const r = spawnSync('python3', [FRAME_PY], {
    input: JSON.stringify({ ...scene, out: outPath, w: W, h: H, accent: PALETTE.gold }),
    encoding: 'utf8',
  });
  if (r.status !== 0) throw new Error(r.stderr || 'render frame failed');
}

function frameToClip(framePath, clipPath, dur) {
  const fadeIn = `fade=t=in:st=0:d=${FADE}`;
  const fadeOut = `fade=t=out:st=${Math.max(0, dur - FADE)}:d=${FADE}`;
  ffmpeg(['-y', '-loop', '1', '-i', framePath, '-t', String(dur), '-r', String(FPS),
    '-vf', `${fadeIn},${fadeOut},format=yuv420p`, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-an', clipPath]);
}

function concat(clips, outPath) {
  const listPath = path.join(OUT_DIR, '.concat.txt');
  fs.writeFileSync(listPath, clips.map((c) => `file '${c}'`).join('\n'), 'utf8');
  ffmpeg(['-y', '-f', 'concat', '-safe', '0', '-i', listPath,
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', String(FPS), '-movflags', '+faststart', '-an', outPath]);
  fs.rmSync(listPath, { force: true });
}

// 合成一段暖色五声调式铺底 BGM（开放五度，静谧）
function genBgm(outWav, durSec = 32) {
  const F = [110, 164.81, 220, 329.63]; // A2 E3 A3 E4
  const inputs = F.map((f) => ['-f', 'lavfi', '-i', `sine=frequency=${f}:duration=${durSec}`]).flat();
  const fc = `[0:a][1:a][2:a][3:a]amix=inputs=4:normalize=0,lowpass=f=900,` +
    `aecho=0.8:0.5:180:0.25,aecho=0.7:0.4:360:0.15,` +
    `afade=t=in:st=0:d=2.5,afade=t=out:st=${durSec - 3}:d=3,volume=0.5`;
  ffmpeg(['-y', ...inputs, '-filter_complex', fc, '-c:a', 'pcm_s16le', outWav]);
}

function addAudio(videoPath, wavPath, outPath, dur) {
  const st = Math.max(0, dur - 0.6);
  const fc = `[1:a]afade=t=in:st=0:d=0.6,afade=t=out:st=${st.toFixed(2)}:d=0.6[a]`;
  ffmpeg(['-y', '-i', videoPath, '-i', wavPath, '-filter_complex', fc,
    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-shortest', outPath]);
}

// 渲染一组场景帧并转成片段
function buildClips(scenes, W, H, tmp) {
  return scenes.map((s, i) => {
    const framePath = path.join(tmp, `f-${i}.png`);
    const clipPath = path.join(tmp, `c-${i}.mp4`);
    renderFrame(s, W, H, framePath);
    frameToClip(framePath, clipPath, s.dur);
    return clipPath;
  });
}

function runBrandPack() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.mkdirSync(SPLIT_DIR, { recursive: true });
  const tmp = fs.mkdtempSync(path.join(OUT_DIR, '.tmp-'));

  try {
    // 1) BGM 素材
    const bgm = path.join(OUT_DIR, 'bgm.wav');
    console.log('🎵 合成 BGM...');
    genBgm(bgm);
    const totalDur = SCENES.reduce((a, s) => a + s.dur, 0);

    // 2) 竖版 9:16（1080x1920）
    console.log('\n📱 竖版 1080×1920...');
    const vTmp = path.join(tmp, 'v'); fs.mkdirSync(vTmp);
    const vClips = buildClips(SCENES, 1080, 1920, vTmp);
    const vMerged = path.join(tmp, 'v-merged.mp4');
    concat(vClips, vMerged);
    addAudio(vMerged, bgm, path.join(OUT_DIR, '心同共生-品牌片-竖版-带音乐.mp4'), totalDur);
    console.log('  ✅ 心同共生-品牌片-竖版-带音乐.mp4');

    // 3) 横版 16:9（1920x1080）
    console.log('\n🖥️  横版 1920×1080...');
    const hTmp = path.join(tmp, 'h'); fs.mkdirSync(hTmp);
    const hClips = buildClips(SCENES, 1920, 1080, hTmp);
    const hMerged = path.join(tmp, 'h-merged.mp4');
    concat(hClips, hMerged);
    addAudio(hMerged, bgm, path.join(OUT_DIR, '心同共生-品牌片-横版-带音乐.mp4'), totalDur);
    console.log('  ✅ 心同共生-品牌片-横版-带音乐.mp4');

    // 4) 6 个单场景竖屏短视频（带 BGM）
    console.log('\n🎬 拆分 6 个单场景竖屏...');
    SCENES.forEach((s, i) => {
      const out = path.join(SPLIT_DIR, `${s.slug}.mp4`);
      addAudio(vClips[i], bgm, out, s.dur);
      console.log(`  ✅ ${s.slug}.mp4`);
    });

    console.log(`\n🎉 全部完成 -> ${OUT_DIR}`);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) runBrandPack();
