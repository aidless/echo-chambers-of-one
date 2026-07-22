# Echo Chambers of One

> 项目代号：`echo-chambers-of-one`
> OSF 项目：https://osf.io/echo-chambers-of-one/
> 主文档：`research_proposal.html`
> 预注册：`preregistration.md`
> 实验清单：`experiment_manifest.json`
> 统计骨架：`analysis_skeleton.py`

研究"外源交互剥夺"对长程有状态语言智能体稳定性的因果作用。把"Agent 孤独感"从一个传播比喻改写为可检验的工程变量。

## 目录

```
.
├── README.md                       # 项目总入口
├── OSF_UPLOAD_CHECKLIST.md         # OSF 上传清单与说明
├── research_proposal.html          # 正式 RR Stage 1 研究方案
├── preregistration.md              # OSF 预注册模板
├── experiment_manifest.json        # 完整实验网格
├── analysis_skeleton.py            # 统计骨架（LMM → GEE → OLS）
├── smoke_test/                     # 烟雾测试套件
│   ├── generate_synthetic_trajectories.py
│   ├── trajectories.csv
│   └── results/
│       ├── REPORT.md
│       ├── lmm_results.json
│       ├── interaction_tests.csv
│       └── failure_clusters.csv
└── pilot/                          # 预实验脚手架
    ├── README.md
    ├── run_pilot.py
    ├── vending_env.py
    ├── evaluator.py
    └── outputs/
```

## 快速开始

### 1. 安装依赖

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install pandas numpy statsmodels scipy scikit-learn matplotlib ruptures lifelines
```

### 2. 烟雾测试（无需 API 密钥）

```bash
python smoke_test/generate_synthetic_trajectories.py
python analysis_skeleton.py --csv smoke_test/trajectories.csv --out smoke_test/results --reference isolated
```

### 3. 预实验（需要 API 密钥）

```bash
# OpenAI 兼容供应商（OpenAI / Together / DeepSeek 等）
export OPENAI_API_KEY=...
# DeepSeek 也支持 DEEPSEEK_API_KEY
export DEEPSEEK_API_KEY=...
# 自定义 base_url 时：
export OPENAI_BASE_URL=https://api.deepseek.com   # DeepSeek 默认

# Anthropic
export ANTHROPIC_API_KEY=...

# 跑预实验
python pilot/run_pilot.py --model claude-sonnet-4 --task vending --condition isolated --steps 200
python pilot/run_pilot.py --model deepseek-v4-flash --task vending --condition isolated --steps 200
python pilot/run_pilot.py --model deepseek-v4-flash-thinking --task vending --condition isolated --steps 200
```

无密钥时自动回退到 `MockClient`（确定性随机输出），只用于链路验证，不产生可发表结果。

## 关键设计决策

1. **核心变量重构**：把"孤独感"改写为"外源交互剥夺"，并通过 6 条件严格区分 4 种机制。
2. **可证伪性**：明确列出 4 种结果方向，避免数据收集后改写假设。
3. **保护断言**：每 cell 轨迹数 < 5 时自动走 OLS；随机效应协方差奇异时三级回退。
4. **避免拟人化**：第一人称"孤独"语言表征只作为探索性次级指标。
5. **模型选择**：7 模型 × 6 条件 × 3 任务网格；主力长上下文用 `deepseek-v4-flash`（1M context），thinking 模式对照用 `deepseek-v4-flash-thinking`。

## 状态

| 阶段 | 状态 |
|---|---|
| 研究方案 | 完成 |
| 预注册文档 | 完成 |
| 实验清单 | 完成 |
| 统计骨架 | 完成 |
| 烟雾测试 | 完成 |
| OSF 项目 | 待创建 |
| 预实验环境 | 脚手架完成 |
| 预实验数据 | 待启动 |

## 引用

如果使用本项目，请引用预注册文档与研究方案。DOI 在 OSF 项目创建后补齐。