#!/usr/bin/env node
// ============================================================
// 智能体 01 — DuckDuckGo 搜索 + 本地爬虫
// 抓取海外采购商与竞品独立站，原始 HTML 落盘到 data/raw/
// ============================================================
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PATHS, CRAWL } from '../config.js';
import { ddgSearch } from '../lib/ddg.js';
import { fetchPage, sleep } from '../lib/crawler.js';

function slugify(s) {
  return (s || '')
    .toLowerCase()
    .replace(/^https?:\/\//, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 80);
}

export async function runCrawler({ keywords = CRAWL.keywords, maxPer = CRAWL.maxResultsPerKeyword } = {}) {
  fs.mkdirSync(PATHS.raw, { recursive: true });
  const index = []; // 抓取清单，供 02 解析
  const seen = new Set();

  for (const kw of keywords) {
    console.log(`\n🔎 搜索: ${kw}`);
    let results;
    try {
      results = await ddgSearch(kw, maxPer);
    } catch (e) {
      console.warn(`  ⚠️ 搜索失败: ${e.message}`);
      continue;
    }
    console.log(`  命中 ${results.length} 条结果`);

    for (const r of results) {
      const host = r.url;
      if (seen.has(host)) continue;
      seen.add(host);
      try {
        await sleep(CRAWL.politeDelayMs);
        const page = await fetchPage(r.url);
        const file = `${slugify(r.url)}.html`;
        const outPath = path.join(PATHS.raw, file);
        fs.writeFileSync(outPath, page.html, 'utf8');
        index.push({
          keyword: kw,
          title: r.title,
          url: r.url,
          finalUrl: page.finalUrl,
          status: page.status,
          file,
          fetchedAt: new Date().toISOString(),
        });
        console.log(`  ✅ [${page.status}] ${r.title?.slice(0, 50)} -> ${file} (${page.html.length} bytes)`);
      } catch (e) {
        index.push({ keyword: kw, title: r.title, url: r.url, status: 'error', error: e.message });
        console.warn(`  ❌ ${r.url} — ${e.message}`);
      }
    }
  }

  fs.writeFileSync(path.join(PATHS.raw, 'index.json'), JSON.stringify(index, null, 2), 'utf8');
  console.log(`\n📦 共抓取 ${index.filter((i) => i.status !== 'error').length} 个页面，清单已写入 data/raw/index.json`);
  return index;
}

// 直接运行：node src/agents/01-crawler.js
const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  runCrawler().catch((e) => {
    console.error(e);
    process.exit(1);
  });
}
