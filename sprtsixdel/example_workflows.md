# Example Workflows

This document provides complete workflow templates for common use cases.

## Workflow 1: STRING Download to Publication-Ready Figures

```bash
python download_string_data.py 9606.protein.links.v12.0.txt.gz
python clean_data.py string_homo_sapiens.csv string_cleaned.csv
python build_graph.py string_cleaned.csv string_network.graphml
python compute_centrality.py string_network.graphml 50
python visualize_network_advanced.py --preset publication string_network.graphml hub_genes.csv
```

Expected result:
- high-resolution figures (PNG/SVG/PDF) and graph exports suitable for reports.

## Workflow 2: Compare Two Networks (Disease A vs Disease B)

1. Build two graph files: `disease_a.graphml`, `disease_b.graphml`
2. Run:

```bash
python examples/compare_networks_example.py disease_a.graphml disease_b.graphml
```

Expected result:
- console report of overlap and basic graph statistics.

## Workflow 3: Identify Candidate Drug Targets From Hub Signals

1. Ensure `hub_genes.csv` exists.
2. Run:

```bash
python examples/identify_drug_targets_example.py hub_genes.csv 25
```

Expected result:
- ranked shortlist for follow-up curation and literature review.

## Workflow 4: Temporal/Iterative Analysis Template

If you have time-stamped snapshots, repeat the core pipeline per snapshot and
store outputs in timestamped folders, then compare hub stability across runs.
The `examples/basic_pipeline_example.py` script provides an automation baseline.
