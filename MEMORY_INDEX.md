# 全局记忆框架索引

> **本文件是 `ai-shared-memory` 全局记忆框架的唯一入口。**
> 每次新会话、记忆维护、项目接入或规范更新前，必须先读取本文件，按索引加载对应文件。

---

## 🚨 启动必读（每次会话必须加载）

- **`rules.md`**：全局铁律、安全规则、Git 规则、OpenClaw 操作规范。所有操作前必读。
- **`profile.md`**：用户信息、交流偏好、重要长期偏好、全局仓库信息。
- **`workflow.md`**：记忆维护流程、先理解后执行机制、归档机制、渐进式开发工作流。
- **`CURRENT_DISCUSSION.md`**：当前讨论进度；若存在且非空，启动时读取以恢复上下文。

## 📁 项目与状态

- **`project_registry.md`**：已接入项目清单、路径说明、项目级记忆结构、同步规则。

## 📚 领域规范（按需加载）

| 触发关键词 / 场景 | 对应文件 |
| --- | --- |
| Java、Spring、接口测试、分支同步、查询优化、批量处理 | `categories/coding.md` |
| 架构设计、异步任务、轮询、冷热分离、版本控制、防越权、大模型 JSON 容错 | `categories/architecture.md` |
| OpenClaw、网关、配置、权限、卸载、使用问题 | `categories/openclaw-faq.md` |

## 📄 提示词模板（执行对应任务时加载）

| 任务 | 模板文件 |
| --- | --- |
| 渐进式代码开发（总体） | `prompts/code_dev_workflow.md` |
| 需求澄清 | `prompts/code_stage_1_requirement.md` |
| 架构设计 | `prompts/code_stage_2_design.md` |
| 代码骨架生成 | `prompts/code_stage_3_skeleton.md` |
| 细节实现 | `prompts/code_stage_4_implementation.md` |
| 代码审查 | `prompts/code_stage_5_review.md` |

> 说明：项目级 `.trae/prompts/dev_workflow/` 可按需引用这些全局模板；若项目索引中存在空的 `dev_workflow` 文件，应标注为“待补充”，不要假装已有内容。

## 🗄️ 全量备份与历史兼容

- **`MEMORY.md`**：全量备份文件 / 历史兼容文件，保留旧框架中的完整信息。
- 新架构入口以 **`MEMORY_INDEX.md`** 为准。
- 新增或更新记忆时，优先写入对应拆分文件；必要时再同步摘要到 `MEMORY.md`。

---

## 加载规则

1. **启动阶段**：先读本索引，再读取 `rules.md`、`profile.md`、`workflow.md` 和 `CURRENT_DISCUSSION.md`。
2. **项目相关**：涉及项目接入、同步、项目记忆结构时读取 `project_registry.md`。
3. **任务相关**：根据任务关键词读取 `categories/` 或 `prompts/` 对应文件。
4. **不确定时**：优先回到本索引，决定需要加载哪个文件。
5. **修改规则**：先检查差异、判断冲突、保留正确内容、只改目标文件；禁止直接覆盖无关内容。

---

## 更新记录

| 日期 | 更新内容 | 更新人 |
| --- | --- | --- |
| 2026-06-03 | feat(framework): 新增索引驱动拆分入口，明确 `MEMORY.md` 为全量备份文件，入口以 `MEMORY_INDEX.md` 为准 | OpenClaw |
