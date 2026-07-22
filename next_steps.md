# 下阶段执行清单（7 月 22 日 — 9 月）

> 与 `experiment_manifest.json` / `preregistration.md` / `paper_outline.md` 对齐。

## Week 0（本周，2026-07-22 ~ 28）

| 任务 | 负责人 | 状态 |
|---|---|---|
| [x] 选题论证（已生成）| – | 完成 |
| [x] 研究方案 HTML（已生成）| – | 完成 |
| [x] 预注册 Markdown（已生成）| – | 完成 |
| [x] 实验清单 JSON（已生成）| – | 完成 |
| [x] 统计骨架（已生成 + 通过烟雾测试）| – | 完成 |
| [x] Pilot 脚手架（已生成 + 链路验证）| – | 完成 |
| [x] 论文大纲（已生成）| – | 完成 |
| [x] Cover letter（已生成）| – | 完成 |
| [x] 7 模型版本（已升级到 V4 Flash）| – | 完成 |

## Week 1（2026-07-29 ~ 08-04）

| 任务 | 优先级 |
|---|---|
| 创建 OSF 项目 `echo-chambers-of-one`（Private）| 高 |
| 在 OSF 上传 README + research_proposal + experiment_manifest | 高 |
| 创建 GitHub 仓库（私有）| 高 |
| 把所有代码与烟雾测试结果 push 到 GitHub | 高 |
| 设置真实 API 密钥（DeepSeek 优先）| 高 |
| 跑一次真实 DeepSeek V4 Flash 预实验 200 步 | 中 |
| 把真实结果并入 `pilot/collected_trajectories.csv` | 中 |
| 内部审阅研究方案与预注册 | 高 |

## Week 2-3（2026-08-05 ~ 18）

| 任务 | 优先级 |
|---|---|
| 修订单 / 改稿研究方案 | 高 |
| 正式登记 OSF 预注册（冻结版本）| 高 |
| 检查 AAMAS 2027 RR 通道的截稿日期（官网）| 高 |
| 提交 RR Stage 1 投稿材料（若通道开放）| 高 |
| 同步预注册与 GitHub README 链接 | 中 |

## Week 4-5（2026-08-19 ~ 09-01）

| 任务 | 优先级 |
|---|---|
| 启动正式预实验：6 模型 × 6 条件 × 1 任务 × 5 重复 | 高 |
| 监控：API 失败率、LMM 收敛率、Holm 校正通过率 | 中 |
| 与导师 / 同事分享 Stage 1 投稿（若已投）| 中 |
| 准备 CogSci / CHI 副投稿大纲 | 低 |

## 9 月（2026-09）

| 任务 | 优先级 |
|---|---|
| 完成预实验 n=5/cell | 高 |
| 用预实验方差估计正式重复数（Monte Carlo）| 高 |
| 启动正式数据收集（按扩展后的 cell 数）| 高 |
| AAMAS RR Stage 1 评审意见回复（若已投）| 高 |

## 关键截止日期

| 截止 | 事件 |
|---|---|
| 2026-08-01 | OSF 项目创建 + 预注册草稿上传 |
| 2026-08-15 | RR Stage 1 内部审阅完成 |
| ~2026-09 | AAMAS 2027 RR Stage 1 截稿（确认日期）|
| 2026-09-15 | 预实验数据收集完成 |
| 2026-12-31 | 正式数据收集完成 |
| 2027-01-15 | Stage 2 完整论文草稿 |
| 2027-02-15 | Stage 2 投稿 |

## 当前阻塞 / 风险

1. **AAMAS 2027 是否开 RR 通道** → 优先查询官网；若无通道，投 ICML RR 或 PsyArXiv 预注册。
2. **API 成本** → 优先用 DeepSeek V4 Flash（最便宜），预算约 $200–500。
3. **作者贡献** → 现只有占位符；需要确定作者顺序与贡献。
4. **IRB / 伦理审查** → 仅人类监督组需要；准备 IRB 申请至少 4 周。

## 不在当前阶段的事

- 不写完整论文（Stage 1 不需要）
- 不做完整预实验（只做 200 步 + n=5）
- 不公开数据（预注册阶段保持 Private）
- 不与真人监督者签约（9 月预实验后再启动）

## 立刻可做的事

1. 创建 OSF 项目：https://osf.io/create-project/
2. 创建 GitHub 仓库：https://github.com/new
3. 设置 DeepSeek API 密钥：
   ```bash
   setx DEEPSEEK_API_KEY "sk-..."
   python -m pip install openai
   python pilot/run_pilot.py --model deepseek-v4-flash --task vending --condition isolated --steps 200
   ```
4. 查询 AAMAS 2027 RR 通道：https://aamas-conference.aamas-conference.org/