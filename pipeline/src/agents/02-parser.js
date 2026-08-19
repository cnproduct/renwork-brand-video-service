#!/usr/bin/env node
// ============================================================
// 智能体 02 — Cheerio 清洗
// 从 data/raw/*.html 抽取：网站标题、核心产品关键词、邮箱、电话、社媒链接
// 结果落盘到 data/parsed/*.json
// ============================================================
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import * as cheerio from 'cheerio';
import { PATHS, PARSE } from '../config.js';

// 从一段 HTML 里抽取所有合规邮箱
function extractEmails(html) {
  const found = new Set();
  const matches = html.match(PARSE.emailRegex) || [];
  for (const m of matches) {
    const email = m.replace(/[.,;:]+$/, ''); // 去掉尾部标点
    if (PARSE.emailBlacklist.some((re) => re.test(email))) continue;
    found.add(email.toLowerCase());
  }
  return [...found];
}

// 常见社媒域，用于抽取官方账号链接
const SOCIAL_DOMAINS = ['facebook.com', 'instagram.com', 'linkedin.com', 'twitter.com', 'youtube.com', 'tiktok.com', 'whatsapp.com'];

function extractSocials($) {
  const out = [];
  $('a[href]').each((_, el) => {
    const href = ($(el).attr('href') || '').toLowerCase();
    if (SOCIAL_DOMAINS.some((d) => href.includes(d))) out.push(href);
  });
  return [...new Set(out)].slice(0, 12);
}

function extractPhones($) {
  const out = [];
  $('a[href^="tel:"]').each((_, el) => {
    const p = ($(el).attr('href') || '').replace('tel:', '').trim();
    if (p && p !== 'tel') out.push(p);
  });
  return [...new Set(out)].slice(0, 6);
}

// 从标题/描述/正文抽核心产品关键词（针对卫浴/五金品类做加权）
function extractProductHints($, text) {
  const PROD_WORDS = [
    'faucet', 'tap', 'shower', 'sanitary', 'bathroom', 'basin', 'toilet', 'bidet',
    'angle valve', 'valve', 'drain', 'sink', 'bathtub', 'ceramic', 'vanity',
    'plumbing', 'hardware', 'kitchen', 'washbasin', 'mixer', 'chrome',
  ];
  const lower = text.toLowerCase();
  return PROD_WORDS.filter((w) => lower.includes(w)).slice(0, 20);
}

export function parseHtml(html, meta = {}) {
  const $ = cheerio.load(html);
  const title = ($('title').first().text() || '').trim();
  const description = ($('meta[name="description"]').attr('content') || '').trim();
  const keywords = ($('meta[name="keywords"]').attr('content') || '').trim();
  const h1 = ($('h1').first().text() || '').trim();
  const bodyText = $('body').text().replace(/\s+/g, ' ').slice(0, 6000);

  const emails = extractEmails(html);
  const fullText = `${title} ${description} ${keywords} ${bodyText}`;

  return {
    ...meta,
    title,
    description,
    h1,
    emails,
    phones: extractPhones($),
    socials: extractSocials($),
    productHints: extractProductHints($, fullText),
    wordCount: bodyText.length,
  };
}

export function runParser() {
  fs.mkdirSync(PATHS.parsed, { recursive: true });
  const indexRaw = path.join(PATHS.raw, 'index.json');
  if (!fs.existsSync(indexRaw)) {
    console.error('❌ 找不到 data/raw/index.json，请先运行 01-crawler');
    process.exit(1);
  }
  const index = JSON.parse(fs.readFileSync(indexRaw, 'utf8'));
  const parsed = [];

  for (const item of index) {
    if (item.status === 'error' || !item.file) continue;
    const rawPath = path.join(PATHS.raw, item.file);
    if (!fs.existsSync(rawPath)) continue;
    const html = fs.readFileSync(rawPath, 'utf8');
    const result = parseHtml(html, {
      keyword: item.keyword,
      url: item.url,
      finalUrl: item.finalUrl,
    });
    const outName = `${path.basename(item.file, '.html')}.json`;
    fs.writeFileSync(path.join(PATHS.parsed, outName), JSON.stringify(result, null, 2), 'utf8');
    parsed.push(result);
    const emailStr = result.emails.length ? `💌 ${result.emails.slice(0, 3).join(', ')}` : '⛔ 无邮箱';
    console.log(`  ✅ ${result.title?.slice(0, 40) || result.url} — ${emailStr}`);
  }

  fs.writeFileSync(path.join(PATHS.parsed, 'parsed.json'), JSON.stringify(parsed, null, 2), 'utf8');
  const totalEmails = parsed.reduce((a, p) => a + p.emails.length, 0);
  console.log(`\n📊 清洗完成：${parsed.length} 个页面，共抽取 ${totalEmails} 个邮箱 -> data/parsed/parsed.json`);
  return parsed;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) runParser();
