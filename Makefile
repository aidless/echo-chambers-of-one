# Offline checks. `check` does not contact OSF, arXiv, or a model API.
# CPython 3.12 and the pins in requirements.txt are required.
.PHONY: eval check

check:
	python3 checks/validate_manifest.py
	python3 checks/parameter_recovery.py
	python3 checks/honesty.py

eval:
	python3 eval/run_cases.py
