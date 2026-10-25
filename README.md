# Echo Chambers of One
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  [![Data](https://img.shields.io/badge/data-CC--BY--4.0-lightgrey.svg)](LICENSE)

> 项目代号：`echo-chambers-of-one`
> 当前版本：`v0.4-pre-reg`（第三轮文献调研修订，2026-07-29）
> GitHub 仓库：https://github.com/aidless/echo-chambers-of-one
> OSF 项目：https://osf.io/echo-chambers-of-one/（待创建）
> 主文档：[`research_proposal.html`](research_proposal.html)
> 预注册 v0.4：[`preregistration.md`](preregistration.md)
> 深度调研：[`LITERATURE_REVIEW.md`](LITERATURE_REVIEW.md)

研究"外源交互剥夺"对长程有状态语言智能体稳定性的因果作用。把"Agent 孤独感"从一个传播比喻改写为可检验的工程变量。

## 目录

```
.
├── README.md                       # 项目总入口（本文件）
├── LICENSE                         # MIT 代码 + CC-BY-4.0 文档双重协议
├── RELEASE_NOTES_v0.1-pre-reg.md   # GitHub Release 说明
├── LITERATURE_REVIEW.md            # 2025-2026 深度文献调研（v0.1→v0.4 三轮，见 _v2/_v3）
├── OSF_UPLOAD_CHECKLIST.md         # OSF 上传清单
├── research_proposal.html          # 正式 RR Stage 1 研究方案
├── preregistration.md              # OSF 预注册 v0.4（含修订说明）
├── experiment_manifest.json        # 完整实验网格 v0.4
├── analysis_skeleton.py            # 统计骨架（LMM → GEE → OLS）
├── paper_outline.md                # Stage 1 论文大纲 v0.2
├── cover_letter.md                 # 投稿信 + 评审质疑响应
├── next_steps.md                   # 7–9 月执行清单
├── DEPLOYMENT_GUIDE.md             # GitHub/OSF/DeepSeek 详细操作指南
├── scripts/                        # 一键上传脚本
│   ├── osf_upload.py               # OSF 自动上传
│   ├── publish_to_github.sh        # GitHub 推送
│   └── create_github_release.sh    # GitHub Release 创建
├── osf/                            # OSF Wiki / 预登记粘贴文本
│   ├── WIKI_HOME.md                # Wiki 首页
│   ├── PREREGISTRATION_PASTE.md    # 预登记粘贴内容
│   └── FAQ.md                      # 评审 FAQ
├── smoke_test/                     # 烟雾测试套件
└── pilot/                          # 预实验脚手架
```

## 当前状态（v0.4）

| 阶段 | 状态 |
|---|---|
| 研究方案 | 完成（HTML）|
| 预注册文档 | ✅ v0.4 修订版（三轮修订；v0.4 增量：模型 3→5、新增伦理与 IRB / PRISMA 2020 / OSF 结构章节）|
| 实验清单 | ✅ v0.2（3 模型 × 4 长度 × 6 条件 × 3 任务 × 3 重复 = 648 cell / 1944 轨迹）|
| 统计骨架 | 完成 + 通过烟雾测试 |
| 烟雾测试 | 完成 |
| Pilot 链路验证 | 完成（3 模型 × 2 条件批量跑通）|
| 深度文献调研 | ✅ LITERATURE_REVIEW.md（20 篇 P0/P1 工作）|
| GitHub 仓库 | ✅ 已推送（main + 5 commits + v0.1-pre-reg 标签）|
| GitHub Release | ⏳ 需手动在网页创建（Release API 无权限）|
| OSF 项目 | 待创建 |
| 真实 API 数据 | 待启动（需要有效 DeepSeek key）|

## 快速开始

### 1. 安装依赖

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install pandas numpy statsmodels scipy scikit-learn matplotlib ruptures lifelines openai anthropic
```

- Python 版本：CI 在 **3.12** 上运行（`.github/workflows/ci.yml`）。
- 最小依赖（仅烟雾测试 + 统计骨架）：`pandas numpy statsmodels scipy scikit-learn`；`analysis_skeleton.py` 的变点检测在未安装 `ruptures` 时自动跳过（try/except，见 `analysis_skeleton.py` 的 `detect_change_points`）。
- Seed 策略：`pilot/run_pilot.py --seed`（默认 11），同一 seed 同时传给 `VendingEnv(seed=seed)` 和 LLM 客户端（`pilot/runner.py`），Mock 回退路径是确定性随机。

### 2. 烟雾测试（无需 API 密钥）

```bash
python smoke_test/generate_synthetic_trajectories.py
python analysis_skeleton.py --csv smoke_test/trajectories.csv --out smoke_test/results --reference isolated
```

### 3. Pilot 链路验证（需要 API 密钥，无效时自动 Mock）

```bash
export OPENAI_API_KEY=...        # 或 DEEPSEEK_API_KEY
export DEEPSEEK_API_KEY=...
export OPENAI_BASE_URL=https://api.deepseek.com   # DeepSeek 默认
export ANTHROPIC_API_KEY=...

python pilot/run_pilot.py --model claude-sonnet-4 --task vending --condition isolated --steps 200
python pilot/run_pilot.py --model deepseek-v4-flash --task vending --condition isolated --steps 200
python pilot/run_pilot.py --model deepseek-v4-flash-thinking --task vending --condition isolated --steps 200

python pilot/collect_outputs.py
python analysis_skeleton.py --csv pilot/collected_trajectories.csv --out pilot/results --reference isolated
```

无密钥或凭据失效时自动回退到 `MockClient`（确定性随机），并在 `pilot/outputs/<model>__<task>__<condition>__seed<seed>__<timestamp>.json` 留下轨迹日志。

## 数据与结果可用性

本仓库处于预注册阶段（v0.4），**不含真实 API 实验数据**（与上方状态表一致）。现有结果文件的来源：

| 结果文件 | 生成方式 | 原始数据 |
|---|---|---|
| `smoke_test/results/`（`lmm_results.json`、`interaction_tests.csv`、`failure_clusters.csv`）| 快速开始第 2 步的两条命令重新生成（已实测通过）| `smoke_test/generate_synthetic_trajectories.py` 合成 |
| `pilot/results/`（同名三件套）| `python pilot/collect_outputs.py` 后对收集的 CSV 跑 `analysis_skeleton.py` | `pilot/collected_trajectories.csv` 与 `pilot/outputs/` 轨迹**未提交**（链路验证为 Mock 模式，见 `pilot/PILOT_REPORT.md`）|

正式实验数据采集待 DeepSeek key 就绪后启动；OSF 项目创建后在此处补 DOI 与数据归档链接。预注册文本 [`preregistration.md`](preregistration.md)（v0.4）为冻结快照，修订历史见文内修订说明。

## 关键设计决策（v0.2）

1. **核心变量重构**：把"孤独感"改写为"外源交互剥夺"，并通过 6 条件严格区分 4 种机制。
2. **可证伪性**：明确列出 4 种结果方向，避免数据收集后改写假设。
3. **保护断言**：每 cell 轨迹数 < 5 时自动走 OLS；随机效应协方差奇异时三级回退（LMM → GEE → OLS）。
4. **避免拟人化**：第一人称"孤独"语言表征只作为探索性次级指标。
5. **模型选择**（v0.2 修订）：从 7 模型缩到 **3 模型**（deepseek-v4-flash 1M、claude-sonnet-4、gpt-4o），加 **4 长度**正交维度，**3 任务**正交覆盖 3 种失败机制。
6. **Context rot 控制**（v0.2 关键修订）：4 状态视图反事实（raw / structured / fake-memory / lorem）排除 context rot 混淆。
7. **失败归因**（v0.2 关键修订）：借鉴 HORIZON，三类归因（planning / memory / historical-error）作为次要 outcome。
8. **8 机制对抗控制**（v0.2 修订）：增加 oracle / adversarial feedback 防止 self-talk 假阴性。
9. **懒探测**：API 凭据无效时不浪费时间在每步重试，懒探测一次后切到 Mock。

## v0.1 → v0.2 主要变化

| 维度 | v0.1 | v0.2 |
|---|---|---|
| 模型数 | 7 | 3 |
| 任务 | 3 | 3（正交化覆盖 3 种机制）|
| 长度操纵 | 无 | **新增 4 长度正交维度** |
| 状态视图 | 1（原始）| 4（反事实）|
| 失败归因 | 无 | **新增 3 类 schema** |
| 8 机制对抗 | 无 | **新增 oracle / adversarial** |
| 重复 | ≥20 | 3 |
| Cell 数 | 2520 | 648 |
| 轨迹数 | 12600 | 1944 |
| 预算 | $200–500 | $1500–$2500 |

## 7 模型正式实验网格（v0.2 修订：3 模型）

| 模型 | 上下文 | 角色 |
|---|---|---|
| **deepseek-v4-flash** | **1M** | **主力长上下文** |
| claude-sonnet-4 | 200K | 闭源 baseline |
| gpt-4o | 128K | 强工具调用 baseline |

## 发布流程

### 发布到 GitHub

```bash
# 已通过 SSH 推送 main + 标签；Release 需手动在 GitHub 网页从 v0.1-pre-reg 标签创建
# https://github.com/aidless/echo-chambers-of-one/releases/new
# 粘贴 RELEASE_NOTES_v0.1-pre-reg.md 内容，勾 Set as a pre-release，Publish
```

### 发布到 OSF

```bash
pip install osfclient
osf login    # 浏览器授权

# 在 https://osf.io/create-project/ 创建项目
python scripts/osf_upload.py --project <your-osf-id> --dry-run
python scripts/osf_upload.py --project <your-osf-id>
```

## 引用

如果使用本项目，请引用预注册文档与研究方案。DOI 在 OSF 项目创建后补齐。

## 许可证

- 代码：MIT
- 文档、数据、预注册：CC-BY-4.0