#!/usr/bin/env node
// ============================================================
// RenWork Pipeline 一键串联
//   node src/pipeline.js            完整流程（开发信/视频默认 dry-run）
//   node src/pipeline.js --dry-run  同上，显式 dry-run
//   node src/pipeline.js --skip-crawl  跳过抓取（用已有 raw/parsed）
//   node src/pipeline.js --send --product "kitchen faucets"  真实发信
// ============================================================
import path from 'node:path';
import { runCrawler } from './agents/01-crawler.js';
import { runParser } from './agents/02-parser.js';
import { runStore } from './agents/03-store.js';
import { runMailer } from './agents/04-mailer.js';
import { runVideo } from './agents/05-video.js';

const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run') || !args.includes('--send');
const skipCrawl = args.includes('--skip-crawl');
const productIdx = args.indexOf('--product');
const product = productIdx > -1 ? args[productIdx + 1] : 'bathroom faucets';

const banner = (t) => console.log(`\n${'═'.repeat(56)}\n▶ ${t}\n${'═'.repeat(56)}`);

async function main() {
  console.log('🚀 RenWork Pipeline 启动');

  if (!skipCrawl) {
    banner('01 抓取：DuckDuckGo 搜索 + 本地爬虫');
    await runCrawler();
  }

  banner('02 清洗：Cheerio 抽取产品与邮箱');
  runParser();

  banner('03 存储：SQLite 线索库');
  runStore();

  banner('04 开发信：Nodemailer 个性化分发');
  await runMailer({ dryRun, product });

  banner('05 短视频：FFmpeg 多语言批量生成');
  runVideo();

  console.log(`\n✅ 全流程完成。线索库: data/leads.db | 开发信预览: out/emails/ | 视频: out/videos/`);
}

main().catch((e) => {
  console.error('\n❌ 管线中断:', e.message);
  process.exit(1);
});
