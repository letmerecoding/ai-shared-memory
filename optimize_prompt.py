#!/usr/bin/env python3
import os
import json
from datetime import datetime, timedelta
from openai import OpenAI

# 配置
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
    api_key="31ae4db9-9313-45ef-9ec1-e2a6dd46069c",
    timeout=60.0
)

# 文件路径
STATS_FILE = "/Users/matianjun/.openclaw/workspace/news/model_stats.json"
PROMPT_FILE = "/Users/matianjun/.openclaw/workspace/news/prompt_optimization.json"
NEWS_DIR = "/Users/matianjun/.openclaw/workspace/news"

def load_weekly_data():
    """加载最近7天的验证数据"""
    weekly_data = []
    today = datetime.now()
    for i in range(7):
        date = today - timedelta(days=i+1)
        date_str = date.strftime("%Y-%m-%d")
        verify_file = os.path.join(NEWS_DIR, f"{date_str}_verification.md")
        if os.path.exists(verify_file):
            with open(verify_file, "r", encoding="utf-8") as f:
                weekly_data.append({
                    "date": date_str,
                    "content": f.read()
                })
    return weekly_data

def analyze_weekly_errors(weekly_data):
    """分析最近7天的错误类型，统计高频错误"""
    prompt = f"""
分析最近7天的新闻验证报告，统计高频错误类型：
1. 统计每种错误出现的次数：时间错误、地点错误、事件不实、内容错误、来源错误等
2. 给出Top3最常见的错误类型
3. 针对每种高频错误给出具体的优化建议

验证报告内容：
{json.dumps(weekly_data, ensure_ascii=False, indent=2)}

输出格式：
### 高频错误统计
1. 错误类型1：X次
2. 错误类型2：X次
3. 错误类型3：X次

### 优化建议
1. 针对错误1的具体建议
2. 针对错误2的具体建议
3. 针对错误3的具体建议
"""
    
    response = client.chat.completions.create(
        model="ark-code-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

def update_prompt(analysis_result, current_prompt):
    """根据分析结果更新生成提示词"""
    prompt = f"""
根据以下错误分析结果，优化新闻生成提示词，把优化建议融入原提示词中，让生成的新闻准确率更高：

原提示词：
{current_prompt}

错误分析结果：
{analysis_result}

输出优化后的完整提示词，不要多余内容。
"""
    
    response = client.chat.completions.create(
        model="ark-code-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

def main():
    print("🚀 开始每周提示词优化任务")
    print(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 加载数据
    weekly_data = load_weekly_data()
    if not weekly_data:
        print("⚠️ 最近7天没有验证数据，跳过优化")
        return
    
    print(f"✅ 加载最近{len(weekly_data)}天的验证数据")
    
    # 加载当前提示词
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        prompt_data = json.load(f)
    current_prompt = prompt_data["generate_prompt"]
    current_version = prompt_data["version"]
    
    # 分析错误
    print("🔍 分析高频错误...")
    analysis_result = analyze_weekly_errors(weekly_data)
    print("\n" + analysis_result + "\n")
    
    # 优化提示词
    print("✍️ 优化提示词...")
    new_prompt = update_prompt(analysis_result, current_prompt)
    print(f"原提示词版本：v{current_version}")
    print(f"新提示词预览：{new_prompt[:200]}...\n")
    
    # 保存更新
    prompt_data["version"] += 1
    prompt_data["generate_prompt"] = new_prompt
    prompt_data["improvement_history"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "type": "weekly_optimization",
        "analysis": analysis_result,
        "old_prompt": current_prompt,
        "new_prompt": new_prompt
    })
    
    with open(PROMPT_FILE, "w", encoding="utf-8") as f:
        json.dump(prompt_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 提示词优化完成，新版本：v{prompt_data['version']}")
    print("🎉 每周优化任务执行完成！")

if __name__ == "__main__":
    main()
