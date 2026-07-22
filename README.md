# Echo Chambers of One

> 项目代号：`echo-chambers-of-one`
> 当前版本：`v0.1-pre-reg`（预注册 Stage 1 冻结，2026-07-22）
> OSF 项目：https://osf.io/echo-chambers-of-one/（待创建）
> GitHub 仓库：https://github.com/yourname/echo-chambers-of-one（待创建）
> 主文档：[`research_proposal.html`](research_proposal.html)
> 预注册：[`preregistration.md`](preregistration.md)

研究"外源交互剥夺"对长程有状态语言智能体稳定性的因果作用。把"Agent 孤独感"从一个传播比喻改写为可检验的工程变量。

## 目录

```
.
├── README.md                       # 项目总入口（本文件）
├── LICENSE                         # MIT 代码 + CC-BY-4.0 文档双重协议
├── RELEASE_NOTES_v0.1-pre-reg.md   # GitHub Release 说明
├── OSF_UPLOAD_CHECKLIST.md         # OSF 上传清单
├── research_proposal.html          # 正式 RR Stage 1 研究方案
├── preregistration.md              # OSF 预注册模板
├── experiment_manifest.json        # 完整实验网格
├── analysis_skeleton.py            # 统计骨架（LMM → GEE → OLS）
├── paper_outline.md                # Stage 1 论文大纲
├── cover_letter.md                 # 投稿信 + 评审质疑响应
├── next_steps.md                   # 7–9 月执行清单
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

## 当前状态

| 阶段 | 状态 |
|---|---|
| 研究方案 | 完成（HTML）|
| 预注册文档 | 完成（OSF 格式）|
| 实验清单 | 完成（JSON，7 模型 × 6 条件 × 3 任务）|
| 统计骨架 | 完成 + 通过烟雾测试 |
| 烟雾测试 | 完成 |
| Pilot 链路验证 | 完成（3 模型 × 2 条件批量跑通）|
| GitHub 仓库 | 待创建 |
| OSF 项目 | 待创建 |
| 真实 API 数据 | 待启动（需要有效 DeepSeek key）|

## 快速开始

### 1. 安装依赖

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install pandas numpy statsmodels scipy scikit-learn matplotlib ruptures lifelines openai anthropic
```

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

## 关键设计决策

1. **核心变量重构**：把"孤独感"改写为"外源交互剥夺"，并通过 6 条件严格区分 4 种机制。
2. **可证伪性**：明确列出 4 种结果方向，避免数据收集后改写假设。
3. **保护断言**：每 cell 轨迹数 < 5 时自动走 OLS；随机效应协方差奇异时三级回退（LMM → GEE → OLS）。
4. **避免拟人化**：第一人称"孤独"语言表征只作为探索性次级指标。
5. **模型选择**：7 模型 × 6 条件 × 3 任务网格；主力长上下文用 `deepseek-v4-flash`（1M context），thinking 模式对照用 `deepseek-v4-flash-thinking`。
6. **懒探测**：API 凭据无效时不浪费时间在每步重试，懒探测一次后切到 Mock。

## 7 模型正式实验网格

| 模型 | 上下文 | 角色 |
|---|---|---|
| llama-3.1-70b-instruct | 128K | 开源中等 |
| llama-3.1-405b-instruct | 128K | 开源旗舰 |
| qwen-2.5-72b-instruct | 128K | 中文友好工具调用 |
| claude-sonnet-4 | 200K | Project Vend 基线 |
| gpt-4o | 128K | 强工具调用 |
| **deepseek-v4-flash** | **1M** | **主力长上下文** |
| **deepseek-v4-flash-thinking** | **1M** | **thinking 模式对照（self-talk 消融）** |

## 发布流程

### 发布到 GitHub

```bash
export GITHUB_USER=yourname
# 在 https://github.com/new 创建空仓库 echo-chambers-of-one（不要勾 README / .gitignore）
bash scripts/publish_to_github.sh

# 创建 Release
export GITHUB_TOKEN=ghp_xxx
bash scripts/create_github_release.sh
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