# Validation Framework

## Objective

Ensure that identified hub genes are stable, explainable, and comparable across
experimental conditions.

## Core Validation Checks

1. **Top-N Overlap Stability**
   - Compare top-N hubs from two runs using Jaccard overlap.
   - Acceptance target: overlap >= 0.70 for same inputs/settings.

2. **Rank Correlation**
   - Compare `hub_score` rankings across reruns.
   - Use Spearman correlation where applicable.
   - Acceptance target: rho >= 0.80 for same inputs/settings.

3. **Metric Consistency**
   - Check if top hubs are repeatedly high across key metrics
     (`degree_centrality`, `betweenness_centrality`, `pagerank`).
   - Acceptance target: majority of top-20 hubs appear in at least 2 metric top-20 lists.

4. **Parameter Sensitivity**
   - Evaluate impact of parameter changes (e.g., top_n_hubs, confidence thresholds).
   - Report shifts in top-N overlap and score distribution.

## Run Protocol

- Keep a per-run metadata file (environment + inputs + command).
- Use consistent seed controls where algorithms support seeding.
- Save outputs in timestamped run directories.

## Report Requirements

Each validation run should report:
- run identifiers and config
- stability metrics (overlap, rank correlation)
- observed deviations and interpretation
- pass/fail against acceptance targets
