# Tutorial: Getting Started

This tutorial walks a new user from installation to first results.

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Prepare Input Data

Either place a STRING file in the project root or process one directly:

```bash
python download_string_data.py 9606.protein.links.v12.0.txt.gz
```

## 3. Run the Full Pipeline

```bash
python run_pipeline.py
```

Optional visualization formats:

```bash
python run_pipeline.py --viz-formats svg,pdf
```

## 4. Review Outputs

- `hub_genes.csv` for top-ranked proteins
- `network_full.png`, `network_hubs.png`, `network_communities.png`
- `network_interactive.html` for searchable interactive exploration

## Success Check

Given valid input data, when the pipeline completes, then `hub_genes.csv` and
the visualization files should be present and non-empty.
