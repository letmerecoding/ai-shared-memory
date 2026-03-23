#!/bin/bash
# 新闻收集脚本 - 每日自动获取前一天重要新闻

cd /Users/matianjun/.openclaw/workspace
# 生成新闻内容（现在先用模板，后面换大模型生成）
python3 fetch_news.py
# 发送邮件
python3 send_mail.py


