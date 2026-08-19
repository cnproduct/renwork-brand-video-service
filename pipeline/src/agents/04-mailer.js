#!/usr/bin/env node
// ============================================================
// 智能体 04 — Nodemailer 个性化开发信分发
// 从线索库读取邮箱，套用模板，经 SMTP 批量发送（支持 dry-run）
// ============================================================
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import nodemailer from 'nodemailer';
import { PATHS, MAIL } from '../config.js';
import { openDb } from './03-store.js';
import { sleep } from '../lib/crawler.js';

function fill(tpl, vars) {
  return tpl.replace(/\{\{(\w+)\}\}/g, (_, k) => vars[k] ?? '');
}

// 从邮箱/公司名猜测联系人称呼（默认 "there"）
function guessContact(email) {
  const local = (email.split('@')[0] || '').replace(/[^a-zA-Z]/g, '');
  if (local.length >= 2) return local[0].toUpperCase() + local.slice(1);
  return 'there';
}

function guessCompany(lead) {
  if (lead.company) return lead.company;
  try { return new URL(lead.website).hostname.replace(/^www\./, ''); } catch { return lead.website; }
}

export function buildEmail(lead, product) {
  const sender = `${MAIL.fromName}`;
  const company = guessCompany(lead);
  const contact = guessContact(lead.email);
  const vars = { company, contact, product, sender };
  return {
    to: lead.email,
    subject: fill(MAIL.subjectTemplate, vars),
    text: fill(MAIL.bodyTemplate, vars),
  };
}

export async function runMailer({ dryRun = true, product = 'bathroom faucets', limit = Infinity } = {}) {
  const { host, port, secure, user, pass } = MAIL.smtp;
  const db = openDb();
  const leads = db.prepare('SELECT * FROM leads ORDER BY id ASC').all();
  db.close();

  if (!leads.length) {
    console.log('⚠️ 线索库为空，请先运行 01→02→03 抓取并入库');
    return 0;
  }

  const targets = leads.slice(0, limit);
  console.log(`📮 待发送 ${targets.length} 封（dryRun=${dryRun}）`);

  let transporter = null;
  if (!dryRun) {
    if (!user || !pass) {
      throw new Error('缺少 SMTP_USER / SMTP_PASS 环境变量，无法真实发送');
    }
    transporter = nodemailer.createTransport({ host, port, secure, auth: { user, pass } });
  }

  fs.mkdirSync(PATHS.emailsOut, { recursive: true });
  let sent = 0;

  for (let i = 0; i < targets.length; i++) {
    const lead = targets[i];
    const email = buildEmail(lead, product);

    if (dryRun) {
      // 落盘预览，不真实发送
      const file = path.join(PATHS.emailsOut, `${lead.id}-${lead.email.replace(/[^a-zA-Z0-9@.-]/g, '_')}.txt`);
      fs.writeFileSync(file, `TO: ${email.to}\nSUBJECT: ${email.subject}\n\n${email.text}`, 'utf8');
    } else {
      await transporter.sendMail({ from: `"${MAIL.fromName}" <${user}>`, ...email });
    }
    sent++;
    console.log(`  ${dryRun ? '📝' : '✉️'}  [${i + 1}/${targets.length}] ${email.to} — ${email.subject}`);

    // 批次间隔，降低被标记风险
    if (!dryRun && (i + 1) % MAIL.batchSize === 0 && i + 1 < targets.length) {
      const wait = MAIL.minDelayMs + Math.random() * (MAIL.maxDelayMs - MAIL.minDelayMs);
      console.log(`  ⏳ 批次暂停 ${Math.round(wait / 1000)}s 防封号...`);
      await sleep(wait);
    }
  }

  console.log(`✅ 完成：${sent} 封${dryRun ? '（已生成预览，未真实发送）' : '已发送'} -> out/emails/`);
  return sent;
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  const dryRun = !process.argv.includes('--send');
  const productIdx = process.argv.indexOf('--product');
  const product = productIdx > -1 ? process.argv[productIdx + 1] : 'bathroom faucets';
  runMailer({ dryRun, product }).catch((e) => {
    console.error(e);
    process.exit(1);
  });
}
