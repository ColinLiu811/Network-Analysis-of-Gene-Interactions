# Reproducibility Guide

## Goals

- Re-run analyses with equivalent outputs under equivalent inputs/configs.
- Preserve enough metadata to explain environment-dependent differences.

## Recommended Steps

1. Use an isolated environment (`venv`, conda, or container).
2. Record runtime metadata before analysis (`run_metadata_capture.py`).
3. Store config files with every run.
4. Save output fingerprints (hashes) for key artifacts.
5. Generate validation summary with `stability_analysis.py`.

## Minimum Run Metadata

- command invoked
- UTC timestamp
- OS and Python version
- installed packages snapshot
- input file paths and SHA256 hashes
- output file paths and SHA256 hashes

## Folder Convention

Example:

```text
runs/
  2026-04-26_runA/
    config.yaml
    metadata.json
    centrality_results.csv
    hub_genes.csv
    validation_summary.json
```

## Practical Acceptance

Given identical inputs and config, when rerun in controlled environment, then
top-N overlap and rank-correlation targets from `validation_framework.md` should
meet acceptance thresholds.
