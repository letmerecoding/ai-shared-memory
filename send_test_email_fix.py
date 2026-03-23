#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 配置
from_addr = "letmerecoding@163.com"
password = "RERPuwtFqeidbnce"
to_addr = "18839139910@163.com"
smtp_server = "smtp.163.com"
smtp_port = 465

# 内容
content = """# 📊 每日记忆更新汇总 - 2026-03-23

## 一、今日更新内容汇总

### 1. 框架搭建完成
- ✅ 建立完整自动记忆提炼框架
- ✅ 完成多项目支持，每个项目独立维护 .trae/collaboration-memory.md
- ✅ 双层归档：总结版 + 完整原始对话版
- ✅ Git式更新流程：先diff检查差异 → 解决冲突 → 安全合并

### 2. 自动化工作流
- 每天 22:00：自动提炼更新记忆（本地完成）
- 每天 08:00：发送邮件汇总昨日更新
- 你手机邮件回复确认 → OpenClaw 拉取回复 → 执行推送GitHub
- 保留你的最终控制权，不会自动推送

### 3. 已接入项目
- /Users/matianjun/xiaoHongDev/pc_xiaohongzhujiao_plus/
- /Users/matianjun/xiaoHongMaster/pc_xiaohongzhujiao_plus/
- /Users/matianjun/sjth-cloud/
- /Users/matianjun/thProjects/
- /Users/matianjun/solo/

### 👉 请确认
如果你看到这封邮件，说明邮件收发正常。请直接回复这封邮件：
- 确认内容没问题，请回复「确认推送」
- 需要修改，请告诉我具体修改内容

---
*OpenClaw 自动生成*
"""

msg = MIMEText(content, "plain", "utf-8")
msg["From"] = Header("OpenClaw 记忆汇总 <letmerecoding@163.com>", "utf-8")
msg["To"] = Header("18839139910@163.com", "utf-8")
msg["Subject"] = Header("2026-03-23 记忆更新汇总，请确认", "utf-8")

try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    print("✅ 测试邮件发送成功！请检查 18839139910@163.com")
except Exception as e:
    print(f"❌ 发送失败: {e}")
