#!/usr/bin/env node
// ============================================================
// 智能体 03 — SQLite 线索库 (Node 内置 node:sqlite)
// 把 02 清洗结果写入 data/leads.db，按邮箱去重
// ============================================================
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { DatabaseSync } from 'node:sqlite';
import { PATHS } from '../config.js';

const SCHEMA = `
CREATE TABLE IF NOT EXISTS leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE,
  company TEXT,
  website TEXT,
  country TEXT,
  product_hints TEXT,
  source_url TEXT,
  source_keyword TEXT,
  phones TEXT,
  socials TEXT,
  first_seen TEXT,
  last_seen TEXT
);
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email);
`;

export function openDb(dbPath = PATHS.db) {
  const db = new DatabaseSync(dbPath);
  db.exec(SCHEMA);
  return db;
}

export function runStore() {
  fs.mkdirSync(path.dirname(PATHS.db), { recursive: true });
  const parsedPath = path.join(PATHS.parsed, 'parsed.json');
  if (!fs.existsSync(parsedPath)) {
    console.error('❌ 找不到 data/parsed/parsed.json，请先运行 02-parser');
    process.exit(1);
  }
  const parsed = JSON.parse(fs.readFileSync(parsedPath, 'utf8'));
  const db = openDb();

  const insert = db.prepare(`
    INSERT INTO leads
      (email, company, website, country, product_hints, source_url, source_keyword, phones, socials, first_seen, last_seen)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(email) DO UPDATE SET last_seen = excluded.last_seen
  `);

  const now = new Date().toISOString();
  let added = 0;

  db.exec('BEGIN');
  for (const p of parsed) {
    if (!p.emails?.length) continue;
    for (const email of p.emails) {
      insert.run(
        email,
        p.h1 || p.title || '',
        p.finalUrl || p.url || '',
        '', // country 可由后续 locale 判断补充
        (p.productHints || []).join('|'),
        p.url || '',
        p.keyword || '',
        (p.phones || []).join('|'),
        (p.socials || []).join('|'),
        now,
        now
      );
      added++;
    }
  }
  db.exec('COMMIT');

  const total = db.prepare('SELECT COUNT(*) AS c FROM leads').get().c;
  console.log(`💾 本次写入 ${added} 条，线索库当前共 ${total} 条 -> ${PATHS.db}`);
  db.close();
  return total;
}

// 便捷：打印线索库概览
export function showLeads(limit = 20) {
  const db = openDb();
  const rows = db.prepare('SELECT id, email, company, website, source_keyword FROM leads ORDER BY id DESC LIMIT ?').all(limit);
  console.table(rows);
  db.close();
  return rows;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  runStore();
  if (process.argv.includes('--show')) showLeads();
}
