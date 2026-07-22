# OSF 上传清单

> 目标平台：OSF（https://osf.io/）
> 推荐路径：https://osf.io/echo-chambers-of-one/（注册时使用此 slug）
> 项目类别：Pre-Data Collection Registration
> 许可协议：CC-BY-4.0
> 隐私等级：Public（完成后转 Public；预注册阶段建议 Private）

## 一、OSF 项目元数据

| 字段 | 值 |
|---|---|
| Title | Echo Chambers of One: Longitudinal Degradation under Interaction Deprivation in Stateful Language Agents |
| Description | 把"Agent 孤独感"改写为"外源交互剥夺"的可证伪假设，并通过 6 条件 × 6 模型 × 3 任务的纵向混合效应设计检验其对长程语言智能体稳定性的因果作用。 |
| Category | Cognitive Science / AI / HCI |
| Contributors | 主要研究者（待补）、共同作者（待补） |
| License | CC-BY-4.0 |
| Tags | `agent-degradation`, `long-horizon`, `interaction-deprivation`, `mixed-effects`, `preregistration` |

## 二、需要上传的文件

### 1. 预注册文档（OSF Wiki / Registrations）

| 文件 | 用途 | OSF 路径 |
|---|---|---|
| `preregistration.md` | 完整预注册模板 | Registrations → New → Standard Pre-Data Collection |

### 2. 研究方案（OSF Wiki / Files）

| 文件 | 大小预估 | OSF 路径 |
|---|---|---|
| `research_proposal.html` | ~25 KB | Files → root → research_proposal.html |
| `experiment_manifest.json` | ~5 KB | Files → root → experiment_manifest.json |
| `README.md` | ~3 KB | Files → root → README.md |

### 3. 分析代码（OSF GitHub 集成或 Files）

| 文件 | 用途 |
|---|---|
| `analysis_skeleton.py` | 主分析脚本（LMM → GEE → OLS） |
| `smoke_test/generate_synthetic_trajectories.py` | 合成数据生成器 |
| `smoke_test/trajectories.csv` | 烟雾测试轨迹（示例数据） |

### 4. 烟雾测试结果（Files）

| 文件 | 用途 |
|---|---|
| `smoke_test/results/REPORT.md` | 链路验证报告 |
| `smoke_test/results/lmm_results.json` | LMM 详细输出 |
| `smoke_test/results/interaction_tests.csv` | 交互项 p 值表 |
| `smoke_test/results/failure_clusters.csv` | 失败模式聚类 |

## 三、上传步骤

### Step 1：创建 OSF 项目

1. 登录 https://osf.io/
2. 点 "+ Create" → "Project"
3. 填入项目元数据（见上表）
4. 选择 "Open-Ended Registration" → "Preregistration"

### Step 2：上传文件

```bash
# 推荐使用 OSF CLI（osfclient）
pip install osfclient
osf login
osf init echo-chambers-of-one
osf upload research_proposal.html
osf upload preregistration.md
osf upload experiment_manifest.json
osf upload analysis_skeleton.py
osf upload README.md
osf upload smoke_test/ -r smoke_test/
```

### Step 3：登记预注册

1. 在项目页面点 "Registrations" → "New Registration"
2. 选择 "Open-Ended Registration"
3. 粘贴 `preregistration.md` 全文到 Rich Text Editor
4. 选择时间戳与创建者
5. 提交后 OSF 会冻结一份不可修改的版本

### Step 4：链接 GitHub

1. 在项目设置 → "Add-Ons" → 启用 GitHub
2. 链接到 GitHub 仓库 `echo-chambers-of-one`
3. 之后每次 push 都会同步到 OSF

## 四、上传顺序建议

| 顺序 | 动作 | 时间点 |
|---|---|---|
| 1 | 创建 OSF 项目（Private） | 2026-07-22 |
| 2 | 上传 README + 研究方案 + 实验清单 | 2026-07-22 |
| 3 | 上传预注册文档草稿 | 2026-07-23 |
| 4 | 内部审阅与修订 | 2026-07-25 |
| 5 | 正式登记预注册（OSF 冻结版本） | 2026-08-01 |
| 6 | 上传分析代码与烟雾测试结果 | 2026-08-01 |
| 7 | 链接 GitHub 仓库 | 2026-08-02 |
| 8 | 转 Public | 2027-02-15（Stage 2 投稿时）|

## 五、关键提醒

- **预注册必须在看到任何真实实验数据之前完成并冻结**。
- 烟雾测试的合成数据**不算真实数据**，仅用于验证统计链路；可以提前上传。
- OSF 项目创建后，把项目链接加进 `README.md` 顶部。
- 上传完成后，把 DOI 也加进 README 与 `research_proposal.html`。