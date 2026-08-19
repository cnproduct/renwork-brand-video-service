#!/usr/bin/env node
// ============================================================
// 智能体 05 — 多语言短视频批量生成
// 文字帧用 Pillow 渲染（跨语言），再交给 FFmpeg 封装为 9:16 竖屏 mp4。
// 进阶动效版本见 ../video-remotion/
// ============================================================
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync, spawnSync } from 'node:child_process';
import { PATHS, VIDEO } from '../config.js';

const RENDER_PY = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'lib', 'render_frame.py');

// 演示产品清单（真实场景可从线索库/产品事实库读取）
const PRODUCTS = [
  { sku: 'RK-1001', name: 'Chrome Kitchen Faucet', color: '0x1f2937' },
  { sku: 'RK-2002', name: 'Pull-out Spring Tap', color: '0x0f766e' },
  { sku: 'RK-3003', name: 'Brass Angle Valve', color: '0x7c2d12' },
];

// 用 Pillow 渲染单帧
function renderFrame(cfg) {
  const r = spawnSync('python3', [RENDER_PY], { input: JSON.stringify(cfg), encoding: 'utf8' });
  if (r.status !== 0) throw new Error(r.stderr || 'Pillow render failed');
}

// 单帧 -> 6 秒视频
function frameToVideo(framePath, outPath) {
  execFileSync('ffmpeg', [
    '-y',
    '-loop', '1',
    '-i', framePath,
    '-t', String(VIDEO.durationSec),
    '-r', String(VIDEO.fps),
    '-vf', `scale=${VIDEO.width}:${VIDEO.height}:force_original_aspect_ratio=decrease,pad=${VIDEO.width}:${VIDEO.height}:(ow-iw)/2:(oh-ih)/2`,
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-an',
    outPath,
  ], { stdio: 'pipe' });
}

export function runVideo() {
  fs.mkdirSync(PATHS.videosOut, { recursive: true });
  const tmp = fs.mkdtempSync(path.join(PATHS.videosOut, '.frames-'));

  let count = 0;
  try {
    for (const product of PRODUCTS) {
      for (const lang of VIDEO.languages) {
        const framePath = path.join(tmp, `${product.sku}-${lang.code}.png`);
        const outPath = path.join(PATHS.videosOut, `${product.sku}-${lang.code}.mp4`);
        try {
          renderFrame({
            out: framePath,
            product: product.name,
            title: lang.title,
            cta: lang.cta,
            color: product.color,
            width: VIDEO.width,
            height: VIDEO.height,
          });
          frameToVideo(framePath, outPath);
          count++;
          console.log(`  ✅ ${product.sku} [${lang.code}] ${product.name} -> ${path.basename(outPath)}`);
        } catch (e) {
          console.warn(`  ❌ ${product.sku} [${lang.code}] 失败: ${e.message}`);
        }
      }
    }
    console.log(`\n🎉 共生成 ${count} 个短视频 -> out/videos/`);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
  return count;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) runVideo();
