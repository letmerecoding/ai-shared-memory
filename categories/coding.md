# 编码规范

这里存放编码相关的规范和习惯。

---

## 一、Java & Spring 专项规范

| # | 规则 |
|---|---|
| 1 | **分层解耦**：严格执行 Controller → Service → Repository；区分 Entity/DTO/VO，修改字段需要同步检查映射 |
| 2 | **Spring 防御**：写操作必须加 `@Transactional`，避开自调用事务失效场景；优先构造器注入 |
| 3 | **健壮性能**：强制使用 Optional 或工具类防止 NPE；IO 资源使用 try-with-resources；Service 保持线程安全 |

---

## 二、任务执行自检清单 (Checklist)

- [ ] **逻辑一致性**：是否扫描并处理了公共方法引用点的风险？
- [ ] **模型完整性**：Entity/DTO/VO 字段映射是否同步更新？
- [ ] **Spring 事务**：写操作是否有事务？是否存在失效场景？
- [ ] **异常与边界**：Catch 块是否包含上下文？空集合/空对象是否有防御？
- [ ] **依赖最小化**：是否引入冗余依赖或重复造轮子？
- [ ] **代码整洁**：无模糊 `//TODO`、无调试打印、无无用注释

---

## 三、接口测试要点

### 请求头格式
```
token: {token}
signature: {signature}
timestamp: {timestamp}
nonce: {nonce}
```
**不需要** `Authorization: Bearer {token}`，token 直接放在 `token` 请求头中。

### 测试流程
1. 测试前先**阅读代码 `WebMvcConfig.java`** 查找是否有跳过签名验证的测试凭证
2. 如果代码中有硬编码的测试凭证，就使用它
3. 如果代码中没有，就**询问用户提供有效的 token、signature、timestamp、nonce**
4. 拿到凭证后按照请求头格式进行接口测试

### 记住规则，不记住固定值
- 不硬编码记住具体的 token/signature 值
- 每次测试前先看代码找测试凭证
- 代码中没有就问用户要
- 拿到后按照格式测试

---

## 更新记录

| 日期 | 更新内容 | 更新人 |
|------|---------|--------|
| 2026-03-20 | 从现有协作规范迁移Java & Spring编码规范 | 迁移 |

