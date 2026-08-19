#!/usr/bin/env node
// 把旁白(TTS) + BGM 混录到 Remotion 版成片上
// 场景时长与 XintongBrandFilm 的 SCENE_FRAMES 对齐
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { synthesizeTts, ttsFileExtension } from '../lib/tts.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT_DIR = path.join(HERE, '..', '..', 'out', 'videos', 'brand-film');

// 与 Remotion SCENE_FRAMES=[90,447,441,530,460,459,453] 对应的秒数
const DURS = [3.0, 447 / 30, 441 / 30, 530 / 30, 460 / 30, 459 / 30, 453 / 30];
const NARR = [
  '',
  '很多人以为，书院和公司，一个做公益，一个做生意，不过是松散的搭档。其实，心同书院与心同共生，是一套跨越百年的双轮文明工程。',
  '书院守护纯粹的公心教育与文化信任场，共生则建立可持续的商业造血能力。一个让人安住本心，一个让人生起妙用，定慧一体，缺一不可。',
  '它们共同服务于同一个使命：启世人公心，化世界大同。书院守公益、守公信，共生连资源、做产品、反哺公益。法律独立，财务隔离，治理协同，公开透明。',
  '沿着明白、做到、利他、共生四步路径，一步也不能跳。十年之后，建成三千所纯公益书院，培养一万名公益讲师，每年一万场公益分享。',
  '二零二六年九月二十八日，首届一日文化节暨祭孔大典，正式开启协同元年。第一年做样板，第三年建网络，第五年成平台，第十年立生态。',
  '最好的协同，不是互相依赖，而是各自独立、彼此成就。书院让经济有了文化之根与公心方向，共生让公益理想有了资源、工具与长久的生命力。',
];

const ffmpeg = (a) => execFileSync('ffmpeg', a, { stdio: 'pipe' });

function main() {
  const tmp = fs.mkdtempSync(path.join(OUT_DIR, '.audio-'));
  try {
    const parts = [];
    NARR.forEach((text, i) => {
      const dur = DURS[i];
      const part = path.join(tmp, `nar-${i}.wav`);
      if (!text) {
        ffmpeg(['-y', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', dur.toFixed(2), '-c:a', 'pcm_s16le', part]);
      } else {
        const raw = path.join(tmp, `tts-${i}.${ttsFileExtension()}`);
        synthesizeTts(text, raw);
        ffmpeg(['-y', '-i', raw, '-ar', '44100', '-ac', '1', '-af', 'apad', '-t', dur.toFixed(2), '-c:a', 'pcm_s16le', part]);
      }
      parts.push(part);
    });

    const total = DURS.reduce((a, b) => a + b, 0);
    const list = path.join(tmp, 'list.txt');
    fs.writeFileSync(list, parts.map((p) => `file '${p}'`).join('\n'), 'utf8');
    const nar = path.join(tmp, 'narration.wav');
    ffmpeg(['-y', '-f', 'concat', '-safe', '0', '-i', list, '-ar', '44100', '-ac', '1', '-c:a', 'pcm_s16le', nar]);

    // BGM
    const F = [110, 164.81, 220, 329.63];
    const inputs = F.map((f) => ['-f', 'lavfi', '-i', `sine=frequency=${f}:duration=${total + 4}`]).flat();
    const bgm = path.join(tmp, 'bgm.wav');
    ffmpeg(['-y', ...inputs, '-filter_complex',
      '[0:a][1:a][2:a][3:a]amix=inputs=4:normalize=0,lowpass=f=900,aecho=0.8:0.5:180:0.25,aecho=0.7:0.4:360:0.15,afade=t=in:st=0:d=2.5,afade=t=out:st=' + (total - 1) + ':d=3,volume=0.55',
      '-c:a', 'pcm_s16le', bgm]);

    const src = path.join(OUT_DIR, '心同共生-品牌片-Remotion版.mp4');
    const dst = path.join(OUT_DIR, '心同共生-品牌片-Remotion版-带配音.mp4');
    ffmpeg(['-y', '-i', src, '-i', nar, '-i', bgm,
      '-filter_complex', '[2:a]volume=0.16[bg];[1:a][bg]amix=inputs=2:duration=first:normalize=0[a]',
      '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', '-shortest', dst]);
    console.log('✅ 完成 ->', dst);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
}

main();
