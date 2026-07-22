#!/usr/bin/env bash
# GitHub 推送脚本
# ----------------
# 前提：已在 GitHub 创建空仓库 echo-chambers-of-one（不要勾选 README / .gitignore / LICENSE）
# 用法：
#   GITHUB_USER=yourname bash scripts/publish_to_github.sh

set -euo pipefail

: "${GITHUB_USER:?请设置 GITHUB_USER 环境变量，例如 export GITHUB_USER=yourname}"
: "${GITHUB_REPO:=echo-chambers-of-one}"

REMOTE_URL="https://github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

echo "[1/4] 检查 git 状态..."
git status --porcelain

echo "[2/4] 添加远程..."
if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "$REMOTE_URL"
else
    git remote add origin "$REMOTE_URL"
fi

echo "[3/4] 推送 main + v0.1-pre-reg 标签..."
git push -u origin main
git push origin v0.1-pre-reg

echo "[4/4] 设置默认分支为 main..."
gh repo edit "${GITHUB_USER}/${GITHUB_REPO}" --default-branch main 2>/dev/null || true

echo
echo "完成。访问：${REMOTE_URL}"
echo "在 GitHub 仓库设置中："
echo "  - About: 添加描述 'Longitudinal degradation under interaction deprivation in language agents'"
echo "  - Topics: agent-degradation, long-horizon, interaction-deprivation, preregistration"
echo "  - Enable Discussions（可选）"