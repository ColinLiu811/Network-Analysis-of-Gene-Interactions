# Advanced Network Analysis Features Guide

## Overview

This guide documents the advanced network analysis features added in Sprint 4, including additional centrality measures, motif detection, path analysis, network comparison, and statistical analysis.

## New Centrality Measures

### Katz Centrality

Katz centrality measures the influence of a node based on the number of paths leading to it, with longer paths weighted less.

```python
from compute_centrality_optimized import compute_centrality_measures_optimized

# Include Katz centrality in computation
df = compute_centrality_measures_optimized(
    G, 
    measures=['degree', 'betweenness', 'katz']
)
```

**Use cases**: Identifying nodes that are influential through multiple indirect connections.

### Harmonic Centrality

Harmonic centrality is the sum of reciprocals of shortest path distances to all other nodes.

```python
# Include Harmonic centrality
df = compute_centrality_measures_optimized(
    G,
    measures=['degree', 'harmonic']
)
```

**Use cases**: Measuring how quickly information can spread from a node to all others.

## Network Motif Detection

Motifs are small subgraph patterns that occur more frequently than expected in random networks.

### 3-Node Motif Detection

```python
from advanced_analysis import detect_3node_motifs, compute_motif_significance

# Detect motifs
motif_results = detect_3node_motifs(G, sample_size=5000)

# Compute significance (Z-scores)
significance = compute_motif_significance(G, motif_results, n_random=100)
```

**Motif Types**:
- `no_edges`: Three unconnected nodes
- `single_edge`: One edge connecting two nodes
- `two_edges`: Two edges (chain)
- `triangle`: Three nodes fully connected

**Output**: Counts, frequencies, and Z-scores indicating statistical significance.

## Path Analysis

Analyze shortest paths and network structure.

### Features

- **All-pairs shortest paths**: Compute distances between all node pairs
- **Critical paths**: Identify longest shortest paths
- **Diameter**: Longest shortest path in the network
- **Path length distribution**: Histogram of path lengths

```python
from advanced_analysis import analyze_paths

path_results = analyze_paths(G, max_nodes=1000)
print(f"Average path length: {path_results['average_path_length']}")
print(f"Diameter: {path_results['diameter']}")
```

## Network Comparison

Compare two networks to identify similarities and differences.

```python
from advanced_analysis import compare_networks

comparison = compare_networks(G1, G2, name1="Disease Network", name2="Control Network")

print(f"Node Jaccard similarity: {comparison['node_overlap']['jaccard_similarity']}")
print(f"Edge Jaccard similarity: {comparison['edge_overlap']['jaccard_similarity']}")
```

**Metrics**:
- Node overlap (common, unique to each network)
- Edge overlap (common, unique edges)
- Jaccard similarity coefficients

## Statistical Analysis

Advanced statistical analysis of network topology.

### Features

- **Degree distribution**: Mean, median, std, histogram
- **Power-law fitting**: Fit degree distribution to power-law (P(k) ~ k^(-gamma))
- **Clustering statistics**: Average clustering, transitivity
- **Small-world properties**: Average path length, clustering coefficient

```python
from advanced_analysis import analyze_network_statistics

stats = analyze_network_statistics(G)
print(f"Power-law gamma: {stats['power_law']['gamma']}")
print(f"Is small-world: {stats['small_world']['is_small_world']}")
```

### Centrality Correlations

Analyze correlations between different centrality measures.

```python
from advanced_analysis import compute_centrality_correlations

# Requires centrality DataFrame
correlation_matrix = compute_centrality_correlations(centrality_df)
print(correlation_matrix)
```

## Complete Advanced Analysis

Run all advanced analyses at once:

```python
from advanced_analysis import run_advanced_analysis
from build_graph import load_graph

# Load graph
G = load_graph('string_network.graphml')

# Load centrality results (optional)
centrality_df = pd.read_csv('centrality_results.csv')

# Run complete analysis
results = run_advanced_analysis(G, centrality_df, output_dir='advanced_results')
```

This generates:
- `katz_centrality.csv` - Katz centrality scores
- `harmonic_centrality.csv` - Harmonic centrality scores
- `motif_analysis.csv` - Motif detection results with Z-scores
- `path_analysis.csv` - Path analysis statistics
- `network_statistics.csv` - Statistical analysis results
- `centrality_correlations.csv` - Correlation matrix

## Usage Examples

### Example 1: Motif Analysis

```python
from advanced_analysis import detect_3node_motifs, compute_motif_significance

motifs = detect_3node_motifs(G)
print(f"Triangles found: {motifs['counts'].get('triangle', 0)}")

significance = compute_motif_significance(G, motifs)
for motif_type, data in significance.items():
    print(f"{motif_type}: Z-score = {data['z_score']:.2f}")
```

### Example 2: Path Analysis

```python
from advanced_analysis import analyze_paths

paths = analyze_paths(G)
print(f"Average path length: {paths['average_path_length']:.2f}")
print(f"Network diameter: {paths['diameter']}")

# Critical paths (longest shortest paths)
for path_info in paths['critical_paths'][:5]:
    print(f"Path length {path_info['length']}: {path_info['source']} -> {path_info['target']}")
```

### Example 3: Network Comparison

```python
from advanced_analysis import compare_networks

# Compare two networks
comparison = compare_networks(network1, network2, "Disease", "Control")

print(f"Common nodes: {comparison['node_overlap']['common']}")
print(f"Common edges: {comparison['edge_overlap']['common']}")
print(f"Node similarity: {comparison['node_overlap']['jaccard_similarity']:.3f}")
```

## Performance Considerations

- **Motif detection**: For large networks (>5000 nodes), sampling is used automatically
- **Path analysis**: Limited to 1000 nodes by default for large networks
- **Harmonic centrality**: Can be slow for large networks; consider using NetworkX's built-in if available
- **Motif significance**: Random network generation can be time-consuming; reduce `n_random` for faster results

## Interpretation Guide

### Motif Z-Scores

- **Z-score > 2**: Motif occurs significantly more than expected (over-represented)
- **Z-score < -2**: Motif occurs significantly less than expected (under-represented)
- **-2 < Z-score < 2**: Motif frequency is not significantly different from random

### Power-Law Gamma

- **Gamma ~ 2-3**: Typical for scale-free networks (biological networks often fall here)
- **Higher gamma**: More uniform degree distribution
- **Lower gamma**: More extreme hub nodes

### Small-World Properties

A network is considered "small-world" if:
- High clustering coefficient (> 0.1)
- Short average path length (< log(n))

This indicates efficient information flow through the network.

## Integration with Pipeline

The advanced analysis can be integrated into the main pipeline:

```python
# After computing standard centrality
from compute_centrality_optimized import compute_centrality_measures_optimized
from advanced_analysis import run_advanced_analysis

# Standard analysis
centrality_df = compute_centrality_measures_optimized(G)

# Advanced analysis
advanced_results = run_advanced_analysis(G, centrality_df)
```

## References

- Katz Centrality: Katz, L. (1953). A new status index derived from sociometric analysis.
- Harmonic Centrality: Boldi, P., & Vigna, S. (2014). Axioms for centrality.
- Network Motifs: Milo, R., et al. (2002). Network motifs: simple building blocks of complex networks.
- Small-World Networks: Watts, D. J., & Strogatz, S. H. (1998). Collective dynamics of 'small-world' networks.
