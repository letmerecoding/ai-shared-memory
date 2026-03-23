#!/usr/bin/env python3
from openai import OpenAI

# 配置
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
    api_key="31ae4db9-9313-45ef-9ec1-e2a6dd46069c"
)

print("测试API调用...")
try:
    response = client.chat.completions.create(
        model="doubao-seed-2.0-lite",
        messages=[{"role": "user", "content": "你好，简单回复一句话就行"}],
        max_tokens=50,
        temperature=0.7
    )
    print("API调用成功！")
    print("返回结果：", response.choices[0].message.content.strip())
except Exception as e:
    print("API调用失败！")
    print("错误信息：", str(e))
