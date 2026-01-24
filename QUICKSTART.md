# Quick Start Guide

## Installation

1. **Install Python 3.8+** (if not already installed)

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Getting STRING Data

You have two options:

### Option 1: Manual Download (Recommended)

1. Visit https://string-db.org/cgi/download
2. Select "Homo sapiens" (species ID: 9606)
3. Download "protein.links.full.v11.5" (or latest version)
4. The file will be named something like `9606.protein.links.v11.5.txt.gz`
5. Place it in this directory

Then process it:
```bash
python download_string_data.py 9606.protein.links.v11.5.txt.gz
```

### Option 2: Use the Download Script

```bash
python download_string_data.py
```

Note: This may require API access or may create a sample structure file.

## Running the Analysis

### Method 1: Run Complete Pipeline

```bash
python run_pipeline.py
```

This will run all steps automatically.

### Method 2: Run Steps Individually

**Step 1: Clean the data**
```bash
python clean_data.py string_homo_sapiens.csv string_cleaned.csv
```

**Step 2: Build the graph**
```bash
python build_graph.py string_cleaned.csv string_network.graphml
```

**Step 3: Compute centrality measures**
```bash
python compute_centrality.py string_network.graphml 50
```

**Step 4: Create visualizations**
```bash
python visualize_network.py string_network.graphml hub_genes.csv
```

## Expected Output Files

After running the pipeline, you should have:

- `string_cleaned.csv` - Cleaned interaction data
- `string_network.graphml` - Network graph file
- `centrality_results.csv` - All centrality measures
- `hub_genes.csv` - Top hub genes ranked
- `network_full.png` - Full network visualization
- `network_hubs.png` - Hub gene network
- `network_communities.png` - Community structure
- `network_interactive.html` - Interactive visualization (if pyvis installed)
- `summary_plots.png` - Summary statistics

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "File not found" errors
Make sure you've downloaded the STRING data file first.

### Visualization is slow or crashes
- The network may be too large
- Try sampling a subset of the data
- Reduce the number of nodes in visualizations

### Memory errors
- Process a smaller subset of data
- Increase system memory if possible
- Use a machine with more RAM

## Next Steps

1. Review `hub_genes.csv` to see top hub genes
2. Open `network_interactive.html` in a web browser
3. Review the visualizations in the PNG files
4. Use `PRESENTATION.md` to prepare your presentation

## Getting Help

- Check the README.md for detailed documentation
- Review PRESENTATION.md for project context
- Check STRING database documentation: https://string-db.org/help/

