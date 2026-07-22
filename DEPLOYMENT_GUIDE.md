# Echo Chambers of One · 详细发布与启动指南

> 目标：把当前 v0.1-pre-reg 推送到 GitHub、登记到 OSF、跑一次真实 DeepSeek V4 Flash 预实验。
> 预计耗时：1.5–2 小时（主要在 GitHub / OSF 网页交互 + 等待审批）。

---

## Part A：GitHub 发布（约 20 分钟）

### A1. 创建 GitHub 仓库

1. 打开 https://github.com/new
2. 填写：
   - **Owner**：你的用户名
   - **Repository name**：`echo-chambers-of-one`
   - **Description**：`Longitudinal degradation under interaction deprivation in language agents`
   - **Public / Private**：推荐 Public（论文要求 OSF + 公开代码）
3. **关键**：下方 4 个勾选框 **全部不勾选**
   - ☐ Add a README file
   - ☐ Add .gitignore
   - ☐ Choose a license
   - ☐ Allow secrets scanner
4. 点 **Create repository**

### A2. 推送本地代码

在 PowerShell（cwd 已经是项目根）执行：

```powershell
# 替换 yourname 为你的 GitHub 用户名
$env:GITHUB_USER="yourname"
bash scripts/publish_to_github.sh
```

预期输出：
```
[1/4] 检查 git 状态...
[2/4] 添加远程...
[3/4] 推送 main + v0.1-pre-reg 标签...
[4/4] 设置默认分支为 main...
完成。访问：https://github.com/yourname/echo-chambers-of-one
```

### A3. 创建 GitHub Release

#### A3.1 创建 Personal Access Token（如果还没有）

1. 打开 https://github.com/settings/tokens?type=beta
2. 点 **Generate new token** → **Fine-grained token**
3. 填写：
   - **Token name**：`echo-chambers-release`
   - **Expiration**：90 days
   - **Resource owner**：你的用户名
   - **Repository access**：Only select repositories → 选 `echo-chambers-of-one`
   - **Permissions**：
     - Contents: Read and write
     - Metadata: Read-only（自动）
4. 点 **Generate token**
5. **复制 token**（页面刷新后不再可见）

#### A3.2 运行 Release 脚本

```powershell
$env:GITHUB_USER="yourname"
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
bash scripts/create_github_release.sh
```

预期输出：
```
[1/3] 检查标签是否存在...
[2/3] 创建 Release...
[3/3] 完成。
Release URL: https://github.com/yourname/echo-chambers-of-one/releases/tag/v0.1-pre-reg
```

#### A3.3 在 GitHub 网页设置仓库元数据

打开 https://github.com/yourname/echo-chambers-of-one → 右上角 ⚙ Settings：

1. **General → Topics**：添加
   - `agent-degradation`
   - `long-horizon`
   - `interaction-deprivation`
   - `preregistration`
   - `registered-report`
   - `llm-agent`
2. **General → About → Releases**：勾 Show prereleases
3. **General → Features**：勾 Issues（可选 Discussions）

### A4. 回填链接

把 GitHub URL 写进 `README.md` 第 5 行：

```markdown
> GitHub 仓库：https://github.com/yourname/echo-chambers-of-one
```

```powershell
# 修改 README.md 后
git add README.md
git commit -m "docs: link GitHub repo"
git push
```

---

## Part B：OSF 预登记（约 30 分钟）

### B1. 创建 OSF 项目

1. 打开 https://osf.io/create-project/
2. 登录（没有账号先注册）
3. 填写：
   - **Title**：`Echo Chambers of One: A Causal Test of Interaction Deprivation on Long-Horizon State Stability in Language Agents`
   - **Category**：Cognitive Science / HCI
   - **Description**：
     > Pre-registered Registered Report examining whether stateful language agents exhibit measurable capability degradation in the absence of fresh external input, corrective feedback, or peer coordination. Design: 7 models × 6 conditions × 3 tasks × ≥20 trajectories per cell.
   - **License**：CC-BY-4.0
   - **Privacy**：**Private**（Stage 1 期间；Stage 2 投稿前转 Public）
4. 点 **Create**
5. **复制项目 ID**：URL 中 `https://osf.io/<5-7字符>/`，把 `<5-7字符>` 保存下来，例如 `x7y8z`

### B2. 创建 Wiki Home

1. 进项目 → 左侧 **Wiki** → **Home** → **Edit**
2. 复制 [`osf/WIKI_HOME.md`](osf/WIKI_HOME.md) 全部内容粘贴
3. 点 **Save**

### B3. 上传文件

#### 方法 1：用 osfclient（推荐）

```powershell
pip install osfclient
osf login    # 浏览器授权
python scripts/osf_upload.py --project <your-osf-id> --dry-run    # 预检查
python scripts/osf_upload.py --project <your-osf-id>             # 实际上传
```

预期输出：
```
[done] 21 files uploaded to OSF project x7y8z
```

#### 方法 2：手动拖拽

1. 进项目 → **Files**
2. 点 **New Folder**，依次创建：
   - `code/` → 拖 `analysis_skeleton.py`
   - `pilot/` → 拖 `pilot/README.md` 和 6 个 `.py` 文件
   - `smoke_test/` → 拖 `smoke_test/results/` 下 4 个文件
3. 在根目录拖：
   - `research_proposal.html`
   - `preregistration.md`
   - `experiment_manifest.json`
   - `paper_outline.md`
   - `cover_letter.md`
   - `README.md`
   - `LICENSE`

### B4. 登记预注册

1. 进项目 → **Registrations** → **+ New Registration**
2. 选择 **Open-Ended Registration**
3. 在 Rich Text 编辑器粘贴 [`osf/PREREGISTRATION_PASTE.md`](osf/PREREGISTRATION_PASTE.md) 全文
4. 填写：
   - **Registration title**：同项目名
   - **Description**：（可选）留空
5. 点 **Submit**
6. OSF 会**冻结一份不可修改的版本**并分配 DOI

### B5. 创建 FAQ Wiki 页面（可选）

1. 进项目 → **Wiki** → **New Page**
2. Title：`FAQ`
3. 粘贴 [`osf/FAQ.md`](osf/FAQ.md) 全文

### B6. 回填链接

把 OSF URL 写进 `README.md`：

```markdown
> OSF 项目：https://osf.io/<your-id>/
> OSF DOI：(登记后会显示在项目页面)
```

```powershell
git add README.md
git commit -m "docs: link OSF project"
git push
```

---

## Part C：真实 DeepSeek V4 Flash 预实验（约 30 分钟 + API 成本）

### C1. 获取有效 DeepSeek API key

1. 打开 https://platform.deepseek.com/api_keys
2. 登录（没有账号先注册；建议用 +86 手机号或邮箱）
3. 点 **Create new secret key**
4. 填写：
   - **Name**：`echo-chambers-research`
   - **Permissions**：Full access
5. 点 **Create**，**复制 key**（仅显示一次）
6. **充值**：账户需要余额。V4 Flash 价格：
   - 缓存命中：$0.0028 / 1M token
   - 缓存未命中：$0.14 / 1M
   - 输出：$0.28 / 1M
7. **200 步预实验单条轨迹预计成本**：< $0.10
8. **完整预实验（6 cell × 5 重复）**：约 $3

### C2. 设置环境变量

```powershell
# 永久设置（重启 PowerShell 后仍生效）
[Environment]::SetEnvironmentVariable("DEEPSEEK_API_KEY", "sk-你的真实密钥", "User")
$env:DEEPSEEK_API_KEY="sk-你的真实密钥"

# 或当前会话
$env:DEEPSEEK_API_KEY="sk-你的真实密钥"
```

### C3. 验证密钥有效

```powershell
cd 'C:\Users\Administrator\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a5f55ec9ea42441f41e1208\pilot'
python run_pilot.py --model deepseek-v4-flash --task vending --condition isolated --steps 50 --seed 11 --health-check
```

预期输出（成功）：
```
[run] model=deepseek-v4-flash task=vending condition=isolated steps=50
[health] deepseek-v4-flash unreachable: ...   # 如果失败则看到这一行
[done] wrote pilot/outputs/...json              # 不管成功失败都会写
  final_balance = ...
```

**如果看到 `[health] ... unreachable`**：密钥无效或余额不足，回到 C1。

### C4. 跑 200 步预实验

```powershell
# 主模型：deepseek-v4-flash
python run_pilot.py --model deepseek-v4-flash --task vending --condition isolated --steps 200 --seed 11
python run_pilot.py --model deepseek-v4-flash --task vending --condition feedback --steps 200 --seed 11
python run_pilot.py --model deepseek-v4-flash --task vending --condition novelty --steps 200 --seed 11

# Thinking 模式对照
python run_pilot.py --model deepseek-v4-flash-thinking --task vending --condition isolated --steps 200 --seed 11

# 其他 3 模型（如果对应 key 也有）
python run_pilot.py --model claude-sonnet-4 --task vending --condition isolated --steps 200 --seed 11
python run_pilot.py --model gpt-4o --task vending --condition isolated --steps 200 --seed 11
```

### C5. 收集 + 分析

```powershell
cd 'C:\Users\Administrator\AppData\Roaming\TRAE SOLO CN\ModularData\ai-agent\work-mode-projects\6a5f55ec9ea42441f41e1208'
python pilot\collect_outputs.py
python analysis_skeleton.py --csv pilot\collected_trajectories.csv --out pilot\results --reference isolated
```

### C6. 把真实结果提交到 Git

```powershell
git add pilot/outputs/ pilot/results/ pilot/collected_trajectories.csv
git commit -m "pilot: real DeepSeek V4 Flash trajectories (200 steps, 6 cells)"
git push
```

---

## Part D：跨链接 GitHub ↔ OSF（5 分钟）

让 OSF 项目页面与 GitHub Release 互相可见。

### D1. 在 OSF 项目添加 GitHub 链接

1. 进 OSF 项目 → **Components**（或描述区） → 添加
   > Code & Data: https://github.com/yourname/echo-chambers-of-one

### D2. 在 GitHub 仓库 About 添加 OSF 链接

打开 https://github.com/yourname/echo-chambers-of-one → 右上角 ⚙ → **Social preview** / **Description** 中加入：
```
Pre-registration: https://osf.io/<your-id>/
```

---

## 验证清单

完成后打开 GitHub 仓库，应能看到：

- [ ] `research_proposal.html`、`preregistration.md`、`README.md` 在根目录
- [ ] `pilot/`、`smoke_test/`、`scripts/`、`osf/` 子目录
- [ ] `LICENSE` 文件
- [ ] 3 个 git commits（Initial / Add publish scripts / Add Release & lazy fallback）
- [ ] 标签 `v0.1-pre-reg` 显示在 Releases 页面
- [ ] Pre-release v0.1-pre-reg 有完整说明

打开 OSF 项目，应能看到：

- [ ] Wiki Home 已建好
- [ ] Files 下 21 个核心文件已上传
- [ ] Registrations 下有冻结的预注册记录（含 DOI）
- [ ] FAQ Wiki 页面（可选）

打开 Pilot 输出，应能看到：

- [ ] `pilot/outputs/` 下 6+ 个 JSON 轨迹文件
- [ ] `pilot/results/lmm_results.json` 是真实 LMM / OLS 估计结果
- [ ] `pilot/results/interaction_tests.csv` 显示 5 指标 × 6 cell 的 p 值

---

## 故障排查

| 现象 | 解决 |
|---|---|
| `git push` 报 403 | Token 没 `repo` 权限，或仓库没创建成功 |
| `osf login` 卡住 | 浏览器弹窗被拦截，允许弹出 |
| OSF 上传报错 | 检查 `--project` 参数；用 `--dry-run` 先看 |
| DeepSeek 401 | 重新创建 key 并检查账户余额 |
| DeepSeek 429 限流 | 等 1 分钟重试；或减少并发 |
| `pip install` 超时 | 换源：`pip install -i https://pypi.tuna.tsinghua.edu.cn/simple <pkg>` |

---

## 时间线同步

- **今日 (2026-07-22)**：完成 A、B、C 三件事
- **明日 (2026-07-23)**：内部审阅 `research_proposal.html` 与 `cover_letter.md`
- **7/28 - 8/04**：修改研究方案、补充作者信息
- **8/15 前**：AAMAS 2027 RR 通道确认
- **9/01 前后**：正式投 RR Stage 1
- **9 月**：启动 n=5/cell 预实验
- **10-12 月**：正式数据收集
- **2027-01**：Stage 2 论文撰写
- **2027-02**：Stage 2 投稿