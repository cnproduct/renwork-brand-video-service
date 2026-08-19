// 轻量本地爬虫：抓取 URL 返回 HTML 文本（利用 Node 内置 fetch）
import { CRAWL } from '../config.js';

/**
 * 抓取单个 URL。
 * @param {string} url
 * @returns {Promise<{url:string, finalUrl:string, status:number, html:string, contentType:string}>}
 */
export async function fetchPage(url) {
  const res = await fetch(url, {
    redirect: 'follow',
    signal: AbortSignal.timeout(CRAWL.crawlTimeoutMs),
    headers: {
      'User-Agent': CRAWL.userAgent,
      'Accept': 'text/html,application/xhtml+xml',
      'Accept-Language': 'en-US,en;q=0.9',
    },
  });
  const html = await res.text();
  return {
    url,
    finalUrl: res.url || url,
    status: res.status,
    contentType: res.headers.get('content-type') || '',
    html,
  };
}

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
