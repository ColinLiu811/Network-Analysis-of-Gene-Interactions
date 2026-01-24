# Protein-Protein Interaction Network Analysis

A comprehensive analysis of Homo sapiens protein-protein interactions using data from the STRING database. This project identifies hub genes through network centrality analysis and visualizes the interaction network structure.

## Project Overview

This project analyzes protein-protein interaction networks to:
1. Download and process STRING database data for Homo sapiens
2. Build network graphs from interaction data
3. Identify hub genes using centrality measures
4. Visualize network structure, communities, and hub genes

## Project Structure

```
indstudy/
├── download_string_data.py    # Download STRING database data
├── clean_data.py              # Clean and format data with Pandas
├── build_graph.py             # Build NetworkX graph from data
├── compute_centrality.py      # Calculate centrality measures and identify hubs
├── visualize_network.py       # Create network visualizations
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── PRESENTATION.md            # Presentation materials
```

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. For STRING data download:
   - Visit https://string-db.org/cgi/download
   - Download "protein.links.full.v11.5" for Homo sapiens (species ID: 9606)
   - Or use the download script (may require API access)

## Usage

### Step 1: Download STRING Data

```bash
python download_string_data.py
```

Or if you have a downloaded STRING file:
```bash
python download_string_data.py path/to/protein.links.v11.5.txt.gz
```

### Step 2: Clean the Data

```bash
python clean_data.py string_homo_sapiens.csv string_cleaned.csv
```

### Step 3: Build the Network Graph

```bash
python build_graph.py string_cleaned.csv string_network.graphml
```

### Step 4: Compute Centrality Measures

```bash
python compute_centrality.py string_network.graphml 50
```

### Step 5: Visualize the Network

```bash
python visualize_network.py string_network.graphml hub_genes.csv
```

## Output Files

- `string_homo_sapiens.csv`: Raw STRING interaction data
- `string_cleaned.csv`: Cleaned and formatted interaction data
- `string_network.graphml`: Network graph in GraphML format
- `centrality_results.csv`: All centrality measures for each protein
- `hub_genes.csv`: Ranked list of hub genes
- `network_full.png`: Full network visualization
- `network_hubs.png`: Hub gene network visualization
- `network_communities.png`: Community structure visualization
- `network_interactive.html`: Interactive network visualization
- `summary_plots.png`: Summary statistics plots

## Key Features

- **Multiple Centrality Measures**: Degree, Betweenness, Closeness, Eigenvector, PageRank
- **Hub Gene Identification**: Composite scoring system to identify most important genes
- **Community Detection**: Louvain algorithm for identifying network clusters
- **Multiple Visualizations**: Static and interactive network visualizations
- **Comprehensive Analysis**: Full statistical summary of network properties

## Dependencies

- pandas: Data manipulation and analysis
- numpy: Numerical computations
- networkx: Graph analysis and algorithms
- matplotlib: Static visualizations
- python-louvain: Community detection
- pyvis: Interactive visualizations
- requests: API access (optional)

## Notes

- Large networks may take significant time to process
- Some visualizations may be sampled for performance
- Interactive visualizations require pyvis package
- STRING database access may require registration for full datasets

## References

- STRING Database: https://string-db.org/
- NetworkX Documentation: https://networkx.org/
- STRING API: https://string-db.org/help/api/

