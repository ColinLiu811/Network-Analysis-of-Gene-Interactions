# Visualization guide (Sprint 5)

This guide covers interactive and static network figures, export formats, configuration, and the advanced visualization entry point.

## `visualize_network.py`

Generates:

- **Static**: `network_full.png`, `network_hubs.png`, `network_communities.png`, `summary_plots.png`
- **Interactive**: `network_interactive.html` (vis.js by default: search, degree / betweenness filters, zoom/pan, tooltips)
- **Optional**: `network_interactive_pyvis.html` when using `--interactive-backend pyvis` or `both`
- **Optional exports**: GraphML, GEXF, and node-link JSON when using `--export-graph-data` (`network_export.*`)

### Common options

| Option | Description |
|--------|-------------|
| `--layout` | `spring`, `circular`, `kamada_kawai`, `spectral` (full-network static layout) |
| `--color-scheme` | `hub` (hubs vs others) or `community` (Louvain / greedy modularity) |
| `--dpi` | Resolution for raster figures (PNG); default 300 |
| `--formats` | Comma-separated **extra** formats for static figures: `png`, `svg`, `pdf` (same basename as the PNG) |
| `--highlight-genes` | Text file of protein IDs (one per line or comma-separated) drawn in **orange** on the full network |
| `--centrality-csv` | Defaults to `centrality_results.csv`; powers interactive tooltips and betweenness filter |
| `--interactive-max-nodes` | Cap nodes in the HTML (sampling) |
| `--interactive-backend` | `visjs` (default), `pyvis`, or `both` |
| `--export-graph-data` | Write `network_export.graphml`, `network_export.gexf`, `network_export_nodelink.json` |
| `--config` | YAML file; can set `visualization.dpi`, `layout`, `color_scheme` (see `config.default.yaml`) |

Examples:

```bash
python visualize_network.py string_network.graphml hub_genes.csv --formats svg,pdf --dpi 600
python visualize_network.py --color-scheme community --layout kamada_kawai
python visualize_network.py --highlight-genes my_genes.txt --export-graph-data
```

## `visualize_network_advanced.py`

Presets and batch-style defaults:

- **`--preset publication`**: DPI 600, PNG/SVG/PDF, plus `--export-graph-data`
- **`--preset slides`**: DPI 200, PNG/PDF
- **`--preset web`**: DPI 150, PNG/SVG
- **`--batch`**: PNG/SVG/PDF and graph data export (can be combined with a preset)

Forward extra arguments to `visualize_network.py` after `--`:

```bash
python visualize_network_advanced.py --preset web -- --color-scheme community
```

## `run_pipeline.py`

Runs the full pipeline using `sys.executable` for subprocesses (portable Python).

| Option | Description |
|--------|-------------|
| `--config` | YAML config; sets `top_n_hubs` for centrality and forwards to `visualize_network` |
| `--viz-formats` | Passed to `visualize_network` as `--formats` (e.g. `svg,pdf`) |

```bash
python run_pipeline.py 9606.protein.links.v12.0.txt.gz --viz-formats svg,pdf --config config.yaml
```

## Configuration file

Copy `config.default.yaml` to `config.yaml` and edit. Keys under `visualization` match the pipeline defaults documented above; `pipeline.top_n_hubs` controls how many hubs are written and emphasized.

PyYAML is required for YAML loading (`pip install -r requirements.txt`).

## Interactive HTML behavior

The default **vis.js** page includes:

- **Search**: show only nodes whose ID contains the query (case-insensitive)
- **Min degree** / **Min betweenness**: hide nodes below thresholds (betweenness is scaled from your network max)
- **Navigation**: mouse wheel zoom, drag background to pan, drag nodes; keyboard shortcuts when the canvas is focused (vis.js defaults)

If `centrality_results.csv` is missing, degree still works; betweenness in tooltips and filters may be zero.
