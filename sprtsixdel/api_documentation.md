# API Documentation (Sprint 6)

This document provides a practical API reference for the main modules in the
project. It is intended for users who want to run parts of the workflow
programmatically or understand data flow between scripts.

## Pipeline Overview

1. `download_string_data.py` -> produces `string_homo_sapiens.csv`
2. `clean_data.py` -> produces `string_cleaned.csv`
3. `build_graph.py` -> produces `string_network.graphml`
4. `compute_centrality.py` -> produces `centrality_results.csv`, `hub_genes.csv`
5. `visualize_network.py` -> produces PNG/HTML visual outputs
6. `run_pipeline.py` -> orchestrates end-to-end execution

## Module Reference

### `clean_data.py`
- Purpose: validate/filter raw interaction rows.
- Typical behavior:
  - filters low-confidence edges
  - removes duplicates and self-interactions
- Input: raw CSV
- Output: cleaned CSV suitable for graph construction

### `build_graph.py`
- Purpose: construct a NetworkX graph from cleaned interactions.
- Input: cleaned interaction CSV
- Output: GraphML (and optionally GEXF in some workflows)

### `compute_centrality.py`
- Purpose: compute centrality metrics and rank hub genes.
- Main outputs:
  - `centrality_results.csv`
  - `hub_genes.csv`
- Key metrics: degree, betweenness, closeness, eigenvector, PageRank,
  clustering coefficient, composite hub score.

### `advanced_analysis.py` / `sprtfourdel/advanced_analysis.py`
- Purpose: advanced analyses introduced in Sprint 4.
- Includes capabilities such as additional centrality/statistical analyses and
  feature-specific outputs for deeper biological interpretation.

### `visualize_network.py`
- Purpose: create static and interactive network visualizations.
- Notable CLI controls:
  - `--layout`, `--color-scheme`, `--dpi`, `--formats`
  - `--interactive-backend`, `--highlight-genes`, `--export-graph-data`

### `visualize_network_advanced.py`
- Purpose: convenience wrapper for presets and batch visualization.
- Presets:
  - `publication`
  - `slides`
  - `web`

### `run_pipeline.py`
- Purpose: execute all stages using `sys.executable` for portability.
- Notable flags:
  - `--config`
  - `--viz-formats`
  - `--version`

### `pipeline_config.py`
- Purpose: load and deep-merge YAML configuration against defaults.
- Typical usage:
  - `cfg = load_config("config.yaml")`

## Data Contracts

### Interaction CSV (cleaned)
Expected columns include identifiers for interacting proteins and an interaction
confidence metric.

### Centrality Output
`centrality_results.csv` should contain:
- `protein_id`
- centrality metric columns
- `hub_score`

`hub_genes.csv` is typically the top-N ranked subset.

## Programmatic Example

```python
from pipeline_config import load_config
import pandas as pd

cfg = load_config("config.yaml")
top_n = int(cfg["pipeline"]["top_n_hubs"])
hubs = pd.read_csv("hub_genes.csv").head(top_n)
print(hubs[["protein_id", "hub_score"]].head(10))
```
