# 项目登记与项目级记忆规范

> 本文件记录已接入项目、项目级记忆结构和全局/项目双向同步规则。

---

## 📁 已接入项目

| 项目代号 | 路径说明 | 状态 |
|---------|---------|------|
| 项目A | `{工作目录}/项目A/` | ✅ **活跃**，教师端班级管理功能开发完成，所有接口测试通过<br>2026-03-24 更新：完成类型变更、重名检查优化、关联关系修复<br>2026-03-25 更新：✅ 已初始化完整规范，创建 `.trae/collaboration-memory.md`，同步全局所有最新规则<br>2026-03-25 更新：✅ 完成 `getClassName` 接口同步，适配纯教师端权限过滤，只返回当前教师关联班级，按年级分组返回<br>2026-04-20 更新：✅ 完成PPT重新生成功能全流程开发（含代码重构、JSON嵌套兼容、历史会话存储、异步任务轮询架构改造）<br>2026-05-12 更新：✅ 新增无意义输入场景感知质检机制、大模型提示词优化教训总结、提交信息写法补充细则 |
| 项目A（分支2） | `{工作目录}/项目A/` | ✅ **活跃**，已初始化规范 |
| 项目B | `{工作目录}/项目B/` | ✅ **活跃**，已初始化规范 |
| 项目C | `{工作目录}/项目C/` | ✅ **活跃**，已初始化规范 |
| 项目D | `{工作目录}/项目D/` | ⛔ **已停用**（2026-10-20 确认不再使用）<br>原状态：已接入，OpenClaw + 火山方舟 Coding Plan 配置指南和常见问题整理<br>2026-03-24 更新：新增多个常见问题解答，包括权限错误、启动命令、配置向导网络错误、答非所问解决、新建会话方法、API配置说明、卸载教程 |
| 项目E（ms-courseware-service-hub） | `{工作目录}/项目E/` | ⛔ **已停用**（2026-07-28 接入，2026-10-20 确认停用，此次补充登记）<br>原状态：新项目初始化完成，创建 `.trae/collaboration-memory.md`，同步全局所有最新规范 |

> **当前活跃开发库：4 个**（项目A、项目A分支2、项目B、项目C）。
> 项目D、项目E 已停用，仅保留历史记录；"总-分-总"汇总下发循环仅针对活跃项目。

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
- **记忆自维护**：当日归档完成后（或用户指示"更新记忆"时），读取项目 `prompts/memory_update.md`，从归档中提炼信息更新对应记忆文件，并在 `project_state.md` 记录更新日期（铁律 20）
- **总-分-总循环**：用户指令驱动（现行机制，替代早期 OpenClaw 每日 22:00 定时任务）——读取各活跃项目记忆框架 → 汇总提取共性 → 更新总纲 → 下发最新框架回各项目
- **协作规范**：多个AI共同维护，随项目走，新窗口自动加载

---

## 项目级新记忆框架建议

参考 `xiaoHongDev/pc_xiaohongzhujiao_plus` 的拆分思想，项目级 `.trae/` 推荐采用：

```text
.trae/
├── MEMORY_INDEX.md              # 项目记忆唯一入口
├── rules.md                     # 项目强制规则与流程规范
├── project_state.md             # 当前项目状态、分支、活跃任务、近期决策
├── identity_and_workflow.md     # 做事方法、协作哲学、复盘机制
├── collaboration-memory.md      # 全量备份文件，入口仍以 MEMORY_INDEX.md 为准
├── experience/                  # 领域经验，按关键词触发加载
├── prompts/                     # 任务提示词模板
└── archive/                     # 双层对话归档
```

### 定位规则

- `MEMORY_INDEX.md` 是项目记忆入口。
- `collaboration-memory.md` 作为全量备份文件和历史兼容文件保留，不再作为唯一入口。
- `prompts/dev_workflow/` 若存在空文件，应在索引中明确标注"待补充"。
- 项目状态变化优先更新 `project_state.md`。
- 强制规则变化优先更新 `rules.md`。
- 技术经验优先写入 `experience/` 对应主题文件。

### 全局同步锚点机制

项目 `.trae/MEMORY_INDEX.md` 中的 `<!-- BEGIN GLOBAL_ARCHITECTURE_INDEX -->` ~ `<!-- END GLOBAL_ARCHITECTURE_INDEX -->` 注释区块，是"总→分"下发 `categories/architecture.md` 索引时的**同步锚点**：下发时只替换该区块内容，项目本地新增的条目（如项目A分支2的权限/SQL/Service 模式）写在区块外或本地 `experience/architecture.md` 中，不会被下发覆盖；回流时对比项目侧与总纲侧差异提取共性。

### 各项目当前结构状态（2026-10-20）

| 项目 | 记忆结构 | 维护状态 |
|------|---------|---------|
| 项目A（xiaoHongDev/pc_xiaohongzhujiao_plus） | **索引驱动拆分版**（MEMORY_INDEX + rules + project_state + identity_and_workflow + experience/×14 + prompts/ + archive/，最近一次记忆更新 2026-10-19） | 活跃，记忆最完整 |
| 项目A分支2（xiaoHongMaster/pc_xiaohongzhujiao_plus） | 单文件 + experience/architecture.md（本地多 3 个架构模式增量） | 活跃 |
| 项目B（sjth-cloud） | 单文件 + experience/architecture.md（含 Vue3/TS 前端规范本地章节） | 活跃 |
| 项目C（thProjects） | 单文件 + experience/architecture.md（标准下发版） | 活跃 |

---

## 💻 技术规范索引

| 分类 | 文件 | 说明 |
|------|------|------|
| 编码规范 | [categories/coding.md](categories/coding.md) | Java & Spring 规范、自检清单、接口测试、MyBatis/SQL 优化、前端 Vue3/TS 规范、类形态设计三问 |
| 架构设计 | [categories/architecture.md](categories/architecture.md) | 通用架构模式（异步任务、冷热分离、防越权、JSON 容错、权限双层可见性、SQL 幂等追加、服务权责分明等）|
| 故障排查 | [categories/openclaw-faq.md](categories/openclaw-faq.md) | OpenClaw 常见问题解答和故障排查指南 |
| 提示词文件 | [prompts/](prompts/) | 代码开发、需求分析等各类场景的提示词模板，渐进式代码开发工作流全套提示词 |
| 大模型交互 | 内嵌 | 大模型提示词优化教训、JSON解析容错方案、场景感知质检机制、提示词生命周期 |

---

## 更新记录

| 日期 | 更新内容 | 更新人 |
|------|---------|--------|
| 2026-06-03 | refactor(framework): 拆分已接入项目和项目级记忆结构规范到独立 project_registry 文件 | OpenClaw |
| 2026-10-20 | sync(registry): 确认四个活跃开发库（项目A、项目A分支2、项目B、项目C）；标记项目D（solo）、项目E（ms-courseware-service-hub）为已停用并补充项目E登记；明确总-分-总循环仅针对活跃项目 | Trae |
| 2026-10-20 | 总-分-总回流：新增"全局同步锚点机制"与"各项目当前结构状态"；"自动汇总"更新为指令驱动总-分-总循环 + 记忆自维护机制；技术规范索引描述同步更新 | Trae |
