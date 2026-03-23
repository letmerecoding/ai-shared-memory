#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime, timedelta

yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime("%Y-%m-%d")

with open(f"/Users/matianjun/.openclaw/workspace/news/{date_str}.md", "r", encoding="utf-8") as f:
    content = f.read()

msg = MIMEText(content, "plain", "utf-8")
msg["From"] = Header("每日新闻摘要 <letmerecoding@163.com>", "utf-8")
msg["To"] = Header("18839139910@163.com", "utf-8")
msg["Subject"] = Header(f"{date_str} 重要新闻摘要", "utf-8")

server = smtplib.SMTP_SSL("smtp.163.com", 465)
server.login("letmerecoding@163.com", "RERPuwtFqeidbnce")
server.sendmail("letmerecoding@163.com", ["18839139910@163.com"], msg.as_string())
server.quit()
print("发送成功，内容和源文件完全一致")
