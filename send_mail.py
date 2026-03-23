#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import sys
from datetime import datetime, timedelta

yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime("%Y-%m-%d")

def send_email(content):
    from_addr = "letmerecoding@163.com"
    password = "RERPuwtFqeidbnce"
    to_addr = "18839139910@163.com"
    smtp_server = "smtp.163.com"
    smtp_port = 465

    # 简洁Word风格排版，兼容所有邮箱
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: "宋体", "微软雅黑", SimSun, Arial, sans-serif; font-size: 14px; line-height: 1.5; color: #000; }}
            h1 {{ font-size: 16px; font-weight: bold; text-align: center; margin: 20px 0 10px 0; }}
            .meta {{ font-size: 12px; text-align: center; color: #666; margin-bottom: 20px; }}
            h2 {{ font-size: 15px; font-weight: bold; margin: 15px 0 8px 0; }}
            .news {{ margin: 10px 0 15px 2em; }}
            .news-title {{ font-weight: bold; margin-bottom: 5px; }}
            .news-content {{ margin-bottom: 5px; text-indent: 2em; }}
            .news-source {{ font-size: 12px; color: #666; }}
            .news-source a {{ color: #0000ff; text-decoration: underline; }}
            hr {{ border: 0; border-top: 1px solid #ccc; margin: 20px 0; }}
            .summary {{ margin: 15px 0; padding: 10px; border: 1px solid #ccc; background: #f9f9f9; }}
            .footer {{ font-size: 12px; color: #666; text-align: center; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>{date_str} 重要新闻摘要</h1>
        <div class="meta">整理时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
        <hr>
    """

    lines = content.split("\n")
    in_news = False
    in_summary = False

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith("## 一、") or line.startswith("## 二、") or line.startswith("## 三、") or line.startswith("## 四、") or line.startswith("## 五、"):
            if in_news:
                html += "</div>\n"
                in_news = False
            html += f"<h2>{line[3:]}</h2>\n"
        elif line.startswith("## 六、今日总结"):
            if in_news:
                html += "</div>\n"
                in_news = False
            html += "<h2>今日总结</h2>\n<div class='summary'>\n"
            in_summary = True
        elif line.startswith("---"):
            html += "<hr>\n"
        elif line.startswith("*以上"):
            if in_summary:
                html += "</div>\n"
                in_summary = False
            if in_news:
                html += "</div>\n"
                in_news = False
            html += f"<div class='footer'>{line}</div>\n"
        elif line and line[0].isdigit() and "、" in line[:5]:
            if in_news:
                html += "</div>\n"
            num, title = line.split("、", 1)
            html += f"<div class='news'><div class='news-title'>{num}、{title}</div>\n"
            in_news = True
        elif line.startswith("来源："):
            parts = line.split(" | ")
            if len(parts) == 2:
                source = parts[0].replace("来源：", "")
                url = parts[1]
                html += f"<div class='news-source'>来源：<a href='{url}' target='_blank'>{source}</a></div>\n"
            html += "</div>\n"  # 闭合当前新闻的div
            in_news = False
        elif in_news:
            html += f"<div class='news-content'>{line}</div>\n"
        elif in_summary:
            html += line + "<br>\n"

    # 最后检查并闭合所有未闭合的标签
    if in_news:
        html += "</div>\n"
    if in_summary:
        html += "</div>\n"

    html += """
    </body>
    </html>
    """

    msg = MIMEText(html, "html", "utf-8")
    msg["From"] = Header(f"每日新闻摘要 <{from_addr}>", "utf-8")
    msg["To"] = Header(to_addr, "utf-8")
    msg["Subject"] = Header(f"{date_str} 重要新闻摘要", "utf-8")

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        content = sys.argv[1]
    else:
        # 读取新闻文件
        with open(f"/Users/matianjun/.openclaw/workspace/news/{date_str}.md", "r", encoding="utf-8") as f:
            content = f.read()
    send_email(content)
