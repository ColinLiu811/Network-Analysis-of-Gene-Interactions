"""
Basic scripted pipeline example.

This script demonstrates how to run the project pipeline stages from Python.
It is intended as a template for custom automation, not a replacement for
`run_pipeline.py`.
"""

from __future__ import annotations

import subprocess
import sys
from typing import List


def run(cmd: List[str]) -> None:
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    py = sys.executable

    # Example commands assume the default intermediate filenames.
    run([py, "clean_data.py", "string_homo_sapiens.csv", "string_cleaned.csv"])
    run([py, "build_graph.py", "string_cleaned.csv", "string_network.graphml"])
    run([py, "compute_centrality.py", "string_network.graphml", "50"])
    run([py, "visualize_network.py", "string_network.graphml", "hub_genes.csv"])

    print("Pipeline example completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
