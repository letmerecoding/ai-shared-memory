import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

date_str = '2026-03-10'
news_file = '/Users/matianjun/.openclaw/workspace/news/2026-03-10.md'

with open(news_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Word风格HTML
html = f'''
<html>
<head><meta charset="utf-8">
<style>
    body{{font-family:"宋体",微软雅黑;font-size:14px;line-height:1.5;color:#000}}
    h1{{font-size:16px;font-weight:bold;text-align:center;margin:20px 0 10px}}
    .meta{{font-size:12px;text-align:center;color:#666;margin-bottom:20px}}
    h2{{font-size:15px;font-weight:bold;margin:15px 0 8px}}
    .news{{margin:10px 0 15px 2em}}
    .news-title{{font-weight:bold;margin-bottom:5px}}
    .news-content{{margin-bottom:5px;text-indent:2em}}
    .news-source{{font-size:12px;color:#666}}
    hr{{border:0;border-top:1px solid #ccc;margin:20px 0}}
    .summary{{margin:15px 0;padding:10px;border:1px solid #ccc;background:#f9f9f9}}
    .footer{{font-size:12px;color:#666;text-align:center;margin-top:20px}}
    .model-info{{font-size:12px;color:#666;text-align:right;margin-top:20px;padding-top:10px;border-top:1px solid #eee}}
</style>
</head>
<body>
    <h1>{date_str} 重要新闻摘要</h1>
    <div class="meta">整理时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
    <hr>
'''

lines = content.split("\n")
in_news = in_summary = in_model = False
for line in lines:
    line = line.strip()
    if not line: continue
    # 支持两种分类格式：## 一、分类 和 ### 分类
    if (line.startswith("## 一、") or line.startswith("## 二、") or line.startswith("## 三、") or 
        line.startswith("## 四、") or line.startswith("## 五、") or line.startswith("### ")):
        if in_news: html += "</div>"
        # 提取分类名称
        if line.startswith("### "):
            category = line[4:].split("（")[0].strip()
        else:
            category = line[3:].split("（")[0].strip()
        html += f"<h2>{category}</h2>"
        in_news = False
    elif line.startswith("## 六、今日总结") or line.endswith("总结"):
        if in_news: html += "</div>"
        html += "<h2>今日总结</h2><div class='summary'>"
        in_summary = True
        in_news = False
    elif line.startswith("## 生产信息"):
        if in_summary: html += "</div>"
        if in_news: html += "</div>"
        html += "<div class='model-info'>"
        in_model = True
        in_news = in_summary = False
    elif line.startswith("---"):
        html += "<hr>"
    elif line.startswith("*以上"):
        if in_summary: html += "</div>"
        if in_news: html += "</div>"
        if in_model: html += "</div>"
        html += f"<div class='footer'>{line}</div>"
        in_news = in_summary = in_model = False
    elif line and line[0].isdigit() and ("、" in line[:10] or "." in line[:10]):
        if in_news: html += "</div>"
        # 处理各种标题格式：1. **标题** / 1、标题 / 1. 标题
        if "**" in line:
            num_part, title_part = line.split("**", 1)
            num = num_part.strip().rstrip(".").rstrip("、")
            title = title_part.split("**", 1)[0].strip()
        elif "、" in line[:10]:
            num, title = line.split("、", 1)
        else:
            num, title = line.split(".", 1)
        html += f"<div class='news'><div class='news-title'>{num.strip()}、{title.strip()}</div>"
        in_news = True
    elif line.startswith("内容："):
        html += f"<div class='news-content'>{line[3:].strip()}</div>"
    elif line.startswith("来源："):
        html += f"<div class='news-source'>{line}</div></div>"
        in_news = False
    elif in_news and not line.startswith("内容：") and not line.startswith("来源："):
        html += f"<div class='news-content'>{line}</div>"
    elif in_summary or in_model:
        html += line + "<br>"

for flag in [in_news, in_summary, in_model]:
    if flag: html += "</div>"

html += "</body></html>"

# 发送测试邮件
from_addr = "letmerecoding@163.com"
password = "RERPuwtFqeidbnce"
to_addr = "18839139910@163.com"

msg = MIMEText(html, "html", "utf-8")
msg["From"] = Header(f"每日新闻摘要 <{from_addr}>", "utf-8")
msg["To"] = Header(to_addr, "utf-8")
msg["Subject"] = Header(f"【测试修复】{date_str} 重要新闻摘要", "utf-8")

try:
    server = smtplib.SMTP_SSL("smtp.163.com", 465)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    print("✅ 测试邮件发送成功，包含完整内容")
except Exception as e:
    print(f"❌ 邮件发送失败: {e}")
