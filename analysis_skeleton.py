"""
Echo Chambers of One — 统计代码骨架
====================================

本脚本实现预注册中的纵向混合效应分析模型。它读取统一格式的
轨迹级 CSV，包含以下列：

    trajectory_id   : str
    model           : str        # 模型标识
    condition       : str        # control, isolated, novelty, feedback, peer, human
    task            : str        # vending, alfworld, longmem, ...
    checkpoint      : int        # 0, 100, 500, 1000, 2000, 5000, 10000
    step_count      : int        # 实际累计步数
    accuracy        : float      # 推理正确率 (0-1)
    planning_score  : float      # 规划目标完成率 (0-1)
    decision_score  : float      # 决策累积回报 (任务相关归一化)
    calibration     : float      # 1 - ECE
    memory_score    : float      # 1 - 矛盾率
    survival_step   : float      # 首次不可恢复偏航步数；未发生记为 checkpoint*1.05
    seed            : int

主分析：
    对每个能力指标拟合线性混合效应模型
        y_{i,t} = β0 + β1·log(1+t) + β2·C_c + β3·log(1+t)·C_c
                  + u_model + u_task + u_run + ε
    并检验 β3 是否显著为负（隔离组斜率更陡）。

依赖：
    pip install pandas numpy statsmodels scikit-learn matplotlib seaborn ruptures lifelines
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------------------------
# 0. 命令行参数
# ---------------------------------------------------------------------------

parser = argparse.ArgumentParser(description="Echo Chambers 纵向分析")
parser.add_argument("--csv", type=Path, required=True, help="轨迹数据 CSV 路径")
parser.add_argument("--out", type=Path, required=True, help="输出目录")
parser.add_argument("--reference", default="isolated", help="参照条件（默认 isolated）")
parser.add_argument(
    "--outcomes",
    nargs="+",
    default=[
        "accuracy",
        "planning_score",
        "decision_score",
        "calibration",
        "memory_score",
    ],
    help="要分析的指标列名",
)
args = parser.parse_args()

args.out.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. 数据准备
# ---------------------------------------------------------------------------

def load_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    required = {
        "trajectory_id",
        "model",
        "condition",
        "task",
        "checkpoint",
        "accuracy",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV 缺少必备列: {missing}")
    df["log_step"] = np.log1p(df["checkpoint"])
    df = df.dropna(subset=["accuracy"])
    return df


def standardize_condition(df: pd.DataFrame, reference: str) -> pd.DataFrame:
    """将 condition 转换为相对参照条件的虚拟变量编码。"""
    df = df.copy()
    df["condition"] = pd.Categorical(df["condition"])
    levels = [c for c in df["condition"].cat.categories if c != reference]
    for level in levels:
        df[f"cond_{level}"] = (df["condition"] == level).astype(float)
        df[f"cond_{level}_x_logstep"] = df[f"cond_{level}"] * df["log_step"]
    return df


# ---------------------------------------------------------------------------
# 2. 主分析：线性混合效应模型
# ---------------------------------------------------------------------------

def fit_lmm(df: pd.DataFrame, outcome: str) -> tuple[dict, object]:
    """对单一指标拟合纵向 LMM 并返回关键统计量。

    鲁棒性策略：
    1. 先尝试默认 BFGS + REML（最稳定）。
    2. 出现奇异矩阵或 LinAlgError 时回退到 pooled OLS（仍能给出固定效应）。

    保护断言：
    - 每 cell 内轨迹数 < 5 时，直接走 pooled OLS，避免奇异矩阵。
    """
    import warnings

    predictors = [
        col
        for col in df.columns
        if col.startswith("cond_") and not col.endswith("_x_logstep")
    ]
    interactions = [f"{p}_x_logstep" for p in predictors]
    formula_parts = ["log_step"] + predictors + interactions
    fixed = " + ".join(formula_parts)
    formula = f"{outcome} ~ {fixed}"

    n_groups = int(df.groupby("trajectory_id").ngroups)
    low_power_cell = n_groups < 5

    base_summary = {
        "outcome": outcome,
        "n_obs": int(len(df)),
        "n_groups": n_groups,
        "low_power_cell": low_power_cell,
    }

    def _ols_fallback(reason: str) -> tuple[dict, object]:
        import statsmodels.api as sm

        X_cols = ["log_step"] + predictors + interactions
        X = sm.add_constant(df[X_cols])
        ols_result = sm.OLS(df[outcome], X).fit()
        summary = {
            **base_summary,
            "method": "ols_fallback",
            "fallback_reason": reason,
            "aic": float(ols_result.aic),
            "bic": float(ols_result.bic),
            "log_likelihood": float(ols_result.llf),
            "fixed_effects": ols_result.params.to_dict(),
            "fixed_effects_pvalues": ols_result.pvalues.to_dict(),
            "random_effects_var": float("nan"),
            "residual_var": float(ols_result.mse_resid),
        }
        return summary, ols_result

    if low_power_cell:
        return _ols_fallback(
            f"low_power_cell: n_groups={n_groups} < 5; skipping LMM/GEE"
        )

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            model = smf.mixedlm(
                formula,
                data=df,
                groups=df["trajectory_id"],
                re_formula="1",
            )
            result = model.fit(reml=True)
            summary = {
                **base_summary,
                "method": "mixedlm_reml",
                "converged": bool(result.converged),
                "aic": float(result.aic),
                "bic": float(result.bic),
                "log_likelihood": float(result.llf),
                "fixed_effects": result.fe_params.to_dict(),
                "fixed_effects_pvalues": result.pvalues.to_dict(),
                "random_effects_var": float(result.cov_re.iloc[0, 0]),
                "residual_var": float(result.scale),
            }
            return summary, result
        except Exception as exc:  # noqa: BLE001
            # 随机效应协方差奇异或奇异矩阵 → 回退到 GEE / OLS
            from statsmodels.genmod.generalized_estimating_equations import GEE
            from statsmodels.genmod.families import Gaussian
            from statsmodels.genmod.cov_struct import Independence

            try:
                gee = GEE.from_formula(
                    formula,
                    groups="trajectory_id",
                    data=df,
                    family=Gaussian(),
                    cov_struct=Independence(),
                )
                gee_result = gee.fit()
                summary = {
                    **base_summary,
                    "method": "gee_independence_fallback",
                    "fallback_reason": str(exc),
                    "aic": float("nan"),
                    "bic": float("nan"),
                    "log_likelihood": float("nan"),
                    "fixed_effects": gee_result.params.to_dict(),
                    "fixed_effects_pvalues": gee_result.pvalues.to_dict(),
                    "random_effects_var": float("nan"),
                    "residual_var": float(gee_result.scale),
                }
                return summary, gee_result
            except Exception as exc2:  # noqa: BLE001
                return _ols_fallback(f"{exc} | {exc2}")


def cohen_d_with_ci(values: np.ndarray, n_boot: int = 2000, seed: int = 0) -> dict:
    """为给定序列计算 Cohen's d 与 95% CI（bootstrap）。"""
    rng = np.random.default_rng(seed)
    mean = float(np.mean(values))
    sd = float(np.std(values, ddof=1))
    if sd == 0:
        return {"d": 0.0, "ci_low": 0.0, "ci_high": 0.0}
    d = mean / sd
    boots = []
    for _ in range(n_boot):
        sample = rng.choice(values, size=len(values), replace=True)
        m = sample.mean()
        s = sample.std(ddof=1)
        if s > 0:
            boots.append(m / s)
    if not boots:
        return {"d": d, "ci_low": d, "ci_high": d}
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return {"d": float(d), "ci_low": float(lo), "ci_high": float(hi)}


# ---------------------------------------------------------------------------
# 3. 多重比较校正（Holm-Bonferroni）
# ---------------------------------------------------------------------------

def holm_bonferroni(pvalues: list[float]) -> list[float]:
    """返回 Holm-Bonferroni 校正后的 p 值列表。"""
    n = len(pvalues)
    indexed = sorted(enumerate(pvalues), key=lambda x: x[1])
    adjusted = [0.0] * n
    running_max = 0.0
    for rank, (orig_idx, p) in enumerate(indexed):
        corrected = min(1.0, p * (n - rank))
        running_max = max(running_max, corrected)
        adjusted[orig_idx] = running_max
    return adjusted


# ---------------------------------------------------------------------------
# 4. 变点检测（探索性）
# ---------------------------------------------------------------------------

def detect_change_points(series: np.ndarray, pen: float = 10.0):
    """使用 PELT 算法对单条轨迹寻找变点。"""
    try:
        import ruptures as rpt
    except ImportError:
        return None
    algo = rpt.Pelt(model="rbf").fit(series.reshape(-1, 1))
    return algo.predict(pen=pen)


# ---------------------------------------------------------------------------
# 5. 失败模式聚类（探索性）
# ---------------------------------------------------------------------------

def cluster_failure_modes(df: pd.DataFrame, k: int = 5, seed: int = 0):
    """对轨迹摘要特征做 K-means 聚类。样本不足时降级为单簇。"""
    features = df.groupby("trajectory_id").agg(
        {
            "accuracy": ["mean", "std", "min"],
            "planning_score": ["mean", "std"],
            "memory_score": ["mean", "min"],
        }
    )
    features.columns = ["_".join(c) for c in features.columns]
    features = features.fillna(0.0)
    n = len(features)
    if n < 2:
        features["cluster"] = [0] * n
        return features.reset_index()
    effective_k = min(k, n)
    scaler = StandardScaler()
    X = scaler.fit_transform(features)
    model = KMeans(n_clusters=effective_k, n_init=10, random_state=seed)
    model.fit(X)
    features["cluster"] = model.labels_
    return features.reset_index()


# ---------------------------------------------------------------------------
# 6. 主流程
# ---------------------------------------------------------------------------

def main() -> None:
    df = load_data(args.csv)
    df = standardize_condition(df, args.reference)

    results = {}
    pvalue_records = []

    for outcome in args.outcomes:
        if outcome not in df.columns:
            print(f"[skip] {outcome} 不在数据中")
            continue
        sub = df.dropna(subset=[outcome])
        summary, fit = fit_lmm(sub, outcome)
        results[outcome] = summary

        # 记录交互项 p 值用于多重比较
        pvalues = summary.get("fixed_effects_pvalues") or fit.pvalues.to_dict()
        coefs = summary["fixed_effects"]
        for key, value in pvalues.items():
            if "_x_logstep" in key:
                pvalue_records.append(
                    {
                        "outcome": outcome,
                        "interaction": key,
                        "p_raw": float(value),
                        "coef": float(coefs[key]),
                    }
                )

    # Holm-Bonferroni 校正
    if pvalue_records:
        raw = [r["p_raw"] for r in pvalue_records]
        adjusted = holm_bonferroni(raw)
        for rec, p_adj in zip(pvalue_records, adjusted):
            rec["p_adjusted_holm"] = p_adj
            rec["significant_05"] = p_adj < 0.05

    # 探索性分析
    failure_clusters = cluster_failure_modes(df)

    # 报告输出
    (args.out / "lmm_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    pd.DataFrame(pvalue_records).to_csv(
        args.out / "interaction_tests.csv", index=False
    )
    failure_clusters.to_csv(args.out / "failure_clusters.csv", index=False)

    print(f"[done] 结果写入 {args.out}")
    print(json.dumps({k: v["fixed_effects"] for k, v in results.items()},
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()