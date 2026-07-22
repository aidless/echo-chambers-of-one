"""
OSF 上传脚本
============

需要先安装 osfclient 并登录：
    pip install osfclient
    osf login    # 浏览器授权后会保存 token

用法：
    python scripts/osf_upload.py --project echo-chambers-of-one

脚本会：
1. 找到 OSF 项目 ID
2. 上传所有文档到 OSF Files
3. 把当前 git tag 信息作为版本注释
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# 上传文件清单：本地路径 -> OSF 远端路径
UPLOAD_PLAN = [
    ("README.md", "README.md"),
    ("research_proposal.html", "research_proposal.html"),
    ("preregistration.md", "preregistration.md"),
    ("experiment_manifest.json", "experiment_manifest.json"),
    ("analysis_skeleton.py", "code/analysis_skeleton.py"),
    ("paper_outline.md", "paper_outline.md"),
    ("cover_letter.md", "cover_letter.md"),
    ("OSF_UPLOAD_CHECKLIST.md", "OSF_UPLOAD_CHECKLIST.md"),
    ("next_steps.md", "next_steps.md"),
    ("smoke_test/results/REPORT.md", "smoke_test/REPORT.md"),
    ("smoke_test/results/lmm_results.json", "smoke_test/lmm_results.json"),
    ("smoke_test/results/interaction_tests.csv", "smoke_test/interaction_tests.csv"),
    ("smoke_test/results/failure_clusters.csv", "smoke_test/failure_clusters.csv"),
    ("pilot/README.md", "pilot/README.md"),
    ("pilot/run_pilot.py", "pilot/run_pilot.py"),
    ("pilot/llm_client.py", "pilot/llm_client.py"),
    ("pilot/vending_env.py", "pilot/vending_env.py"),
    ("pilot/evaluator.py", "pilot/evaluator.py"),
    ("pilot/runner.py", "pilot/runner.py"),
    ("pilot/collect_outputs.py", "pilot/collect_outputs.py"),
    ("LICENSE", "LICENSE"),
]


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="上传项目文件到 OSF")
    parser.add_argument("--project", required=True, help="OSF 项目 ID 或短 slug")
    parser.add_argument("--dry-run", action="store_true", help="只打印要上传的文件清单")
    args = parser.parse_args()

    if args.dry_run:
        print("Dry run: 将上传以下文件到 OSF")
        for local, remote in UPLOAD_PLAN:
            local_path = REPO_ROOT / local
            if not local_path.exists():
                print(f"  [SKIP] {local} 不存在")
                continue
            print(f"  {local} -> {remote}")
        return

    # 实际上传需要 osfclient
    try:
        import osfclient  # noqa: F401
    except ImportError:
        print("[error] 请先安装 osfclient: pip install osfclient")
        print("[error] 并登录: osf login")
        return

    for local, remote in UPLOAD_PLAN:
        local_path = REPO_ROOT / local
        if not local_path.exists():
            print(f"[skip] {local} 不存在")
            continue
        run(["osf", "upload", args.project, str(local_path), "--destination", remote])


if __name__ == "__main__":
    main()