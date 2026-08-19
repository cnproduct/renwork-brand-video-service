// ============================================================
// RenWork Pipeline 统一配置
// 私密信息一律走环境变量，本文件只放可公开的结构化配置。
// ============================================================
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import os from 'node:os';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

export const PATHS = {
  root: ROOT,
  raw: path.join(ROOT, 'data', 'raw'),       // 01 抓取的原始 HTML
  parsed: path.join(ROOT, 'data', 'parsed'), // 02 清洗后的 JSON
  db: path.join(ROOT, 'data', 'leads.db'),   // 03 SQLite 线索库
  emailsOut: path.join(ROOT, 'out', 'emails'),
  videosOut: path.join(ROOT, 'out', 'videos'),
  productAssets: path.join(ROOT, 'assets', 'products'),
};

// ------------------------------------------------------------
// 01 抓取：DuckDuckGo 搜索 + 本地爬虫
// ------------------------------------------------------------
export const CRAWL = {
  // 搜索关键词：可按 "品类 + 采购商/分销商 + 国家" 扩展
  keywords: [
    'sanitary ware distributor USA',
    'kitchen faucet importer Germany',
    'bathroom fittings wholesaler UK',
    'faucet distributor Australia',
  ],
  maxResultsPerKeyword: 5,   // 每个关键词取前 N 条结果
  crawlTimeoutMs: 15000,     // 单站抓取超时
  maxRedirects: 3,
  userAgent:
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' +
    '(KHTML, like Gecko) Chrome/124.0 Safari/537.36 RenWorkBot/1.0',
  politeDelayMs: 800,        // 请求间礼貌间隔
};

// ------------------------------------------------------------
// 02 清洗：Cheerio 抽取规则
// ------------------------------------------------------------
export const PARSE = {
  emailRegex: /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g,
  // 跳过明显是抓取/库图/统计类邮箱
  emailBlacklist: [
    /\.png$/i, /\.jpg$/i, /\.jpeg$/i, /\.gif$/i, /\.svg$/i, /\.webp$/i,
    /sentry\.io/i, /example\.com/i, /wixpress\.com/i, /@2x$/i,
  ],
  // 常见的联系方式/产品关键词，用于抽取上下文
  contactHints: ['tel:', 'mailto:', 'whatsapp', 'contact', 'inquiry', 'quote'],
};

// ------------------------------------------------------------
// 03 存储：SQLite 线索库 schema 由 03-store.js 创建
// ------------------------------------------------------------

// ------------------------------------------------------------
// 04 开发信：Nodemailer + SMTP（凭据从环境变量读取）
// ------------------------------------------------------------
export const MAIL = {
  // 从环境变量读取，避免写入仓库：SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS
  smtp: {
    host: process.env.SMTP_HOST || 'smtp.zoho.com',
    port: Number(process.env.SMTP_PORT || 465),
    secure: process.env.SMTP_SECURE !== 'false',
    user: process.env.SMTP_USER || '',
    pass: process.env.SMTP_PASS || '',
  },
  fromName: 'Philip', // 发件人显示名
  batchSize: 10,        // 每批发送数量
  minDelayMs: 30_000,   // 批次内最小间隔（防封号）
  maxDelayMs: 120_000,
  // 个性化模板，支持占位符：{{company}} {{contact}} {{product}} {{sender}}
  subjectTemplate: '{{product}} — factory-direct supply for {{company}}',
  bodyTemplate: [
    'Hi {{contact}},',
    '',
    'I noticed {{company}} is active in the {{product}} market.',
    '',
    'We are a factory-direct manufacturer and can supply {{product}} with:',
    '- Competitive MOQ and fast lead time',
    '- CE / ISO certified quality',
    '- Private label & OEM support',
    '',
    'Would you be open to a short intro call this week?',
    '',
    'Best regards,',
    '{{sender}}',
  ].join('\n'),
};

// ------------------------------------------------------------
// 05 短视频：FFmpeg 批量多语言
// ------------------------------------------------------------
export const VIDEO = {
  width: 1080,
  height: 1920, // 9:16 竖屏
  fps: 30,
  durationSec: 6,
  // 多语言字幕（标题 + CTA）
  languages: [
    { code: 'en', title: 'FACTORY DIRECT QUALITY', cta: 'DM for samples' },
    { code: 'es', title: 'CALIDAD DIRECTA DE FÁBRICA', cta: 'Pide muestras' },
    { code: 'ar', title: 'جودة مباشرة من المصنع', cta: 'اطلب عينات' },
  ],
  // 系统可用字体（按顺序取第一个存在的）
  fonts: [
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/Supplemental/Arial.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
  ],
};

// 全局默认旁白：所有新视频生成器统一使用 Edge TTS 云扬中文男声。
// 可通过 RENWORK_TTS_PROVIDER=say 临时回退到 macOS say，但默认不回退。
export const TTS = {
  provider: process.env.RENWORK_TTS_PROVIDER || 'edge-tts',
  voice: process.env.RENWORK_TTS_VOICE || 'zh-CN-YunyangNeural',
  rate: process.env.RENWORK_TTS_RATE || '+4%',
  pitch: process.env.RENWORK_TTS_PITCH || '+0Hz',
};

export default { PATHS, CRAWL, PARSE, MAIL, VIDEO, TTS };
