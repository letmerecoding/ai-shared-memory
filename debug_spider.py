#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
}

yesterday = datetime.now() - timedelta(days=1)
date_str = yesterday.strftime("%Y-%m-%d")
print(f"调试日期：{date_str}")
print("="*50)

# 1. 调试澎湃新闻国内版
print("1. 调试澎湃新闻...")
try:
    res = requests.get("https://www.thepaper.cn/channel_97808", headers=headers, timeout=10)
    print(f"状态码：{res.status_code}")
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select(".news_li")[:3]
    print(f"抓取到新闻条数：{len(items)}")
    for i, item in enumerate(items):
        try:
            title = item.select_one("h2 a").text.strip()
            content = item.select_one(".news_txt").text.strip() if item.select_one(".news_txt") else title
            url = "https://www.thepaper.cn" + item.select_one("h2 a")["href"]
            time = item.select_one(".news_time").text.strip()
            print(f"新闻{i+1}：{title}")
            print(f"链接：{url}")
            print(f"时间：{time}")
            print("-"*30)
        except Exception as e:
            print(f"解析新闻{i+1}失败：{e}")
except Exception as e:
    print(f"澎湃新闻爬取失败：{e}")

print("\n" + "="*50)

# 2. 调试环球网国际新闻
print("2. 调试环球网国际新闻...")
try:
    res = requests.get("https://world.huanqiu.com/", headers=headers, timeout=10)
    print(f"状态码：{res.status_code}")
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select(".list_con h3 a")[:10]
    print(f"抓取到新闻条数：{len(items)}")
    count = 0
    for i, item in enumerate(items):
        try:
            title = item.text.strip()
            if any(keyword in title for keyword in ["冲突", "战争", "局势", "制裁", "军事"]) and count < 3:
                url = item["href"]
                print(f"新闻{count+1}：{title}")
                print(f"链接：{url}")
                count += 1
                print("-"*30)
        except Exception as e:
            print(f"解析新闻{i+1}失败：{e}")
except Exception as e:
    print(f"环球网爬取失败：{e}")

print("\n" + "="*50)

# 3. 调试东方财富网财经新闻
print("3. 调试东方财富网财经新闻...")
try:
    date_num = date_str.replace("-", "")
    url = f"https://finance.eastmoney.com/news/ccgn_{date_num}.html"
    res = requests.get(url, headers=headers, timeout=10)
    print(f"请求URL：{url}")
    print(f"状态码：{res.status_code}")
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select("#newsListContent li")[:3]
    print(f"抓取到新闻条数：{len(items)}")
    for i, item in enumerate(items):
        try:
            title = item.select_one("a").text.strip()
            url = item.select_one("a")["href"]
            time = item.select_one(".time").text.strip() if item.select_one(".time") else ""
            print(f"新闻{i+1}：{title}")
            print(f"链接：{url}")
            print(f"时间：{time}")
            print("-"*30)
        except Exception as e:
            print(f"解析新闻{i+1}失败：{e}")
except Exception as e:
    print(f"东方财富网爬取失败：{e}")

print("\n" + "="*50)

# 4. 调试36氪科技新闻
print("4. 调试36氪科技新闻...")
try:
    res = requests.get("https://36kr.com/information/technology", headers=headers, timeout=10)
    print(f"状态码：{res.status_code}")
    # 36氪用的是动态渲染，先试试找JSON数据
    script = re.search(r'window.__INITIAL_STATE__=(.*?);', res.text)
    if script:
        data = script.group(1)
        print("找到动态数据，解析中...")
        # 简单提取标题和链接
        items = re.findall(r'"title":"(.*?)".*?"permalink":"(.*?)"', data)[:3]
        print(f"抓取到新闻条数：{len(items)}")
        for i, (title, url) in enumerate(items):
            url = "https://36kr.com" + url
            print(f"新闻{i+1}：{title.encode('utf-8').decode('unicode_escape')}")
            print(f"链接：{url}")
            print("-"*30)
    else:
        soup = BeautifulSoup(res.text, "html.parser")
        items = soup.select(".article-item")[:3]
        print(f"抓取到新闻条数：{len(items)}")
        for i, item in enumerate(items):
            try:
                title = item.select_one(".article-title a").text.strip()
                url = "https://36kr.com" + item.select_one(".article-title a")["href"]
                print(f"新闻{i+1}：{title}")
                print(f"链接：{url}")
                print("-"*30)
            except Exception as e:
                print(f"解析新闻{i+1}失败：{e}")
except Exception as e:
    print(f"36氪爬取失败：{e}")

print("\n" + "="*50)

# 5. 调试丁香园医疗新闻
print("5. 调试丁香园医疗新闻...")
try:
    res = requests.get("https://dxy.com/news", headers=headers, timeout=10)
    print(f"状态码：{res.status_code}")
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select(".news-item")[:3]
    print(f"抓取到新闻条数：{len(items)}")
    for i, item in enumerate(items):
        try:
            title = item.select_one("a").text.strip()
            url = item.select_one("a")["href"]
            print(f"新闻{i+1}：{title}")
            print(f"链接：{url}")
            print("-"*30)
        except Exception as e:
            print(f"解析新闻{i+1}失败：{e}")
except Exception as e:
    print(f"丁香园爬取失败：{e}")
