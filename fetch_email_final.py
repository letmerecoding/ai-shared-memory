#!/usr/bin/env python3
import imaplib
import email
from email.header import decode_header

# 配置
username = "letmerecoding@163.com"
password = "RERPuwtFqeidbnce"
imap_server = "imap.163.com"
imap_port = 993

print("连接IMAP服务器...")
mail = imaplib.IMAP4_SSL(imap_server, imap_port)

# 登录
print("正在登录...")
rv, data = mail.login(username, password)
print(f"登录结果: {rv}")

# 列出邮箱
print("列出邮箱...")
rv, data = mail.list()
print(f"list 结果: {rv}")
folders = []
for line in data:
    if line:
        parts = line.decode().split()
        if len(parts) >= 2:
            folder = parts[-1]
            folders.append(folder)
            print(f"  {folder}")

# 找收件箱
inbox_name = None
for f in folders:
    if "INBOX" in f.upper():
        inbox_name = f
        break
if not inbox_name:
    inbox_name = "INBOX"

print(f"使用收件箱: {inbox_name}")

# 选择收件箱
rv, data = mail.select(inbox_name, readonly=True)
print(f"选择 {inbox_name} 结果: {rv}")

if rv != "OK":
    print(f"选择收件箱失败: {rv}")
    mail.logout()
    exit(1)

# 搜索最新邮件
print("搜索全部邮件...")
rv, data = mail.search(None, "ALL")
print(f"搜索结果: {rv}")

if rv != "OK":
    print(f"搜索邮件失败: {rv}")
    mail.logout()
    exit(1)

# 获取最新邮件ID
message_ids = data[0].split()
if not message_ids:
    print("没有找到邮件")
    mail.logout()
    exit(0)

latest_id = message_ids[-1]
print(f"最新邮件ID: {latest_id}")

# 获取邮件
print("获取邮件...")
rv, data = mail.fetch(latest_id, "(RFC822)")
print(f"fetch 结果: {rv}")

if rv != "OK":
    print(f"获取邮件失败: {rv}")
    mail.logout()
    exit(1)

# 解析邮件
for response_part in data:
    if isinstance(response_part, tuple):
        msg = email.message_from_bytes(response_part[1])
        
        # 解码主题
        subject = ""
        for part, encoding in decode_header(msg["Subject"]):
            if isinstance(part, bytes):
                if encoding:
                    subject += part.decode(encoding)
                else:
                    subject += part.decode()
            else:
                subject += part
        print(f"\n📧 最新邮件主题: {subject}")
        print("-" * 50)
        
        # 获取正文
        body_found = False
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode()
                        print(body)
                        body_found = True
                        break
                    except Exception as e:
                        print(f"解码失败: {e}")
                        continue
        else:
            try:
                body = msg.get_payload(decode=True).decode()
                print(body)
                body_found = True
            except Exception as e:
                print(f"解码失败: {e}")

        if not body_found:
            print("（未能获取到正文内容）")

mail.logout()
print("-" * 50)
