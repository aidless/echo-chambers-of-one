# 本仓没有既有单测套件（CI 只做 byte-compile 与链接检查），
# 因此 eval 目标只跑 eval/cases.jsonl 的验收题库，跑它真实调用 pilot/ 与 analysis_skeleton.py 的 API。
.PHONY: eval

eval:
	python3 eval/run_cases.py
