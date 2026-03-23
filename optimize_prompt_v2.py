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

# 支持的任务类型，每个任务单独优化提示词
SUPPORTED_TASKS = {
    "news_daily": {
        "name": "新闻日报生成",
        "data_dir": "/Users/matianjun/.openclaw/workspace/news",
        "verify_file_suffix": "_verification.md",
        "prompt_file": "/Users/matianjun/.openclaw/workspace/news/prompt_optimization.json",
        "default_prompt": """
生成{date}的重要新闻：
1. 5个分类：国内政策、国际冲突、财经、科技、医疗，每类3条共15条
2. 每条格式：
序号、标题
内容
来源：名称 时间
3. 最后加200字总结
4. 不要任何链接，必须是{date}当天发布的真实新闻
"""
    }
    # 后续可以添加更多任务类型，比如邮件生成、文案撰写等
}

def load_task_config(task_type):
    """加载任务配置"""
    if task_type not in SUPPORTED_TASKS:
        raise ValueError(f"不支持的任务类型：{task_type}")
    config = SUPPORTED_TASKS[task_type]
    os.makedirs(config["data_dir"], exist_ok=True)
    return config

def load_weekly_data(task_config):
    """加载最近7天的任务数据"""
    weekly_data = []
    today = datetime.now()
    for i in range(7):
        date = today - timedelta(days=i+1)
        date_str = date.strftime("%Y-%m-%d")
        verify_file = os.path.join(task_config["data_dir"], f"{date_str}{task_config['verify_file_suffix']}")
        if os.path.exists(verify_file):
            with open(verify_file, "r", encoding="utf-8") as f:
                weekly_data.append({
                    "date": date_str,
                    "content": f.read()
                })
    return weekly_data

def analyze_task_errors(task_name, weekly_data):
    """分析特定任务的高频错误"""
    prompt = f"""
你是专业的提示词优化专家，现在分析【{task_name}】任务最近7天的验证报告：
1. 统计所有错误类型及出现次数，找出Top3高频错误
2. 针对每个高频错误给出具体的优化建议，要可落地、可写入提示词
3. 优化建议要直接针对错误根源，不要泛泛而谈

验证报告内容：
{json.dumps(weekly_data, ensure_ascii=False, indent=2)}

输出格式：
### 高频错误统计（{task_name}）
1. 错误类型1：X次
2. 错误类型2：X次
3. 错误类型3：X次

### 针对性优化建议
1. 【错误1】建议：xxx
2. 【错误2】建议：xxx
3. 【错误3】建议：xxx
"""
    
    response = client.chat.completions.create(
        model="ark-code-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1500
    )
    return response.choices[0].message.content.strip()

def optimize_task_prompt(task_name, analysis_result, current_prompt):
    """根据分析结果优化特定任务的提示词"""
    prompt = f"""
根据以下错误分析结果，优化【{task_name}】任务的生成提示词：
1. 把所有优化建议融入原提示词，用自然的语言表述
2. 保持原提示词的核心要求不变，只增加优化内容
3. 输出完整的优化后提示词，不要多余内容

原提示词：
{current_prompt}

错误分析结果：
{analysis_result}
"""
    
    response = client.chat.completions.create(
        model="ark-code-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1500
    )
    return response.choices[0].message.content.strip()

def load_task_prompt(task_config):
    """加载任务的提示词配置，不存在则初始化"""
    if os.path.exists(task_config["prompt_file"]):
        with open(task_config["prompt_file"], "r", encoding="utf-8") as f:
            return json.load(f)
    # 初始化
    return {
        "task_name": task_config["name"],
        "version": 1,
        "current_prompt": task_config["default_prompt"],
        "optimization_history": []
    }

def save_task_prompt(task_config, prompt_data):
    """保存任务的提示词配置"""
    with open(task_config["prompt_file"], "w", encoding="utf-8") as f:
        json.dump(prompt_data, f, ensure_ascii=False, indent=2)

def process_single_task(task_type):
    """处理单个任务的提示词优化"""
    print(f"\n{'='*60}")
    print(f"开始优化任务：{task_type}")
    
    # 加载配置
    config = load_task_config(task_type)
    task_name = config["name"]
    
    # 加载数据
    weekly_data = load_weekly_data(config)
    if not weekly_data:
        print(f"⚠️ {task_name}最近7天没有数据，跳过优化")
        return
    
    print(f"✅ 加载最近{len(weekly_data)}天的验证数据")
    
    # 加载当前提示词
    prompt_data = load_task_prompt(config)
    current_version = prompt_data["version"]
    current_prompt = prompt_data["generate_prompt"]
    
    # 分析错误
    print(f"🔍 分析{task_name}的高频错误...")
    analysis_result = analyze_task_errors(task_name, weekly_data)
    print("\n" + analysis_result + "\n")
    
    # 优化提示词
    print(f"✍️ 优化{task_name}的提示词...")
    new_prompt = optimize_task_prompt(task_name, analysis_result, current_prompt)
    print(f"原版本：v{current_version}")
    print(f"新提示词预览：\n{new_prompt[:300]}...\n")
    
    # 保存更新
    prompt_data["version"] += 1
    prompt_data["generate_prompt"] = new_prompt
    prompt_data["improvement_history"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "improvement": "根据最近4天错误分析自动优化提示词",
        "analysis": analysis_result,
        "old_prompt": current_prompt,
        "new_prompt": new_prompt,
        "accuracy_before": None,
        "accuracy_after": None
    })
    
    save_task_prompt(config, prompt_data)
    print(f"✅ {task_name}优化完成，新版本：v{prompt_data['version']}")

def main():
    print("🚀 开始每周多任务提示词优化")
    print(f"执行时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 处理所有支持的任务
    for task_type in SUPPORTED_TASKS:
        process_single_task(task_type)
    
    print(f"\n{'='*60}")
    print("🎉 所有任务优化完成！")

if __name__ == "__main__":
    main()
