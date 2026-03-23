const axios = require('axios');
const cheerio = require('cheerio');

async function crawlWeixinArticle(url) {
  try {
    const response = await axios.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
      }
    });
    
    const $ = cheerio.load(response.data);
    const content = $('#js_content').text();
    console.log('文章内容提取成功：');
    console.log(content.slice(0, 5000)); // 提取前5000字符
  } catch (error) {
    console.error('爬取失败:', error.message);
  }
}

crawlWeixinArticle('https://mp.weixin.qq.com/s/eqoCBWVaRW90jYvp0BI2fg');
