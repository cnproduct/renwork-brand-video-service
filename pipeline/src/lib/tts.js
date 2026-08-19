import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
import { TTS } from '../config.js';

export function ttsFileExtension() {
  return TTS.provider === 'edge-tts' ? 'mp3' : 'aiff';
}

export function synthesizeTts(text, outputPath) {
  if (!text) return;
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    fs.rmSync(outputPath, { force: true });
    let result;
    if (TTS.provider === 'edge-tts') {
      result = spawnSync('python3', [
        '-m', 'edge_tts', '-t', text, '-v', TTS.voice,
        '--rate', TTS.rate, '--pitch', TTS.pitch,
        '--write-media', outputPath,
      ], { encoding: 'utf8' });
    } else {
      result = spawnSync('say', ['-v', 'Tingting', '-r', '175', '-o', outputPath, text], { encoding: 'utf8' });
    }
    const size = fs.existsSync(outputPath) ? fs.statSync(outputPath).size : 0;
    if (result.status === 0 && size > 1000) return outputPath;
    if (attempt < 3) spawnSync('sleep', ['1.5']);
  }
  throw new Error(`TTS 生成失败：${TTS.provider} / ${TTS.voice}`);
}
