#!/usr/bin/env python3
"""
自动聊天机器人 - 模拟用户风格和他人聊天
使用方法：
1. 配置接入平台（微信/QQ/企业微信等）
2. 导入用户的聊天历史，学习用户聊天风格
3. 设置自动回复规则
"""
import os
import json
from datetime import datetime
from openai import OpenAI

# 配置
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
    api_key="31ae4db9-9313-45ef-9ec1-e2a6dd46069c",
    timeout=60.0,
)

# 配置文件路径
CONFIG_PATH = "/Users/matianjun/.openclaw/workspace/chat_config.json"
CHAT_HISTORY_PATH = "/Users/matianjun/.openclaw/workspace/chat_history/"
os.makedirs(CHAT_HISTORY_PATH, exist_ok=True)

def load_config():
    """加载聊天配置"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    # 默认配置
    default_config = {
        "user_style": """
        你的聊天风格：
        1. 语气轻松自然，像朋友一样聊天
        2. 回复简洁，不要太长
        3. 可以适当使用表情符号，不要太正式
        4. 符合日常聊天习惯，不要像机器人
        5. 不知道的就说不知道，不要瞎编
        """,
        "auto_reply_rules": [
            "工作时间（9:00-18:00）只回复重要消息",
            "休息时间可以正常聊天",
            "涉及敏感内容/转账/隐私问题直接拒绝回复",
            "不熟悉的人问隐私问题一律不回答"
        ],
        "special_rules": {
            "老板/客户": "回复要专业、礼貌，及时回应工作问题",
            "家人/朋友": "可以更随意，像平时聊天一样",
            "陌生人": "谨慎回复，不要透露个人信息"
        },
        "auto_reply_enabled": False,  # 默认关闭自动回复
        "notify_user": True  # 所有自动回复都会同步通知用户
    }
    save_config(default_config)
    return default_config

def save_config(config):
    """保存配置"""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def load_chat_history(contact):
    """加载和指定联系人的聊天历史"""
    history_file = os.path.join(CHAT_HISTORY_PATH, f"{contact}.json")
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_chat_history(contact, history):
    """保存聊天历史"""
    history_file = os.path.join(CHAT_HISTORY_PATH, f"{contact}.json")
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def generate_reply(contact, message, contact_type="朋友"):
    """生成自动回复"""
    config = load_config()
    history = load_chat_history(contact)
    
    # 构建提示词
    prompt = f"""
    你现在需要替用户回复消息，模拟用户的聊天风格。
    
    【用户聊天风格】：
    {config['user_style']}
    
    【联系人类型】：{contact_type}
    【联系人备注】：{contact}
    【对方发来的消息】：{message}
    
    【最近聊天历史】：
    {json.dumps(history[-10:], ensure_ascii=False) if history else '无'}
    
    【回复要求】：
    1. 严格按照用户的聊天风格回复
    2. 回复内容要符合上下文和聊天历史
    3. 不要暴露你是机器人，就像用户本人在聊天
    4. 回复不要太长，符合日常聊天习惯
    5. 如果是不适合自动回复的内容，就返回"[需要手动回复]"
    
    请直接输出回复内容，不要任何其他解释：
    """
    
    try:
        response = client.chat.completions.create(
            model="doubao-seed-code",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        reply = response.choices[0].message.content.strip()
        
        # 保存聊天记录
        history.append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "from": contact,
            "message": message,
            "reply": reply,
            "auto_generated": True
        })
        save_chat_history(contact, history)
        
        # 通知用户
        if config["notify_user"]:
            print(f"\n🔔 自动回复通知：")
            print(f"联系人：{contact}")
            print(f"对方消息：{message}")
            print(f"自动回复：{reply}")
            print("-"*50 + "\n")
        
        return reply
    except Exception as e:
        print(f"❌ 生成回复失败: {e}")
        return "[需要手动回复]"

def add_chat_history(contact, message, reply, is_user_reply=True):
    """手动添加聊天历史，用于学习用户风格"""
    history = load_chat_history(contact)
    history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "from": contact,
        "message": message,
        "reply": reply,
        "auto_generated": not is_user_reply
    })
    save_chat_history(contact, history)
    print(f"✅ 已添加和【{contact}】的聊天记录到学习库")

def update_user_style(new_style):
    """更新用户聊天风格"""
    config = load_config()
    config["user_style"] = new_style
    save_config(config)
    print("✅ 已更新聊天风格配置")

def toggle_auto_reply(enable=True):
    """开关自动回复"""
    config = load_config()
    config["auto_reply_enabled"] = enable
    save_config(config)
    print(f"✅ 自动回复已{'开启' if enable else '关闭'}")

if __name__ == "__main__":
    # 测试
    print("🤖 自动聊天机器人测试")
    print("="*50)
    
    # 示例：测试生成回复
    reply = generate_reply("张三", "周末要不要一起吃饭？", "朋友")
    print(f"测试回复：{reply}")
    
    print("\n💡 使用说明：")
    print("1. 先导入你和联系人的聊天历史，让AI学习你的风格")
    print("2. 配置自动回复规则和特殊联系人规则")
    print("3. 开启自动回复后，AI会自动替你回复消息")
    print("4. 所有自动回复都会同步通知你，你可以随时接管")
