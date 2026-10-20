# 架构设计与开发模式规范

本文件汇总从实际项目开发中提炼的通用架构设计模式、编码规范和最佳实践。

---

## 📋 目录

- [🔴 技术架构模式](#-技术架构模式)
- [🟠 编码与设计规范](#-编码与设计规范)
- [🟡 常见问题速查](#-常见问题速查)
- [🟢 权限与授权体系设计](#-权限与授权体系设计)

---

## 🔴 技术架构模式

### 1. 异步任务轮询架构设计模式

**适用场景**：长耗时操作（大模型生成、文件处理、批量任务等）

**架构流程**：
```
用户请求 → 创建任务记录(status=0, progress=0) → 立即返回taskId → 前端轮询 → 后端异步执行并更新进度 → 完成(status=1, progress=100)
```

**数据库表设计核心字段**：
| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | TINYINT | 任务状态：0-执行中，1-已完成，2-异常 |
| `progress` | INT | 进度百分比 0-100 |
| `message` | VARCHAR(500) | 状态消息/错误信息 |
| `content` | LONGTEXT | 最终结果（完成后才保存） |

**进度更新策略**：分阶段更新，每完成一个里程碑更新一次
| 阶段 | progress | message |
|------|----------|---------|
| 开始核心处理 | 10 | 正在处理... |
| 核心处理完成 | 30 | 核心处理完成，开始后续步骤 |
| 中间步骤完成 | 50 | 中间步骤完成 |
| 最终处理 | 50→90 | 处理中 X/Y |
| 全部完成 | 100 | 处理完成 |

**安全要点**：查询任务时必须加上用户标识过滤（如`openId = loginUser.openid`），防止越权访问

---

### 1.1 实战扩展：PPT重新生成异步任务完整架构

**适用场景**：大模型多步骤生成任务（PPT、文档、多图片批量生成等）

**架构特点**：三模型分工 + 并行图片生成 + SSE返回taskId + 前端轮询

**完整流程**：
```
用户请求重新生成
    ↓
创建 TDialogueAttachment 记录 → status=0, progress=0
    ↓
通过 SSE 返回 taskId 给前端 → SSE关闭
    ↓
前端轮询 GET /ai/pptRegenerate/task/{taskId}
    ↓
后端异步执行 → 实时更新 progress 到数据库
    ↓
完成 → status=1, progress=100 → 前端获取 content 渲染PPT
失败 → status=2 → 前端显示错误信息
```

**进度更新规则（多阶段任务）**：
| 阶段 | progress | message |
|------|----------|---------|
| 开始大模型A生成内容 | 10 | 正在生成PPT内容 |
| 大模型A生成完成 | 30 | PPT内容生成完成，开始分析配图 |
| 大模型B分析完成 | 50 | 配图分析完成，开始生成图片 |
| 每生成一页 | 50→90 | 已生成 X/Y 页 |
| 全部完成 | 100 | 生成完成 |

**版本号控制**：
- operateType=1（整个PPT重新生成）→ 每次版本号+1
- operateType=2（单页重新生成）→ 版本号不变
- 版本号计算逻辑：只统计 operateType=1 的记录数，而不是 MAX(version)

**超时处理机制**：
- 定时任务：每5分钟扫描一次
- 超时阈值：30分钟
- 处理逻辑：status=0 且创建时间超过30分钟 → 标记为 status=2，设置消息"生成超时，请重试"
- 环境过滤：dev环境不执行

**涉及组件复用**：
- TDialogueAttachmentService：会话附件服务，自动处理版本号
- TDialogueAttachment 实体：任务状态和结果存储
- 已存在的轮询接口：AiController / getPptRegenerateTask
- 已存在的VO：PptRegenerateTaskVO

---

### 2. 冷热数据分离架构模式

**适用场景**：Redis内存优化、大对象存储、会话历史等冷热数据分明的场景

**核心思想**：热数据（索引、引用）存Redis追求速度，冷数据（完整内容）存MySQL追求容量和一致性

**完整架构**：

| 层级 | 存储介质 | 存储内容 | 数据大小 | 查询频率 |
|------|---------|---------|---------|---------|
| **热数据层** | Redis | 只存引用标记 `{"type":"ppt_task","taskId":"xxx"}` | ~50字节 | 极高 |
| **冷数据层** | MySQL | 完整的status、content、progress、version、operateType等元数据 | 几十KB到几MB | 较低 |

**写入流程**：
```
用户请求 → 主线程第0秒立即写入Redis（只存taskId引用）
    ↓
异步线程开始执行 → 只更新MySQL，不更新Redis
    ↓
异步完成 → 更新MySQL的status、progress、content等字段
```

**查询流程**：
```
前端请求会话历史 → 从Redis获取会话列表
    ↓
识别所有 ppt_task 标记，收集taskId列表
    ↓
批量查询MySQL t_dialogue_attachment 表获取元数据
    ↓
组装完整会话列表返回给前端
```

**核心收益**：
- ✅ Redis内存占用降低 99%+（从几十KB降到约50字节）
- ✅ 用户体验好：异步任务开始就能在历史记录中看到
- ✅ 完全兼容旧数据：旧的完整JSON存储方式自动兼容
- ✅ 数据一致性好：MySQL是最终数据源，Redis只存引用

**返回格式设计**：
```json
// PPT类型对话，content只返回taskId
{
  "content": "{\"taskId\": \"123456\"}",
  "type": "pptReload",
  "operatorType": 1
}
```

---

### 3. API防越权访问设计规范

**问题场景**：用户可能通过修改ID参数访问他人数据（如taskId、fileId、userId等）

**解决方案**：
- 所有涉及用户私有数据的查询接口，查询条件必须包含用户标识过滤
- 示例：`queryWrapper.eq("open_id", loginUser.getOpenid())`
- 不仅要校验登录状态，还要校验数据归属权

---

## 🟠 编码与设计规范

### 4. 版本号控制策略设计

**适用场景**：需要区分不同操作类型对版本号的影响

**策略原则**：
| 操作类型 | 版本变更 | 说明 |
|----------|---------|------|
| 重大变更（整个资源重新生成） | 版本号+1 | 每次都产生新版本 |
| 局部修改（单页/单项修改） | 版本号不变 | 保持当前版本 |

**实现方式**：Service层根据`operateType`自动计算版本号，对外屏蔽细节

---

### 5. 大模型输出JSON解析容错方案

**根本方案（优先）：不让模型输出 JSON**——JSON 解析失败的根本原因是模型不擅长输出精确的结构化数据。与其加多层容错，不如从源头消除问题：让模型只输出纯文本/HTML，由代码做模板替换（模型擅长语义与内容生成，代码擅长精确的字符串操作）。

**防御性方案：JSON 前预清理**——无法避免模型输出 JSON 时，parse 前 regex 清理可能破坏语法的内容（如 LaTeX 命令 `\boldsymbol{}`、`\text{}`）。

**嵌套兼容**：大模型偶尔会将实际 JSON 多嵌套一层在 `value` 字段中，解析时需兼容：
```java
JSONObject jsonObject = JSON.parseObject(jsonString);
// 兼容大模型返回的嵌套结构
if (jsonObject.containsKey("value") && jsonObject.get("value") instanceof JSONObject) {
    jsonObject = jsonObject.getJSONObject("value");
}
```

**降级容错**：解析失败时使用原始文本兜底（如标题降级为"第N页"、正文用原始文本），不让单点解析失败中断整个流程。

**Markdown 包裹清理**：模型输出常包裹在 ```json ... ``` 或前后说明文字中，解析前先去掉代码块标记、提取第一个 `{` 到最后一个 `}` 之间的内容；必须添加调试日志打印原始输出和清理后的 JSON。

**适用范围**：所有与大模型交互的 JSON 解析场景

---

### 6. 代码重构消除重复代码实践

**提取公共方法的原则**：
- 相同逻辑出现2次以上考虑提取
- 提取的方法应该具有独立完整的语义
- 方法命名清晰表达其用途

**重构收益示例**：
- 提取前：~140行重复代码（两处）
- 提取后：~80行公共方法 + ~20行调用 = 净减少~40行
- 附带收益：调用处自动获得公共方法的所有能力（如JSON清理、超时配置等）

**公共方法示例**：
```java
// 统一流式调用大模型，返回清理后的JSON
private String callDouBaoModelStream(List<ChatMessage> chatMessages, int maxTokens)

// 统一分析配图需求并处理图片
private boolean analyzeAndProcessPageImages(String pagesJson, String userRequest, JSONObject page)
```

---

### 7. SSE返回值变更模式

**适用场景**：长耗时操作不适合保持SSE长连接

**变更模式**：
- **原模式**：SSE保持长连接，流式返回最终结果
- **新模式**：SSE立即返回taskId，然后关闭连接，前端通过轮询接口获取最终结果

**返回值变化**：
```json
// 原
{ "responseType": "ppt", "result": "...完整JSON...", "pptType": 1 }

// 新
{ "responseType": "ppt", "taskId": 12345, "pptType": 1 }
```

---

### 8. 项目官方命名规范

**项目名称定义**：`pc_xiaohongzhujiao_plus` 项目中，`xiaohongzhujiao` 的官方中文名称为 **"小鸿助教"**

**历史曾用名**：小红猪家校共育平台

**使用规范**：
- 正式文档、代码注释、用户界面等场景统一使用"小鸿助教"
- 历史归档中出现的"小红猪"为曾用名，不影响理解

---

## 🟡 常见问题速查

### 9. 开发常见问题速查

| 问题 | 原因 | 解决 |
|------|------|------|
| Maven仓库权限错误 | 沙箱/容器不允许访问项目外的Maven仓库 | 重新启动，依赖通常已预下载 |
| Broken pipe 日志报错 | 客户端断开连接后服务器尝试发送数据 | 不需要捕获，保持现状即可 |
| lambda访问effectively final | lambda表达式需要访问final变量 | 直接初始化变量，避免条件赋值 |
| DTO缺字段导致业务字段静默丢失 | DTO与Entity字段不对齐，`BeanUtils.copyProperties` 拷贝时缺字段为null | 新增业务字段时同步更新DTO/VO/Entity三处；写入链路要端到端联调 |
| NoClassDefFoundError 但源码与编译均正常 | IDE 增量编译产物不完整，运行时 classpath 与磁盘 target 不一致 | `mvn clean compile`（或 IDE Rebuild）+ 重启；判定关键 = 同名 class 在 target 存在但运行时加载失败，不要怀疑代码 |
| IDE import 标红但 mvn 编译通过 | IDE 索引/缓存失效 | ① Maven 面板 Reload All → ② Invalidate Caches / Restart → ③ `mvn clean compile`；命令行编译通过 + 多文件同 import + 仅 IDE 标红 = 环境问题，不改代码 |

---

## 🟢 权限与授权体系设计

### 10. 双层可见性控制模式（智能体权限）

**适用场景**：多租户系统中，既要有组织级粗粒度控制，也要有资源级细粒度控制

**架构模式**：
```
第一层：组织维度（t_org_agent_rel）
  - 学校/区域管理员维护 user_agent_id_list 白名单
  - 决定"某组织能看到哪些智能体"（粗粒度）

第二层：资源维度（user_agent.agent_range_formal）
  - 智能体创建者选择可见范围（1=仅自己 / 2=本校 / 3=本区域）
  - 决定"该智能体对谁可见"（细粒度）
```

**关键闭环**：发布资源时必须同步更新组织白名单，否则出现"发布了但看不到"的死角。
- 发布 agentRange=2（本校） → 追加到发布者学校的 user_agent_id_list
- 发布 agentRange=3（本区域） → 追加到发布者区域的 user_agent_id_list
- 发布 agentRange=1（仅自己） → 不更新白名单

**教训**：设计"手动维护白名单"模式时，必须评估创建方与消费方的一致性。否则用户发布后同组织其他人看不到，产品语义与实现语义相悖。

---

### 11. SQL 逗号分隔列表的幂等追加模式

**适用场景**：`user_agent_id_list` 这类 `,10,20,30,` 格式的列表字段，追加ID时防重

**关键SQL**：
```sql
UPDATE t_org_agent_rel
   SET user_agent_id_list = CONCAT(IFNULL(user_agent_id_list, ''), #{agentId}, ','),
       update_time = NOW()
 WHERE school_id = #{schoolId}
   AND is_deleted = 0
   AND (user_agent_id_list IS NULL OR user_agent_id_list NOT LIKE CONCAT('%,', #{agentId}, ',%'))
```

**要点**：
- `CONCAT + IFNULL`：处理NULL初始值，追加时形如 `,10,20,` 保持首尾逗号
- `NOT LIKE '%,ID,%'`：利用首尾逗号定界防止部分匹配（如避免 `,1,` 匹配到 `,10,`）
- WHERE 内联防重条件，保证同一事务内幂等
- 更新时机放在业务写入完成之后（如 `saveOrUpdate` 之后再追加），确保有效 agentId

---

### 12. 服务接口权责分明原则

**教训**：Service 方法不要返回包装类聚合多个信息，而应按职责拆分为多个方法

**反例**：
```java
// 返回聚合类 VisibleScope（含 openMode + visibleAgentIds）
VisibleScope resolveVisibleScope(String openid);
```

**正例**：
```java
// 权责分明，各司其职
List<Long> resolveVisibleScope(String openid);         // 只返回白名单
PublishRangeVO resolvePublishRanges(String openid);    // 只返回发布范围
NavConfigVO resolveNavConfig(String openid);           // 只返回导航配置
void appendAgentToOrgWhitelist(...);                    // 只做白名单写入
```

**收益**：
- 调用方只关注自己需要的信息
- 单个方法可独立演进
- Mapper SQL 更简洁（不需要在 SQL 中同时构造多层信息）
- 消除调用方重复空值判断（如 `openid` 非空由调用方保证，Service 不重复判断）

---

## 更新记录

| 日期 | 更新内容 | 更新人 |
|------|---------|--------|
| 2026-10-20 | 总-分-总回流：#5 JSON容错扩充（根本方案/预清理/降级容错/Markdown清理）；速查表新增 DTO缺字段、NoClassDefFoundError、IDE import 标红；新增 #10 双层可见性控制、#11 SQL幂等追加、#12 服务接口权责分明（回流自项目A分支2 experience/architecture.md 本地增量） | Trae |
