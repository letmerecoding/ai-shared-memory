const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

// 配置邮箱
const transporter = nodemailer.createTransport({
  host: 'smtp.163.com',
  port: 465,
  secure: true,
  auth: {
    user: 'letmerecoding@163.com',
    pass: 'RERPuwtFqeidbnce'
  }
});

// 获取昨天的日期
const date = new Date();
date.setDate(date.getDate() - 1);
const dateStr = date.toISOString().split('T')[0];
const newsFile = path.join('/Users/matianjun/.openclaw/workspace/news', `${dateStr}.md`);

// 读取新闻文件
const newsContent = fs.readFileSync(newsFile, 'utf8');

// 邮件选项
const mailOptions = {
  from: '"每日新闻摘要" <letmerecoding@163.com>',
  to: '18839139910@163.com',
  subject: `${dateStr} 重要新闻摘要`,
  text: newsContent,
  html: `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>${dateStr} 重要新闻摘要</title>
      <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 1000px; margin: 0 auto; padding: 20px; }
        h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        h2 { color: #3498db; margin-top: 30px; }
        .news-item { margin-bottom: 20px; padding-left: 10px; border-left: 3px solid #eee; }
        .news-title { font-weight: bold; font-size: 1.1em; margin-bottom: 5px; }
        .news-meta { color: #7f8c8d; font-size: 0.9em; margin-bottom: 5px; }
        .summary { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 30px; }
      </style>
    </head>
    <body>
      ${newsContent.replace(/^# (.*)$/gm, '<h1 style="color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;">$1</h1>')
                   .replace(/^## (.*)$/gm, '<h2 style="color: #3498db; margin-top: 30px; font-size: 1.3em;">$1</h2>')
                   .replace(/^([0-9]+)、(.*)$/gm, '<div style="margin-bottom: 20px; padding-left: 10px; border-left: 3px solid #eee;"><div style="font-weight: bold; font-size: 1.1em; margin-bottom: 5px;">$1、$2</div>')
                   .replace(/^来源：(.*) \| (.*)$/gm, '<div style="color: #7f8c8d; font-size: 0.9em; margin-bottom: 15px;">来源：<a href="$2" style="color: #3498db; text-decoration: none;">$1</a></div></div>')
                   .replace(/^---$/gm, '<hr style="border: 1px solid #eee; margin: 20px 0;">')}
    </body>
    </html>
  `
};

// 发送邮件
transporter.sendMail(mailOptions, (error, info) => {
  if (error) {
    console.error('邮件发送失败:', error);
    process.exit(1);
  }
  console.log('邮件发送成功:', info.response);
  process.exit(0);
});
