#!/usr/bin/env python3
import imaplib

username = "letmerecoding@163.com"
password = "RERPuwtFqeidbnce"
imap_server = "imap.163.com"
imap_port = 993

mail = imaplib.IMAP4_SSL(imap_server, imap_port)
rv, data = mail.login(username, password)
print(f"login: {rv}")

rv, data = mail.list()
print(f"list: {rv}")
for line in data:
    if line:
        print(line.decode())

mail.logout()
