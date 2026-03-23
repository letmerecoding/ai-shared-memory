#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime, timedelta
from openai import OpenAI

# 配置豆包API（火山引擎方舟）
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
    api_key="31ae4db9-9313-45ef-9ec1-e2a6dd46069c"
)
model = "volcengine-plan/ark-code-latest"

# 获取昨天的日期
yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime("%Y-%m-%d")
news_file = f"/Users/matianjun/.openclaw/workspace/news/{date_str}.md"

def load_news():
    """加载新闻文件"""
    with open(news_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 解析所有新闻标题
    news_items = []
    lines = content.split("\n")
    current_title = ""
    current_content = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 匹配新闻标题（数字、开头的行）
        if line and line[0].isdigit() and "、" in line[:5]:
            if current_title:
                news_items.append({
                    "title": current_title,
                    "content": current_content.strip()
                })
            num, title = line.split("、", 1)
            current_title = title
            current_content = ""
        elif line.startswith("来源："):
            continue
        elif current_title and not line.startswith("## "):
            current_content += line + " "
    
    if current_title:
        news_items.append({
            "title": current_title,
            "content": current_content.strip()
        })
    
    return news_items

def verify_news(news_item):
    """调用大模型验证新闻真实性和时效性"""
    prompt = f"""
请验证以下新闻的真实性和时效性：
标题：{news_item['title']}
内容：{news_item['content']}
发布日期应该是：{date_str}

请回答以下问题：
1. 这条新闻是否真实存在？
2. 发布时间是否符合{date_str}左右的时间范围？
3. 内容是否有明显错误或不实之处？

请用简洁的语言回答，每条新闻的验证结果控制在200字以内。
"""
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"验证失败：{str(e)}"

def main():
    print(f"开始验证{date_str}的新闻真实性...\n")
    news_items = load_news()
    
    results = []
    for i, item in enumerate(news_items, 1):
        print(f"正在验证第{i}条新闻：{item['title']}")
        result = verify_news(item)
        results.append({
            "index": i,
            "title": item['title'],
            "verification": result
        })
        print(f"验证结果：{result}\n")
    
    # 保存验证结果
    output_file = f"/Users/matianjun/.openclaw/workspace/news/{date_str}_verification.md"
    content = f"# {date_str} 新闻真实性验证报告\n\n"
    content += f"验证时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for res in results:
        content += f"## 第{res['index']}条：{res['title']}\n"
        content += f"{res['verification']}\n\n"
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"验证完成，结果已保存到：{output_file}")

if __name__ == "__main__":
    main()
