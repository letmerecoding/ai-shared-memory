#!/usr/bin/env python3
from openai import OpenAI

# 配置
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
    api_key="31ae4db9-9313-45ef-9ec1-e2a6dd46069c"
)

# 测试生成新闻
print("测试生成新闻...")
prompt = """
请生成2023年3月9日的3条国内重大政策新闻，要求：
1. 每条包含标题、内容、来源、时间
2. 真实存在的新闻
3. 不要链接

格式：
1、【标题】
【内容】
来源：【来源】【时间】
"""

response = client.chat.completions.create(
    model="doubao-seed-2.0-pro",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
    max_tokens=1000
)

print("生成结果：")
print(response.choices[0].message.content)

# 测试验证
print("\n\n测试验证新闻...")
verify_prompt = f"""
请验证以下2023年3月9日的新闻是否真实：
{response.choices[0].message.content}

逐条验证，给出真实/不真实的结论。
"""

verify_response = client.chat.completions.create(
    model="glm-4.7",
    messages=[{"role": "user", "content": verify_prompt}],
    temperature=0.3,
    max_tokens=500
)

print("验证结果：")
print(verify_response.choices[0].message.content)
