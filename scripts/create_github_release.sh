#!/usr/bin/env bash
# GitHub Release 创建脚本
# ----------------------
# 前提：已 push 标签 v0.1-pre-reg
# 用法：
#   export GITHUB_USER=yourname
#   export GITHUB_TOKEN=ghp_xxx   # 需要 repo 权限
#   bash scripts/create_github_release.sh

set -euo pipefail

: "${GITHUB_USER:?请先 export GITHUB_USER=yourname}"
: "${GITHUB_REPO:=echo-chambers-of-one}"
: "${GITHUB_TOKEN:?请先 export GITHUB_TOKEN=ghp_xxx}"

REPO="${GITHUB_USER}/${GITHUB_REPO}"
TAG="v0.1-pre-reg"
TITLE="Echo Chambers of One · v0.1-pre-reg · Pre-registration Stage 1"
NOTES_FILE="$(dirname "$0")/../RELEASE_NOTES_v0.1-pre-reg.md"

echo "[1/3] 检查标签是否存在..."
if ! git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "标签 $TAG 不存在，先创建："
    git tag -a "$TAG" -m "Pre-registration Stage 1 — frozen 2026-07-22"
    git push origin "$TAG"
fi

echo "[2/3] 创建 Release..."
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    gh release create "$TAG" \
        --repo "$REPO" \
        --title "$TITLE" \
        --notes-file "$NOTES_FILE" \
        --prerelease \
        --target main
else
    echo "[info] gh CLI 未认证，使用 curl + API 直接创建"
    curl -sSL \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        -H "Accept: application/vnd.github+json" \
        -X POST \
        "https://api.github.com/repos/${REPO}/releases" \
        -d @- <<EOF
{
  "tag_name": "${TAG}",
  "target_commitish": "main",
  "name": "${TITLE}",
  "body": $(python -c "import json,sys; print(json.dumps(open(sys.argv[1],encoding='utf-8').read()))" "$NOTES_FILE"),
  "prerelease": true,
  "draft": false
}
EOF
fi

echo "[3/3] 完成。"
echo "Release URL: https://github.com/${REPO}/releases/tag/${TAG}"