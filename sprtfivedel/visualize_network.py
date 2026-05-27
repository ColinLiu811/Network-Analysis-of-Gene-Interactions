"""
Sprint 5 deliverable entry point for visualization.

This wrapper forwards execution to the root-level `visualize_network.py`
implementation so the Sprint 5 deliverables stay grouped under `sprtfivedel/`
without duplicating the large source file.
"""

from __future__ import annotations

import os
import runpy
import sys


if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target = os.path.join(repo_root, "visualize_network.py")
    sys.argv[0] = target
    runpy.run_path(target, run_name="__main__")
