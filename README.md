# 共享长期记忆库

这是一个跨 AI 模型共享的长期记忆库，用于统一存储流程规范、用户偏好、项目登记、技术经验和工作规则。

---

## 当前框架：索引驱动拆分版

本仓库已经从“1 个大文件 + 多个小文件”的老框架，重构为：

```text
MEMORY_INDEX.md 作为唯一入口
MEMORY.md 作为全量备份 / 历史兼容文件
```

所有 AI 在开始对话、维护记忆、接入项目、更新规范前，应先读取 `MEMORY_INDEX.md`，再按索引加载对应文件。

---

## 目录结构

```text
ai-shared-memory/
├── MEMORY_INDEX.md          # 全局记忆框架唯一入口
├── MEMORY.md                # 全量备份 / 历史兼容文件，不再作为唯一入口
├── rules.md                 # 全局铁律、安全规则、Git规则、OpenClaw操作规范
├── profile.md               # 用户信息、交流偏好、重要长期偏好、仓库信息
├── workflow.md              # 记忆维护流程、归档机制、渐进式开发工作流
├── project_registry.md      # 已接入项目清单、项目级记忆结构、同步规则
├── CURRENT_DISCUSSION.md    # 当前讨论进度和共识
├── categories/              # 按领域分类的专业记忆
│   ├── coding.md
│   ├── architecture.md
│   └── openclaw-faq.md
├── prompts/                 # 提示词模板
│   ├── code_dev_workflow.md
│   ├── code_stage_1_requirement.md
│   ├── code_stage_2_design.md
│   ├── code_stage_3_skeleton.md
│   ├── code_stage_4_implementation.md
│   └── code_stage_5_review.md
└── memory/                  # 每日归档与历史记录
    └── YYYY-MM-DD.md
```

---

## 加载方式

1. 先读取 `MEMORY_INDEX.md`。
2. 启动必读：`rules.md`、`profile.md`、`workflow.md`、`CURRENT_DISCUSSION.md`。
3. 项目相关任务读取 `project_registry.md`。
4. 根据当前任务读取 `categories/` 或 `prompts/` 下对应文件。
5. `MEMORY.md` 仅作为全量备份和历史兼容，不作为新框架唯一入口。

---

## 维护规则

- 更新前先检查差异，不直接覆盖。
- 新增或修改通用规范后，判断是否需要同步到已接入项目。
- 只提交长期记忆相关文件，保持仓库干净。
- 禁止使用 `git add .`，只添加明确修改的文件。
- 推送远程前必须等待用户明确指令。

---

## 更新记录

| 日期 | 更新内容 | 更新人 |
| --- | --- | --- |
| 2026-06-03 | refactor(framework): 重构为索引驱动拆分版，明确 `MEMORY_INDEX.md` 为入口、`MEMORY.md` 为全量备份 | OpenClaw |
