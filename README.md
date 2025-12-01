# Gene Interaction Network Analysis Tool

A comprehensive Python-based application for analyzing gene interaction networks using graph theory. This tool constructs, analyzes, and visualizes gene interaction networks from biological data, identifying key hub genes and computing important network metrics.

## Features

- **Data Input**: Accepts CSV/TSV files with gene interaction pairs
- **Data Preprocessing**: Removes duplicates and filters by confidence scores
- **Graph Construction**: Builds undirected networks using NetworkX
- **Network Analysis**: Computes multiple centrality metrics:
  - Degree centrality
  - Betweenness centrality
  - Closeness centrality
  - Clustering coefficient
- **Hub Gene Identification**: Ranks genes by importance
- **Visualization**: Creates static (PNG) and interactive (HTML) network visualizations
- **Comprehensive Reports**: Generates detailed analysis reports

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ColinLiu811/Network-Analysis-of-Gene-Interactions.git
cd Network-Analysis-of-Gene-Interactions
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Generate Example Data

First, generate some example interaction data:

```bash
python generate_example_data.py -n 100 -i 300 -o example_interactions.csv
```

This creates a CSV file with 100 genes and 300 interactions.

### 2. Run Analysis

Basic analysis without visualization:
```bash
python gene_network_analysis.py example_interactions.csv
```

With visualization (PNG):
```bash
python gene_network_analysis.py example_interactions.csv --visualize --format png
```

With interactive HTML visualization:
```bash
python gene_network_analysis.py example_interactions.csv --visualize --format html
```

With both visualization formats:
```bash
python gene_network_analysis.py example_interactions.csv --visualize --format both
```

### 3. Advanced Options

Filter by confidence score:
```bash
python gene_network_analysis.py example_interactions.csv -c 0.7 --visualize
```

Customize output directory and number of hub genes:
```bash
python gene_network_analysis.py example_interactions.csv -o results --top-hubs 20 --visualize
```

## Input File Format

The input CSV/TSV file should contain the following columns:

- **GeneA**: First gene in the interaction pair (required)
- **GeneB**: Second gene in the interaction pair (required)
- **Score**: Confidence/score for the interaction (optional)

Example:
```csv
GeneA,GeneB,Score
GENE_0001,GENE_0002,0.85
GENE_0001,GENE_0003,0.72
GENE_0002,GENE_0004,0.91
```

The tool will automatically:
- Remove duplicate interactions (A-B and B-A are treated as the same)
- Remove self-interactions
- Filter by confidence threshold if provided

## Output Files

The analysis generates the following files in the output directory (default: `output/`):

1. **cleaned_interactions.csv**: Preprocessed interaction data
2. **network_metrics.csv**: Complete centrality metrics for all genes
3. **network_visualization.png**: Static network visualization (if `--visualize` is used)
4. **network_visualization.html**: Interactive network visualization (if `--visualize --format html` is used)
5. **analysis_report.md**: Comprehensive markdown report with summary statistics and hub genes

## Command-Line Options

```
positional arguments:
  input_file            Path to input CSV/TSV file with gene interactions

optional arguments:
  -h, --help            Show help message
  -o, --output-dir      Output directory for results (default: output)
  -c, --confidence-threshold
                        Minimum confidence score threshold (default: 0.0)
  --top-hubs            Number of top hub genes to highlight (default: 10)
  --visualize           Generate network visualization
  --format {png,html,both}
                        Visualization format (default: png)
```

## Network Metrics Explained

### Degree Centrality
The number of direct connections a gene has. Genes with high degree centrality interact with many other genes and are likely key players in the network.

### Betweenness Centrality
Measures how often a gene lies on the shortest path between other genes. High betweenness indicates genes that act as bridges or bottlenecks in the network.

### Closeness Centrality
Measures how close a gene is to all other genes in the network. Genes with high closeness can quickly reach other genes through the network.

### Clustering Coefficient
Measures how connected a gene's neighbors are to each other. High clustering indicates local network modules or communities.

## Example Workflow

```bash
# 1. Generate example data
python generate_example_data.py -n 150 -i 400 -o my_data.csv

# 2. Run full analysis with visualizations
python gene_network_analysis.py my_data.csv \
    --visualize \
    --format both \
    --top-hubs 15 \
    -c 0.5 \
    -o results

# 3. View results
ls results/
# cleaned_interactions.csv
# network_metrics.csv
# network_visualization.png
# network_visualization.html
# analysis_report.md
```

## Project Structure

```
networkAnalysisOfGeneInteractions/
├── gene_network_analysis.py    # Main entry point
├── data_processor.py           # Data loading and preprocessing
├── network_analyzer.py         # Graph construction and metrics
├── network_visualizer.py       # Visualization generation
├── report_generator.py          # Report generation
├── generate_example_data.py    # Example data generator
├── view_html.py                # Helper script to view HTML in Codespaces
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Requirements

- Python 3.7+
- pandas >= 1.5.0
- networkx >= 3.0
- matplotlib >= 3.5.0
- numpy >= 1.21.0
- pyvis >= 0.3.0 (optional, for HTML visualizations)

## Notes

- Large networks (>1000 nodes) may take longer to process and visualize
- The spring layout algorithm is used for visualization, which may produce different layouts on each run
- Interactive HTML visualizations require pyvis and can be opened in any web browser
- The tool automatically handles both CSV and TSV formats

## Future Enhancements (Stretch Features)

Potential additions:
- Biological annotation integration (NCBI/UniProt APIs)
- Community detection and module visualization
- Network comparison tools (e.g., normal vs. tumor)
- Additional centrality metrics
- Export to other graph formats (GraphML, GEXF)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this tool in your research, please cite appropriately and acknowledge the use of NetworkX and other open-source libraries.

## Acknowledgments

- [NetworkX](https://networkx.org/) for graph analysis capabilities
- [Matplotlib](https://matplotlib.org/) for static visualizations
- [Pyvis](https://pyvis.readthedocs.io/) for interactive network visualizations
- [Pandas](https://pandas.pydata.org/) for data processing

