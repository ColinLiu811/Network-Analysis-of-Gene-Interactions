# Protein-Protein Interaction Network Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.0+-green.svg)](https://networkx.org/)

A comprehensive Python toolkit for analyzing protein-protein interaction networks using data from the STRING database. This project identifies hub genes through network centrality analysis and visualizes the interaction network structure.

## 🎯 Overview

This project provides a complete pipeline for:
- **Downloading and processing** STRING database data for Homo sapiens
- **Building network graphs** from protein interaction data
- **Computing multiple centrality measures** to identify important nodes
- **Identifying hub genes** using composite scoring algorithms
- **Visualizing network structure**, communities, and hub genes
- **Generating comprehensive reports** and statistics

## ✨ Key Features

- 🔬 **Multiple Centrality Measures**: Degree, Betweenness, Closeness, Eigenvector, PageRank, and Clustering Coefficient
- 🎯 **Hub Gene Identification**: Composite scoring system combining multiple metrics
- 🧩 **Community Detection**: Louvain algorithm for identifying functional modules
- 📊 **Multiple Visualizations**: Static (PNG) and interactive (HTML) network visualizations
- 📈 **Comprehensive Analysis**: Full statistical summary of network properties
- 🔄 **Automated Pipeline**: One-command execution of the complete analysis workflow
- 📁 **Multiple Formats**: Support for GraphML and GEXF graph formats

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Output Files](#-output-files)
- [Dependencies](#-dependencies)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/ColinLiu811/Network-Analysis-of-Gene-Interactions.git
cd Network-Analysis-of-Gene-Interactions
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download STRING Data

You have two options:

**Option A: Manual Download (Recommended)**
1. Visit [STRING Database Downloads](https://string-db.org/cgi/download)
2. Select "Homo sapiens" (species ID: 9606)
3. Download "protein.links.full.v12.0" (or latest version)
4. Place the file (e.g., `9606.protein.links.v12.0.txt.gz`) in the project directory

**Option B: Use the Download Script**
```bash
python download_string_data.py
```

> **Note**: The download script may require API access or create a sample structure file. Manual download is recommended for full datasets.

## ⚡ Quick Start

### Automated Pipeline (Recommended)

Run the complete analysis pipeline with a single command:

```bash
python run_pipeline.py
```

Or with a STRING file:
```bash
python run_pipeline.py 9606.protein.links.v12.0.txt.gz
```

This will automatically:
1. Process the STRING data file
2. Clean and format the data
3. Build the network graph
4. Compute centrality measures
5. Identify hub genes
6. Generate all visualizations

### Manual Step-by-Step

If you prefer to run steps individually:

```bash
# Step 1: Process STRING data
python download_string_data.py 9606.protein.links.v12.0.txt.gz

# Step 2: Clean the data
python clean_data.py string_homo_sapiens.csv string_cleaned.csv

# Step 3: Build network graph
python build_graph.py string_cleaned.csv string_network.graphml

# Step 4: Compute centrality measures
python compute_centrality.py string_network.graphml 50

# Step 5: Visualize network
python visualize_network.py string_network.graphml hub_genes.csv
```

For more detailed instructions, see [QUICKSTART.md](QUICKSTART.md).

## 📖 Usage

### Command-Line Options

#### `download_string_data.py`
```bash
python download_string_data.py [input_file]
```
- If `input_file` is provided, processes the downloaded STRING file
- Otherwise, attempts to download via API

#### `clean_data.py`
```bash
python clean_data.py [input_file] [output_file]
```
- Default: `string_homo_sapiens.csv` → `string_cleaned.csv`
- Filters by confidence threshold (≥400)
- Removes duplicates and self-interactions

#### `build_graph.py`
```bash
python build_graph.py [input_file] [output_file]
```
- Default: `string_cleaned.csv` → `string_network.graphml`
- Creates undirected NetworkX graph
- Saves in GraphML format

#### `compute_centrality.py`
```bash
python compute_centrality.py [graph_file] [top_n]
```
- Default: `string_network.graphml` with top 50 hub genes
- Computes 6 centrality measures
- Generates composite hub scores

#### `visualize_network.py`
```bash
python visualize_network.py [graph_file] [hub_genes_file]
```
- Default: `string_network.graphml` and `hub_genes.csv`
- Creates 4 static visualizations and 1 interactive HTML

#### `run_pipeline.py`
```bash
python run_pipeline.py [string_file]
```
- Runs complete pipeline automatically
- Optional: provide STRING file path as argument

## 📁 Project Structure

```
Network-Analysis-of-Gene-Interactions/
├── download_string_data.py    # Download and process STRING database data
├── clean_data.py              # Clean and format data with Pandas
├── build_graph.py             # Build NetworkX graph from data
├── compute_centrality.py      # Calculate centrality measures and identify hubs
├── visualize_network.py       # Create network visualizations
├── run_pipeline.py            # Automated pipeline execution
│
├── data_processor.py           # Legacy: Data processing utilities
├── gene_network_analysis.py    # Legacy: Gene network analysis tool
├── network_analyzer.py         # Legacy: Network analysis functions
├── network_visualizer.py       # Legacy: Visualization utilities
├── report_generator.py         # Legacy: Report generation
├── generate_example_data.py    # Legacy: Example data generator
├── view_html.py               # Legacy: HTML viewer helper
│
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── QUICKSTART.md              # Quick start guide
├── CONTRIBUTING.md            # Contribution guidelines
├── CHANGELOG.md               # Project changelog
├── LICENSE                    # MIT License
│
├── docs/                      # Documentation
│   ├── PORTFOLIO.md          # Project portfolio
│   ├── PRESENTATION.md       # Presentation materials
│   └── PROJECT_ESSAY.md      # Project essay
│
└── lib/                       # Third-party libraries for visualizations
    ├── tom-select/
    └── vis-9.1.2/
```

## 📊 Output Files

After running the pipeline, you'll find the following output files:

### Data Files
- `string_homo_sapiens.csv` - Raw STRING interaction data (excluded from git)
- `string_cleaned.csv` - Cleaned and formatted interaction data (excluded from git)
- `string_network.graphml` - Network graph in GraphML format (excluded from git)
- `centrality_results.csv` - All centrality measures for each protein (excluded from git)
- `hub_genes.csv` - Ranked list of top hub genes (excluded from git)

### Visualizations
- `network_full.png` - Full network visualization with hub genes highlighted
- `network_hubs.png` - Hub gene network focusing on top hubs and neighbors
- `network_communities.png` - Community structure visualization
- `network_interactive.html` - Interactive network visualization (open in browser)
- `summary_plots.png` - Summary statistics plots (degree distribution, hub scores, etc.)

> **Note**: Large data files and generated outputs are excluded from git via `.gitignore`. Users need to run the pipeline to generate these files.

## 🔧 Dependencies

### Core Dependencies
- **pandas** ≥ 1.5.0 - Data manipulation and analysis
- **numpy** ≥ 1.21.0 - Numerical computations
- **networkx** ≥ 3.0 - Graph analysis and algorithms
- **matplotlib** ≥ 3.5.0 - Static visualizations

### Optional Dependencies
- **python-louvain** - Community detection (Louvain algorithm)
- **pyvis** ≥ 0.3.0 - Interactive HTML visualizations
- **requests** - API access for STRING database

Install all dependencies:
```bash
pip install -r requirements.txt
```

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide with troubleshooting
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guidelines for contributing
- **[CHANGELOG.md](CHANGELOG.md)** - Project version history

### Additional Documentation
See the `docs/` folder for:
- **PORTFOLIO.md** - Complete project portfolio with code examples
- **PRESENTATION.md** - Presentation materials
- **PROJECT_ESSAY.md** - Detailed project essay

## 🧪 Network Metrics Explained

### Degree Centrality
The number of direct connections a protein has. Proteins with high degree centrality interact with many other proteins and are likely key players in the network.

### Betweenness Centrality
Measures how often a protein lies on the shortest path between other proteins. High betweenness indicates proteins that act as bridges or bottlenecks in the network.

### Closeness Centrality
Measures how close a protein is to all other proteins in the network. Proteins with high closeness can quickly reach other proteins through the network.

### Eigenvector Centrality
Measures importance based on connections to important proteins. A protein is important if it's connected to other important proteins.

### PageRank
Google's algorithm adapted for networks. Measures the probability of reaching a protein through random walks.

### Clustering Coefficient
Measures how connected a protein's neighbors are to each other. High clustering indicates local network modules or communities.

## 🎓 Example Results

The analysis typically identifies:
- **19,488 proteins** in the human interactome
- **929,472 high-confidence interactions** (after filtering)
- **Top 50 hub genes** with composite scores
- **13+ communities** representing functional modules
- **Scale-free network structure** typical of biological networks

Hub genes typically have:
- 11.7× more connections than average
- Critical roles in network integrity
- Importance in disease and drug targeting

## ⚠️ Notes and Limitations

- **Large networks** (>10,000 nodes) may take significant time to process
- **Memory requirements**: ~1-3 GB for full human interactome
- **Visualizations** may be sampled for performance on large networks
- **Interactive visualizations** require pyvis package
- **STRING database** access may require registration for full datasets
- **Computation time**: Centrality computation can take 2-3 hours for large networks

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code style and standards
- How to submit pull requests
- Reporting issues
- Feature requests

## 📝 Citation

If you use this project in your research, please cite:

```bibtex
@software{protein_network_analysis,
  title = {Protein-Protein Interaction Network Analysis},
  author = {Liu, Colin},
  year = {2024},
  url = {https://github.com/ColinLiu811/Network-Analysis-of-Gene-Interactions}
}
```

## 🙏 Acknowledgments

- **[STRING Database](https://string-db.org/)** for providing comprehensive protein interaction data
- **[NetworkX](https://networkx.org/)** for powerful graph analysis tools
- **[Matplotlib](https://matplotlib.org/)** for static visualizations
- **[Pyvis](https://pyvis.readthedocs.io/)** for interactive network visualizations
- **[Pandas](https://pandas.pydata.org/)** for data processing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 References

- [STRING Database](https://string-db.org/) - Protein interaction database
- [NetworkX Documentation](https://networkx.org/) - Graph analysis library
- [STRING API](https://string-db.org/help/api/) - API documentation

## 📧 Contact

For questions, issues, or contributions, please:
- Open an [issue](https://github.com/ColinLiu811/Network-Analysis-of-Gene-Interactions/issues)
- Submit a [pull request](https://github.com/ColinLiu811/Network-Analysis-of-Gene-Interactions/pulls)
- Check the [documentation](docs/)

---

**Made with ❤️ for computational biology and network analysis**
