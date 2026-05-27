"""
Example: shortlist candidate targets from hub gene rankings.
"""

from __future__ import annotations

import argparse
import pandas as pd


def main() -> int:
    parser = argparse.ArgumentParser(description="Shortlist top hub candidates.")
    parser.add_argument("hub_csv", help="Path to hub_genes.csv")
    parser.add_argument("top_n", type=int, nargs="?", default=20)
    args = parser.parse_args()

    df = pd.read_csv(args.hub_csv)
    required = ["protein_id", "hub_score"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    shortlist = df.sort_values("hub_score", ascending=False).head(args.top_n)
    print(shortlist[["protein_id", "hub_score"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
