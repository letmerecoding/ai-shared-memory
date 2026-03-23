#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

date_str = datetime.now().strftime("%Y-%m-%d")

# 邮件配置
from_addr = "letmerecoding@163.com"
password = "RERPuwtFqeidbnce"
to_addr = "18839139910@163.com"
smtp_server = "smtp.163.com"
smtp_port = 465

# 邮件内容
content = """# 📊 每日记忆更新汇总 - %s

## 一、全局框架更新

### 🎯 新增机制：OpenClaw 自动记忆提炼框架
- 完成自动记忆提炼机制设计和配置
- 核心流程：每日对话归档 → 定时任务自动汇总 → 提炼长期价值信息 → 更新全局记忆和各项目规范
- 遵循用户要求：**保存完整原始对话保证可追溯性**，不丢失任何信息

### 📝 MEMORY.md 重构更新
- 重新组织分类结构，增加清晰目录导航
- 新增 OpenClay 操作规范，明确记忆文件更新流程：**先检查差异 → 判断冲突 → 安全合并 → 不随便覆盖**
- 新增已接入项目清单记录，统一维护项目路径和状态
- 更新记录新增今日重构和框架完善两条提交

## 二、多项目规范同步更新

### ✅ 已完成同步的项目：

1. **pc_xiaohongzhujiao_plus (开发目录)** /Users/matianjun/xiaoHongDev/pc_xiaohongzhujiao_plus/
   - 新增文档维护规则，明确文档存放于项目 .trae/ 目录随项目走
   - 新增对话归档规则：双层归档结构（总结版 + 完整原始版）
   - 补充完整对话归档提示词规范模板，确保完整性
   - 新增记忆文件更新提交规范，要求遵循 Git 提交信息格式
   - 完善 Git 式更新流程，先检查差异再合并，解决冲突不随便覆盖

2. **pc_xiaohongzhujiao_plus (主目录)** /Users/matianjun/xiaoHongMaster/pc_xiaohongzhujiao_plus/
   - 初始化完整协作规范文档
   - 同步最新的归档规则、提交规范、更新流程

3. **sjth-cloud** /Users/matianjun/sjth-cloud/
   - 初始化完整协作规范文档
   - 同步最新规则

4. **thProjects** /Users/matianjun/thProjects/
   - 初始化完整协作规范文档，适配项目通用开发场景调整内容
   - 同步最新规则

5. **solo** /Users/matianjun/solo/
   - 在现有 OpenClay 配置指南基础上，补充完整对话归档规范
   - 同步最新的记忆更新提交规范和 Git 式更新流程

## 三、开发工作进展（pc_xiaohongzhujiao_plus）

### ✅ 今日完成功能开发：
- 新增接口 GET /schoolInfo/class/grades/{phase} 根据学段获取年级选项
- 修改分页查询，通过 teacher_class_rel 查询当前教师关联班级，实现权限过滤
- 修改名称重复校验，schoolId 为 null 时不添加条件
- 修改创建班级逻辑，schoolId 为 null 时允许插入
- 给 create 方法添加 @Transactional 事务保证一致性
- 更新服务层接口定义

### ✅ 所有接口测试通过：
| 接口 | 结果 |
|------|------|
| GET /schoolInfo/class/options | ✅ 通过 |
| GET /schoolInfo/class/grades/{phase} | ✅ 通过 |
| POST /schoolInfo/class/checkName | ✅ 通过 |
| POST /schoolInfo/class/create | ✅ 通过 |
| POST /schoolInfo/class/pageList | ✅ 通过 |

**当前状态**：需求功能全部实现，测试全部通过，文档整理归档完成

## 四、📊 本次更新统计

| 分类 | 更新文件数 | 说明 |
|------|---------|---------|
| 框架重构 | 1 | MEMORY.md 整体重构分类 |
| 规则新增 | 1 | core/rules.md 新增完整归档规范和邮件工作流 |
| 项目整理 | 1 | 整理已接入项目清单 |
| 决策记录 | 1 | 记录自动记忆机制需求和用户偏好 |
| 项目同步 | 5 | 五个项目都同步了最新规范 |
| **合计** | **9** | **首次整理初始化完成** |

## 📌 本次更新核心要点

1. **建立了完整的自动化记忆框架**：
   - 每日对话归档 → 自动提炼 → 邮件汇总 → 用户确认 → GitHub推送 全流程

2. **明确了归档规则**：
   - 双层归档结构，总结版方便查阅，完整版保存完整原始对话
   - 强制要求逐轮完整保留，禁止总结缩写遗漏
   - Git式更新流程：先diff检查差异，有冲突解决冲突再合并

3. **多项目支持**：
   - 每个项目独立维护 .trae/collaboration-memory.md
   - OpenClaw 双向同步核心信息到全局 MEMORY.md
   - 解决了IDE插件越权问题，记忆文件放在项目内

4. **工作流设计**：
   - 自动提炼更新只在本地完成
   - 每日发邮件汇总，用户确认后再推送到GitHub
   - 保留用户最终控制权，避免误提交

---

## 👉 待操作

以上就是今天所有更新内容，请确认：
- 如果内容没问题，请回复「确认推送」，我会提交并推送到GitHub
- 如果需要修改或补充，请告诉我具体修改内容

---
*自动生成于 %s (Asia/Shanghai)*
""" % (date_str, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

msg = MIMEText(content, "plain", "utf-8")
msg["From"] = "OpenClaw 记忆汇总 <letmerecoding@163.com>"
msg["To"] = "18839139910@163.com"
msg["Subject"] = "%s 记忆更新汇总，请确认" % date_str

try:
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    print("✅ 测试邮件发送成功，请检查邮箱 18839139910@163.com")
except Exception as e:
    print(f"❌ 邮件发送失败: {e}")
