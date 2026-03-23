# MEMORY.md - 长期记忆仓库

这是长期记忆仓库，用来存放从每日对话中提炼出来的、有长期保留价值的信息。

## 用户信息

- 用户称呼：大哥
- 时区：Asia/Shanghai

## 重要决策与偏好

- 用户每天需要和多个大模型对话，希望建立自动记忆提炼机制：每日对话归档 → 自动汇总提炼 → 存入长期记忆仓库
- 偏好：轻松随意的交流风格，像朋友一样聊天

## OpenClaw 操作规范（新增规则）

| # | 规则 |
|---|---|
| 1 | **当用户告知一个项目路径时**，都需要检查这个项目下是否有长期记忆文件，如果没有则以 `.trae/collaboration-memory.md` 的格式创建一份整理好的最新规范模板 |
| 2 | **当新增一条通用规范时**：<br>(1) 判断是否需要将这个长期记忆更新到用户已提供的所有项目下，并做适应性改造<br>(2) 如果判断无需更新到所有项目，需要明确告知同步到了哪些路径，并说明理由 |
| 3 | 项目规范遵循：每个项目独立维护 `.trae/collaboration-memory.md`，随项目走，OpenClaw 双向同步核心信息到全局统一记忆仓库 |
| 4 | **更新记忆文件的完整流程（Git式）**：<br>1. **先检查差异**：读取现有文件内容，对比将要更新的内容，找出差异<br>2. **判断冲突**：有冲突解决冲突，无冲突则安全合并<br>3. **不随便覆盖**：保留原有正确内容，只新增或修改有差异的部分<br>4. **提交信息规范**：格式遵循 `type(scope): 标题概括改动`，正文分条描述修改，更新记录表必须记录本次更新 |

## 项目与工作

### 每日新闻推送项目
- 每天10点定时发送新闻邮件
- 要求：无链接、纯文本、大模型生成内容需要另一个大模型验证真实性
- 最终脚本：`news_daily_final.py`
- 模型速度排序：deepseek-v3.2 (最快) > ark-code-latest > doubao-seed-code > doubao-seed-2.0-code > glm-4.7 > kimi-k2.5
- 关键问题修复：HTML标签闭合问题导致邮件嵌套，已修复

### 智能作文批改系统
- 已经完成需求文档
- 完成教师端Figma原型设计

### 已接入自动记忆汇总的项目列表

| 项目名称 | 项目地址 | 状态 |
|---------|---------|------|
| pc_xiaohongzhujiao_plus (小红猪加分教师端) | `/Users/matianjun/xiaoHongDev/pc_xiaohongzhujiao_plus/` | ✅ 已接入，已有开发内容 |
| pc_xiaohongzhujiao_plus | `/Users/matianjun/xiaoHongMaster/pc_xiaohongzhujiao_plus/` | ✅ 已初始化规范 |
| sjth-cloud | `/Users/matianjun/sjth-cloud/` | ✅ 已初始化规范 |
| thProjects | `/Users/matianjun/thProjects/` | ✅ 已初始化规范 |
| solo | `/Users/matianjun/solo/` | ✅ 已接入，已有OpenClaw配置调试经验 |

### 统一记忆结构（所有项目共用）
- **长期规范**：`.trae/collaboration-memory.md`（提炼后的协作规范和项目记忆）
- **每日归档**：
  - `.trae/archive/YYYY-MM-DD.md` - 整理总结版（提炼核心，方便快速查阅）
  - `.trae/archive/YYYY-MM-DD-full.md` - 完整原始归档（逐轮完整记录所有对话）
- **完整归档规范**：
  - 禁止总结、缩写、合并重复对话
  - 按时间顺序逐轮记录，一轮都不能少
  - 完整保留每轮原话，格式清晰区分用户和AI
  - 存档后必须自查轮次，确保完整
- **自动汇总**：OpenClaw 每日 22:00 自动读取各项目当日归档，提炼更新长期记忆，去重合并不新增重复内容
- **协作规范**：多个AI共同维护，随项目走，新窗口自动加载

### pc_xiaohongzhujiao_plus (小红猪加分教师端) - xiaoHongDev
- 项目地址：`/Users/matianjun/xiaoHongDev/pc_xiaohongzhujiao_plus/`
- 2026-03-23 开发完成：
  - 新增根据学段获取年级选项接口 `GET /schoolInfo/class/grades/{phase}`
  - 优化班级分页查询，增加教师权限过滤（只返回当前教师关联班级）
  - 修复班级创建问题：允许 `schoolId` 为 `null` 插入
  - 验证并确定了完整对话归档规范
  - 所有接口测试通过，开发完成

## 技术偏好

- **项目级AI协作规范**：项目内 `.trae/` 目录存放记忆，长期规范 + 双层按日归档，多个AI共同维护
- **完整归档要求**：必须保存完整原始对话，才能保证档案可追溯，不丢失有价值信息
- **自动汇总机制**：OpenClaw 每日自动从各项目归档提炼，更新长期记忆，双向同步去重
- ...（后续会不断补充）
