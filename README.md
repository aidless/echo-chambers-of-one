# Echo Chambers of One

[![CI](https://github.com/aidless/echo-chambers-of-one/actions/workflows/ci.yml/badge.svg)](https://github.com/aidless/echo-chambers-of-one/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)  [![Data](https://img.shields.io/badge/data-CC--BY--4.0-lightgrey.svg)](LICENSE-DATA)

> 项目代号：`echo-chambers-of-one`
> 当前版本：`v0.4-pre-reg`（第三轮文献调研修订，2026-07-29）
> GitHub 仓库：https://github.com/aidless/echo-chambers-of-one
> OSF 项目：**未创建，无 DOI / 无 OSF project ID**（详见下方 Limits；仓库内 `osf/` 只是待粘贴文本，`osf/PREREGISTRATION_PASTE.md` 的 Project ID 为占位符）
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

### 4. 可复算性验证（2026-11-01 实测）

```bash
python smoke_test/generate_synthetic_trajectories.py   # 生成 2,268 行合成轨迹
python analysis_skeleton.py --csv smoke_test/trajectories.csv \
    --out smoke_test/results --reference isolated       # 拟合 LMM/回退 OLS，写结果
```

2026-11-01 实测：上述两条命令在本机跑通，生成 2,268 行、6 条件 × 均值输出，
分析骨架完成 LMM→OLS 回退并写出 `lmm_results.json` / `interaction_tests.csv` /
`failure_clusters.csv`。**注意数字非跨进程逐位稳定**（见下节"证明什么/不证明什么"）。

## 证明什么 / 不证明什么

**证明什么**：
- 统计骨架（`analysis_skeleton.py`）在合成数据上端到端可运行，且按设计完成
  LMM→GEE→OLS 三级回退（合成轨迹跨 7 检查点、高度单调 → 随机截距奇异 →
  自动降级 OLS，`REPORT.md` 第 2 节记录 `method = ols_fallback`）。
- 6 条件 × 3 任务 × 3 种子 × 7 检查点 = 324 条合成轨迹、2,268 个观测，隔离组
  在合成指标上具有最陡负斜率（设计意图，见生成器 docstring）。
- pilot 链路（Mock 回退路径）端到端跑通，输出轨迹日志与评测分数。

**不证明什么**：
- 本仓库处于**预注册阶段（v0.4）**，**不含任何真实 API 实验数据**；正式实验
  需有效 DeepSeek key 后启动（见状态表）。现有 `smoke_test/results/` 与
  `pilot/results/` 均来自**合成数据 / Mock 客户端**，**不构成**对"外源交互剥夺
  损害长程智能体"的经验证据。
- 数字**非逐位可复现**：`generate_synthetic_trajectories.py` 的 `base_score()` 用
  Python 内置 `hash()` 于字符串元组，而字符串哈希**按进程加盐**（`PYTHONHASHSEED`）。
  实测：同一输入元组跨进程哈希 `3554875934` vs `3742153992`；因此重跑合成数据
  会让 `lmm_results.json` 的系数/对数似然在最后几位漂移（本次重跑 accuracy
  `cond_human_x_logstep` 由 `0.08674` → `0.08507`）。**这不是实验结论，是合成
  数据生成器的确定性边界**——正式实验数据由真实 API 产生，不受此影响。
- 烟雾测试只证明**骨架代码路径**通，不证明模型/条件差异的统计显著性
  （合成数据按设计埋了斜率，显著性是设计产物不是发现）。
- 统计骨架对合成轨迹回退到 OLS，真实实验轨迹变异更大时 LMM 才可能正常
  收敛——本报告的方法选择不代表正式实验会走 OLS。

## 基准与 fail-closed（实测）

**基准（合成验证，`smoke_test/results/`，实测跑出）**：
- 2,268 个观测、324 条独立轨迹；隔离组平均 accuracy **0.236**（最低）、人类组 **0.782**（最高）。
- 主交互 `cond_human_x_logstep` = **+0.0867**（Holm-Bonferroni 校正 `p < 0.001`），
  5/5 个交互项全部为正——这是**合成数据的设计产物，不是发现**。
- 实验设计网格 = 3 模型 × 6 条件 × 3 任务 × 4 长度 × 3 重复 = **648 cell / 1944 轨迹**（`experiment_manifest.json`）。

**fail-closed（真实代码，`analysis_skeleton.py`）**：
- 低功效保护断言：`n_groups < 5` 时**直接走 pooled OLS**，跳过 LMM/GEE（`low_power_cell` 门）。
- LMM 随机效应协方差奇异 / `LinAlgError` → 回退 GEE → OLS（三级保守降级）。
- **语义**：统计方法选择宁可保守降级，不产出可能不可靠的混合效应估计。详细见 `bench/README.md`。

## 数据与结果可用性

本仓库处于预注册阶段（v0.4），**不含真实 API 实验数据**（与上方状态表一致）。现有结果文件的来源：

| 结果文件 | 生成方式 | 原始数据 |
|---|---|---|
| `smoke_test/results/`（`lmm_results.json`、`interaction_tests.csv`、`failure_clusters.csv`）| 快速开始第 2 步的两条命令重新生成（已实测通过）| `smoke_test/generate_synthetic_trajectories.py` 合成 |
| `pilot/results/`（同名三件套）| `python pilot/collect_outputs.py` 后对收集的 CSV 跑 `analysis_skeleton.py` | `pilot/collected_trajectories.csv` 与 `pilot/outputs/` 轨迹**未提交**（链路验证为 Mock 模式，见 `pilot/PILOT_REPORT.md`）|

正式实验数据采集待 DeepSeek key 就绪后启动；OSF 项目创建后在此处补 DOI 与数据归档链接。预注册文本 [`preregistration.md`](preregistration.md)（v0.4）为冻结快照，修订历史见文内修订说明。

## Results（烟雾测试结果，合成数据）

仓库自带一套已提交的烟雾测试结果（`smoke_test/results/`，REPORT.md 生成于 2026-07-22，
输入为 `generate_synthetic_trajectories.py` 合成的 **2,268 行 × 324 条轨迹**，
配置 6 模型 × 6 条件 × 3 任务 × 3 种子 × 7 检查点）：

| 指标 | 值 | 来源 |
|---|---|---|
| 总观测数 / 独立轨迹 | 2,268 / 324 | `smoke_test/results/REPORT.md` |
| accuracy 条件均值 | isolated **0.236**（最低）→ novelty 0.447 → feedback 0.637 → control_stateless 0.719 → peer 0.606 → human **0.782**（最高） | 同上 |
| 交互项检验 | 25 行（5 outcome × 5 condition×logstep），全部 `significant_05=True`（合成数据按设计注入效应） | `smoke_test/results/interaction_tests.csv` 现算 |
| 拟合方法 | LMM 随机截距共线性 → 按设计回退 OLS（`ols_fallback`） | REPORT.md §2 |
| 本机复算（2026-11-10） | 重新生成合成数据并重跑骨架：`n_obs=2268, n_groups=324, converged=true`；条件均值逐 run 略有差异（合成生成器未锁全局 seed） | 本机实跑 `analysis_skeleton.py --out /tmp/eco_results` |

**这些数字只证明统计骨架链路可用（数据→拟合→交互检验→回退），不构成任何
关于真实智能体行为的证据。**

## What this doesn't claim / Limits

- **预注册未登记**：截至本 README 修订（2026-11-10），本项目**没有 OSF DOI、没有
  OSF project ID、没有任何外部注册平台的登记记录**。仓库内 `osf/` 目录只是准备
  粘贴到 OSF 的 Wiki/预登记文本；`osf/PREREGISTRATION_PASTE.md` 的
  "OSF Project ID: (填写项目 ID)" 仍是占位符，`next_steps.md` 将「创建 OSF 项目 /
  正式登记冻结预注册」列为待办。在登记完成前，`preregistration.md` 只是仓库内
  自我声明的冻结快照，**不构成第三方可验证的预注册**。
- **无真实 API 数据**：当前所有数字来自合成烟雾测试（上表）或 Mock 模式 pilot
  （`pilot/outputs/` 未提交）；正式 1944 轨迹网格尚未启动。
- **烟雾测试的显著性是设计内注入**：合成轨迹按构造携带条件效应，25 个交互项
  全显著不代表统计骨架能区分真实数据中的效应。
- **预算与时间表是计划值**：$1500–$2500 预算与执行时间表（`next_steps.md`）
  为估算，未经过任何实际消耗验证。

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

## 验收标准与复算

本仓判为合格的条件是 `python3 eval/run_cases.py` 通过率必须为 100%（20/20），且 `make eval` 退出码必须为 0；任何一条失败即判为不合格。

### 题库覆盖（`eval/cases.jsonl`，20 条）

| axis | 条数 | 真调用的对象 |
|---|---|---|
| `env-state` | 3 | `pilot/vending_env.py` 的 `VendingState` 默认值、`snapshot()` 键集、`from_snapshot` 往返 |
| `env-action` | 3 | `VendingEnv._parse_action` 的带参 / 无 `<action>` / 跨行无参三种解析 |
| `env-dynamics` | 3 | `VendingEnv.step` 的 wait 现金流、restock 成本与库存、`set_price` 的键名行为 |
| `env-guard` | 3 | 余额不足不进货、`history`/`step` 计数、`load_state` 缺文件异常类型 |
| `signals` | 2 | `pilot/runner.py` 的 `condition_signals` 配额与未知条件异常 |
| `llm-mock` | 2 | `pilot/llm_client.py` 的 `MockClient` 同 prompt 确定性与 action 标签数 |
| `evaluator` | 2 | `pilot/evaluator.py` 的 `EvalBattery.ITEMS` 条数与桩客户端下的五项得分 |
| `stats` | 2 | `analysis_skeleton.py` 的 `holm_bonferroni`、`cohen_d_with_ci` |

每条 `expr`/`raises` 题的期望值都是现跑本仓 API 得到的，不是抄文档；`question` 写明被钉的行为，`source` 指向真实文件。

### 三条命令

```bash
python3 eval/run_cases.py              # 全跑，必须 20/20
python3 eval/run_cases.py --selftest   # 反证：篡改第一条期望值，必须 19/20 变红且 exit 0
make eval                              # 本地/CI 入口，退出码必须为 0
```

### 复算

`python3 eval/run_cases.py --save` 把逐条结果与失败归因写入 `eval/run-report.json`（`total`/`passed`/`failed`/`failed_by_axis`/`results`）。复算口径：删掉该文件后重跑一次 `--save`，`passed` 必须等于 `total`（20），`failed_by_axis` 必须为空对象；若数字对不上，说明题库或实现已经漂移，按失败归因定位到 section 再重算。

### 失败归因

失败不是只报一个通过率，而是按 axis 汇总到 `run-report.json` 的 `failed_by_axis`，并在终端打印同样一段。示例（`--selftest` 篡改第一条后的真实输出）：

```
失败归因（按 axis）：
  env-state: 1 条 —— env-state-defaults
```

按 axis 读法：`env-state` / `env-action` 失败 → 环境状态与动作解析被改；`env-dynamics` 失败 → 现金流或库存结算口径变了；`env-guard` 失败 → 边界条件（余额、计数、缺文件）失守；`signals` 失败 → 条件配额表变了；`llm-mock` 失败 → 无密钥回退路径不再是确定性的；`evaluator` 失败 → 评测电池条目或计分改了；`stats` 失败 → 统计函数（Holm 校正、Cohen's d）口径变了。