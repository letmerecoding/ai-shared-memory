#!/usr/bin/env python3
import os
from datetime import datetime, timedelta
from openai import OpenAI

# 配置
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
    api_key="31ae4db9-9313-45ef-9ec1-e2a6dd46069c"
)
generate_model = "doubao-seed-2.0-pro"  # 生成新闻用的模型
verify_model = "doubao-seed-2.0-pro"    # 验证新闻用的模型
output_dir = "/Users/matianjun/.openclaw/workspace/news"
os.makedirs(output_dir, exist_ok=True)

# 获取昨天的日期
yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime("%Y-%m-%d")

def generate_news():
    """通过大模型生成前一天的新闻日报"""
    prompt = f"""
请生成2023年3月9日的重要新闻日报，要求如下：
1. 分为5个分类：国内重大政策、国际区域冲突、财经新闻、科技突破、生物医疗进展
2. 每个分类3条新闻，共15条
3. 每条新闻包含：标题、内容、发布时间、来源
4. 不需要附带任何新闻链接
5. 所有新闻必须是2023年3月9日当天发布的真实存在的新闻，内容必须符合事实
6. 格式严格按照以下Markdown格式：

## 一、国内重大政策
1、【新闻标题】
【新闻内容】
来源：【来源名称】 【发布时间】

## 二、国际区域冲突
4、【新闻标题】
【新闻内容】
来源：【来源名称】 【发布时间】

以此类推，最后加上今日总结。
"""
    
    response = client.chat.completions.create(
        model=generate_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=4000
    )
    return response.choices[0].message.content.strip()

def verify_news(news_content):
    """调用另一个大模型验证每条新闻的真实性"""
    prompt = f"""
请验证以下2023年3月9日的新闻日报中每条新闻的真实性，要求：
1. 逐条验证每条新闻的：发生时间、新闻主题、内容真实性
2. 对每条新闻给出验证结果：真实/不真实，以及简要说明
3. 格式：每条新闻对应一条验证结果，清晰明了

新闻内容：
{news_content}
"""
    
    response = client.chat.completions.create(
        model=verify_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=3000
    )
    return response.choices[0].message.content.strip()

def save_news(content, verification):
    """保存新闻和验证结果"""
    # 保存新闻日报
    news_file = os.path.join(output_dir, f"{date_str}.md")
    with open(news_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"新闻日报已保存：{news_file}")
    
    # 保存验证结果
    verify_file = os.path.join(output_dir, f"{date_str}_verification.md")
    with open(verify_file, "w", encoding="utf-8") as f:
        f.write(f"# {date_str} 新闻真实性验证报告\n\n")
        f.write(f"验证时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(verification)
    print(f"验证报告已保存：{verify_file}")
    
    return news_file

def send_email(news_file):
    """发送邮件（沿用之前的Word风格排版）"""
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header
    
    from_addr = "letmerecoding@163.com"
    password = "RERPuwtFqeidbnce"
    to_addr = "18839139910@163.com"
    smtp_server = "smtp.163.com"
    smtp_port = 465
    
    # 读取新闻内容
    with open(news_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 构建HTML邮件（Word风格，无链接）
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
            html += f"<div class='news-source'>{line}</div>\n"
            html += "</div>\n"
            in_news = False
        elif in_news:
            html += f"<div class='news-content'>{line}</div>\n"
        elif in_summary:
            html += line + "<br>\n"
    
    # 闭合未闭合的标签
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

def main():
    print(f"开始生成{date_str}的新闻日报...")
    news_content = generate_news()
    print("新闻生成完成，开始验证真实性...")
    verification = verify_news(news_content)
    print("验证完成，保存文件...")
    news_file = save_news(news_content, verification)
    print("开始发送邮件...")
    send_email(news_file)
    print("全部流程完成！")

if __name__ == "__main__":
    main()
