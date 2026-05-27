"""
Validation utility for comparing two analysis runs.

Computes:
- top-N hub overlap (Jaccard)
- Spearman rank correlation over shared proteins (if available)
"""

from __future__ import annotations

import argparse
import json
from typing import Dict, List, Set

import pandas as pd


def jaccard(a: Set[str], b: Set[str]) -> float:
    union = a | b
    return len(a & b) / len(union) if union else 0.0


def rank_spearman(df_a: pd.DataFrame, df_b: pd.DataFrame) -> float:
    if "protein_id" not in df_a.columns or "protein_id" not in df_b.columns:
        return float("nan")
    if "hub_score" not in df_a.columns or "hub_score" not in df_b.columns:
        return float("nan")

    a = df_a[["protein_id", "hub_score"]].copy()
    b = df_b[["protein_id", "hub_score"]].copy()
    merged = a.merge(b, on="protein_id", suffixes=("_a", "_b"))
    if merged.empty:
        return float("nan")
    return float(merged["hub_score_a"].corr(merged["hub_score_b"], method="spearman"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare hub and centrality outputs from two runs.")
    parser.add_argument("hub_a")
    parser.add_argument("hub_b")
    parser.add_argument("--top-n", type=int, default=50)
    parser.add_argument("--centrality-a", default=None)
    parser.add_argument("--centrality-b", default=None)
    parser.add_argument("--out", default="validation_summary.json")
    args = parser.parse_args()

    hub_a = pd.read_csv(args.hub_a)
    hub_b = pd.read_csv(args.hub_b)
    set_a = set(map(str, hub_a["protein_id"].head(args.top_n).tolist()))
    set_b = set(map(str, hub_b["protein_id"].head(args.top_n).tolist()))
    overlap = jaccard(set_a, set_b)

    summary: Dict[str, float] = {
        "top_n": float(args.top_n),
        "top_n_jaccard": overlap,
    }

    if args.centrality_a and args.centrality_b:
        c_a = pd.read_csv(args.centrality_a)
        c_b = pd.read_csv(args.centrality_b)
        summary["spearman_hub_score"] = rank_spearman(c_a, c_b)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))
    print(f"Wrote summary to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
