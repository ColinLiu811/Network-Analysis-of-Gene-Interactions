# Tutorial: Analyzing Your Own Data

Use this guide when your interaction data is not from the default example flow.

## 1. Format Expectations

Your cleaned interaction file should include:
- source protein identifier
- target protein identifier
- confidence or weight-like interaction field

If starting from STRING downloads, prefer using `download_string_data.py` and
`clean_data.py` so formatting is consistent with downstream scripts.

## 2. Build and Analyze

```bash
python clean_data.py my_raw_data.csv my_cleaned.csv
python build_graph.py my_cleaned.csv my_network.graphml
python compute_centrality.py my_network.graphml 100
```

## 3. Visualize With Custom Options

```bash
python visualize_network.py my_network.graphml hub_genes.csv \
  --layout kamada_kawai \
  --color-scheme community \
  --formats svg,pdf \
  --dpi 600
```

## 4. Optional Config-Driven Run

```bash
cp config.default.yaml config.yaml
python run_pipeline.py --config config.yaml
```

## Success Check

Given valid custom data, when all stages run successfully, then centrality
results and visual outputs should be generated without manual file edits.
