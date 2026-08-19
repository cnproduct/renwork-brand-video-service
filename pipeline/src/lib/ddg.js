// DuckDuckGo HTML 端点搜索（无需 API Key）
// 返回结构化结果：{ title, url, snippet }
import * as cheerio from 'cheerio';

const DDG_ENDPOINT = 'https://html.duckduckgo.com/html/';

/**
 * 用 DuckDuckGo 搜索关键词。
 * @param {string} query 搜索关键词
 * @param {number} max 最多返回条数
 * @returns {Promise<Array<{title:string,url:string,snippet:string}>>}
 */
export async function ddgSearch(query, max = 5) {
  const params = new URLSearchParams({ q: query });
  const res = await fetch(`${DDG_ENDPOINT}?${params}`, {
    headers: {
      'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36',
      'Accept-Language': 'en-US,en;q=0.9',
    },
  });
  if (!res.ok) {
    throw new Error(`DuckDuckGo search failed: HTTP ${res.status}`);
  }
  const html = await res.text();
  const $ = cheerio.load(html);

  const results = [];
  $('.result').each((_, el) => {
    const a = $(el).find('a.result__a');
    const title = a.text().trim();
    // DDG 对结果链接做了重定向包装，需要解出真实 URL
    let url = a.attr('href') || '';
    const m = url.match(/uddg=([^&]+)/);
    if (m) url = decodeURIComponent(m[1]);
    const snippet = $(el).find('.result__snippet').text().trim();
    if (title && url) results.push({ title, url, snippet });
  });

  return results.slice(0, max);
}
