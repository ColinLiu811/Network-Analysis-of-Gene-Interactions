# Sprint Four Deliverables: Advanced Network Analysis Features

This folder contains all deliverables from Sprint 4 - Advanced Network Analysis Features.

## Deliverables Structure

### Code Artifacts

- **`advanced_analysis.py`** - Complete advanced analysis module
  - Katz and Harmonic centrality measures
  - 3-node motif detection with significance testing
  - Path analysis (shortest paths, critical paths, diameter)
  - Network comparison tools
  - Statistical analysis (degree distribution, power-law fitting, small-world properties)
  - Centrality correlation analysis

- **`compute_centrality_optimized.py`** - Updated with new centrality measures
  - Added Katz centrality computation
  - Added Harmonic centrality computation
  - Integrated into parallel computation framework
  - Updated hub score calculation to optionally include new measures

### Documentation

- **`advanced_features_guide.md`** - Comprehensive guide for advanced features
  - Usage instructions for all new features
  - Code examples
  - Interpretation guidelines
  - Performance considerations

## New Features

### Additional Centrality Measures

1. **Katz Centrality**
   - Measures influence through multiple paths
   - Configurable attenuation factor
   - Integrated into parallel computation

2. **Harmonic Centrality**
   - Sum of reciprocals of shortest path distances
   - Measures how quickly information spreads
   - Handles disconnected graphs

### Network Motif Detection

- **3-node motif detection**: Identifies common subgraph patterns
- **Motif types**: no_edges, single_edge, two_edges, triangle
- **Significance testing**: Z-scores comparing to random networks
- **Sampling**: Automatic for large networks (>5000 nodes)

### Path Analysis

- **All-pairs shortest paths**: Distance analysis between all node pairs
- **Critical paths**: Longest shortest paths in the network
- **Diameter**: Longest shortest path
- **Path length distribution**: Histogram of path lengths
- **Average path length**: Mean shortest path distance

### Network Comparison

- **Node overlap**: Common and unique nodes between networks
- **Edge overlap**: Common and unique edges
- **Jaccard similarity**: Similarity coefficients for nodes and edges
- **Network statistics**: Density, size comparisons

### Statistical Analysis

- **Degree distribution**: Mean, median, std, histogram
- **Power-law fitting**: Fit degree distribution to power-law (gamma parameter)
- **Clustering statistics**: Average clustering, transitivity
- **Small-world properties**: Average path length, clustering coefficient
- **Centrality correlations**: Correlation matrix between centrality measures

## Usage

### Basic Usage

```python
from advanced_analysis import run_advanced_analysis
from build_graph import load_graph

# Load graph
G = load_graph('string_network.graphml')

# Run complete advanced analysis
results = run_advanced_analysis(G, output_dir='advanced_results')
```

### Individual Features

```python
from advanced_analysis import (
    detect_3node_motifs, 
    analyze_paths, 
    compare_networks,
    analyze_network_statistics
)

# Motif detection
motifs = detect_3node_motifs(G)
significance = compute_motif_significance(G, motifs)

# Path analysis
paths = analyze_paths(G)

# Network comparison
comparison = compare_networks(G1, G2)

# Statistical analysis
stats = analyze_network_statistics(G)
```

### New Centrality Measures

```python
from compute_centrality_optimized import compute_centrality_measures_optimized

# Include Katz and Harmonic centrality
df = compute_centrality_measures_optimized(
    G,
    measures=['degree', 'betweenness', 'katz', 'harmonic']
)
```

## Output Files

When running `run_advanced_analysis()`, the following files are generated:

- `katz_centrality.csv` - Katz centrality scores for all nodes
- `harmonic_centrality.csv` - Harmonic centrality scores
- `motif_analysis.csv` - Motif counts and Z-scores
- `path_analysis.csv` - Path statistics (average length, diameter, etc.)
- `network_statistics.csv` - Statistical metrics (power-law gamma, clustering, etc.)
- `centrality_correlations.csv` - Correlation matrix between centrality measures

## Dependencies

New dependency added:
- `scipy>=1.9.0` - For statistical analysis and curve fitting

Install with:
```bash
pip install -r requirements.txt
```

## Success Criteria Met

- [x] At least 2 new centrality measures implemented (Katz, Harmonic)
- [x] Motif detection works for small to medium networks
- [x] Path analysis provides meaningful insights
- [x] Network comparison tools functional
- [x] All new features documented with examples

## Files Summary

- **2 code modules**: `advanced_analysis.py`, updated `compute_centrality_optimized.py`
- **1 documentation file**: `advanced_features_guide.md`
- **Total**: 3 deliverable files

## Notes

- Motif detection uses sampling for large networks to manage computation time
- Path analysis is limited to 1000 nodes by default for large networks
- Harmonic centrality can be slow for very large networks
- All features maintain compatibility with existing pipeline
