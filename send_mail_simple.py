#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from datetime import datetime, timedelta

yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime("%Y-%m-%d")

def send_email():
    from_addr = "letmerecoding@163.com"
    password = "RERPuwtFqeidbnce"
    to_addr = "18839139910@163.com"
    smtp_server = "smtp.163.com"
    smtp_port = 465

    # 纯文本格式，没有任何样式，字体大小完全统一
    with open(f"/Users/matianjun/.openclaw/workspace/news/{date_str}.md", "r", encoding="utf-8") as f:
        content = f.read()

    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = Header(f"每日新闻摘要 <{from_addr}>", "utf-8")
    msg["To"] = Header(to_addr, "utf-8")
    msg["Subject"] = Header(f"{date_str} 重要新闻摘要", "utf-8")

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()
        print("纯文本邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")

if __name__ == "__main__":
    send_email()
