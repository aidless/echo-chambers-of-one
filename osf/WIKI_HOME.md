# Echo Chambers of One — OSF Wiki 首页

> 把下面的内容粘贴到 OSF 项目 Wiki 的 Home 页面。

---

## 项目概览

**Echo Chambers of One** 是一个关于长程语言智能体稳定性的预注册研究。我们把"Agent 孤独感"这个传播比喻改写为可检验的"**外源交互剥夺（interaction deprivation）**"假说——一个有持久状态的语言智能体在长时间闭环运行中，缺少来自外部的新颖信息、客观纠错或同伴交互，是否会独立于任务长度与上下文污染而出现能力下降。

## 研究设计

- **7 模型** × **6 条件** × **3 任务** × **≥20 重复**
- 10000 步纵向轨迹，检查点 0 / 100 / 500 / 1k / 2k / 5k / 10k
- 主分析：纵向混合效应模型（LMM → GEE → OLS 三级回退）
- 多重比较：Holm-Bonferroni 分层校正

## 三种核心条件

| 条件 | 含义 |
|---|---|
| 闭环隔离 | 只有任务与自身记忆，无外部信号 |
| 外部新颖性 | 接收等量非社交信息 |
| 标量纠错 | 只收到对错或奖励信号 |

辅以：同伴交互、人类交互（正对照）、无状态控制（基线）。

## 时间线

| 阶段 | 日期 |
|---|---|
| Stage 1 冻结 | 2026-07-22 ✅ |
| Pilot 数据 | 2026-08 |
| Stage 1 投稿 | ~2026-09 |
| 正式数据收集 | 2026-10 → 2026-12 |
| Stage 2 投稿 | 2027-02 |

## 链接

- 📄 研究方案：`research_proposal.html`
- 📋 预注册：`preregistration.md`
- 📊 实验清单：`experiment_manifest.json`
- 💻 代码：GitHub `echo-chambers-of-one`
- 📁 数据：见 OSF Files

## 联系方式

（投稿前补）

---

## Wiki 导航建议

| 页面 | 内容 |
|---|---|
| Home | 本页 |
| Methods（详细）| 把 `research_proposal.html` 转换为 wiki 章节 |
| Pre-registration | `preregistration.md` 全文 |
| FAQ | 评审常见质疑响应（见 `cover_letter.md` 第 2 节）|
| Updates | 阶段性进展公告 |