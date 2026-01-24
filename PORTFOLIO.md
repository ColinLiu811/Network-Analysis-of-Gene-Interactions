# Protein-Protein Interaction Network Analysis Portfolio
## Hub Gene Identification in Homo sapiens

**Project Type:** Computational Biology / Network Analysis  
**Tools:** Python, Pandas, NetworkX, Matplotlib  
**Data Source:** STRING Database v12.0  
**Date:** December 2024

---

## Project Overview

This project analyzes the complete protein-protein interaction network for Homo sapiens to identify hub genes—proteins that play critical roles in network structure and cellular function. Using network analysis techniques, we processed over 13 million interactions from the STRING database, built a comprehensive network graph, and identified the most important hub genes using multiple centrality measures.

### Objectives

- Download and process STRING database data for Homo sapiens
- Build a network graph representation of protein interactions
- Compute multiple centrality measures to identify important nodes
- Identify and rank hub genes
- Visualize network structure, communities, and hub genes

---

## Build Process

### Step 1: Data Acquisition
Downloaded and processed STRING database file (`9606.protein.links.full.v12.0.txt.gz`), extracting 13.7 million interactions and 19,622 unique proteins.

```python
# Process gzipped STRING file
import gzip
import pandas as pd

with gzip.open('9606.protein.links.full.v12.0.txt.gz', 'rt') as f:
    df = pd.read_csv(f, sep=' ')
    df = df[['protein1', 'protein2', 'combined_score']]
    df.to_csv('string_homo_sapiens.csv', index=False)
```

### Step 2: Data Cleaning
Filtered interactions by confidence threshold (≥400), removed duplicates and self-interactions, and standardized protein identifiers. **Result:** 929,472 high-confidence interactions (6.8% of original), 19,488 proteins retained (99.3%).

```python
# Filter by confidence threshold
df = df[df['combined_score'] >= 400]  # Medium+ confidence

# Remove species prefix from protein IDs
df['protein1_clean'] = df['protein1'].str.replace(r'^\d+\.', '', regex=True)
df['protein2_clean'] = df['protein2'].str.replace(r'^\d+\.', '', regex=True)

# Remove self-interactions
df = df[df['protein1_clean'] != df['protein2_clean']]

# Remove duplicate interactions (A-B same as B-A)
df['pair'] = df.apply(lambda x: tuple(sorted([x['protein1_clean'], 
                                               x['protein2_clean']])), axis=1)
df = df.drop_duplicates(subset=['pair'])
```

### Step 3: Network Construction
Built undirected NetworkX graph with 19,488 nodes and 929,472 edges. Network properties: average degree 95.39, density 0.004895, 2 connected components (largest: 99.99% of network).

```python
import networkx as nx

# Create undirected graph
G = nx.Graph()

# Add edges with weights
for _, row in df.iterrows():
    G.add_edge(row['protein1_clean'], row['protein2_clean'], 
               weight=row['combined_score'])

# Save in GraphML format
nx.write_graphml(G, 'string_network.graphml')
```

### Step 4: Centrality Computation
Computed six centrality measures for all nodes: degree, betweenness (sampled k=100), closeness, eigenvector, PageRank, and clustering coefficient. Generated composite hub score by normalizing and averaging key measures. **Runtime:** ~2.5 hours.

```python
# Compute multiple centrality measures
degree_centrality = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G, k=100)  # Sampling for efficiency
closeness = nx.closeness_centrality(subgraph)
eigenvector = nx.eigenvector_centrality(G)
pagerank = nx.pagerank(G)
clustering = nx.clustering(G)

# Composite hub score (normalized average)
normalized_measures = ['degree_centrality', 'betweenness_centrality', 
                       'eigenvector_centrality', 'pagerank']
for col in normalized_measures:
    df[f'{col}_normalized'] = df[col] / df[col].max()
df['hub_score'] = df[[f'{c}_normalized' for c in normalized_measures]].mean(axis=1)
```

### Step 5: Hub Gene Identification
Ranked proteins by composite hub score and identified top 50 hub genes using 95th percentile threshold. Top hub: ENSP00000269305 with 2,267 interactions and hub score 1.0000.

```python
# Rank by hub score and identify top hubs
df = df.sort_values('hub_score', ascending=False)
hub_score_threshold = df['hub_score'].quantile(0.95)
top_hubs = df.head(50)
```

### Step 6: Visualization
Created 4 static visualizations (full network, hub network, communities, summary plots) and 1 interactive HTML visualization using Pyvis.

```python
# Community detection using Louvain algorithm
import community.community_louvain as community_louvain
communities = community_louvain.best_partition(G)

# Create interactive visualization with Pyvis
from pyvis.network import Network
net = Network(height='800px', width='100%', bgcolor='#222222', font_color='white')
net.from_nx(G)
net.show('network_interactive.html')
```

---

## Results & Findings

### Network Statistics

| Metric | Value |
|--------|-------|
| **Total Nodes (Proteins)** | 19,488 |
| **Total Edges (Interactions)** | 929,472 |
| **Average Degree** | 95.39 |
| **Graph Density** | 0.004895 |
| **Connected Components** | 2 |
| **Largest Component** | 19,486 nodes (99.99%) |

### Data Processing Summary

| Stage | Interactions | Proteins | Confidence (Median) |
|-------|--------------|----------|---------------------|
| **Initial Raw Data** | 13,715,404 | 19,622 | 209.00 |
| **After Cleaning** | 929,472 | 19,488 | 541.00 |
| **Reduction** | 93.2% removed | 0.7% removed | +159% increase |

### Top 10 Hub Genes

| Rank | Protein ID | Degree | Hub Score | Degree Centrality |
|------|------------|--------|-----------|-------------------|
| 1 | ENSP00000269305 | 2,267 | 1.0000 | 0.1163 |
| 2 | ENSP00000380070 | 1,937 | 0.8250 | 0.0994 |
| 3 | ENSP00000494750 | 1,852 | 0.7387 | 0.0950 |
| 4 | ENSP00000451828 | 1,820 | 0.7166 | 0.0934 |
| 5 | ENSP00000388107 | 1,563 | 0.6856 | 0.0802 |
| 6 | ENSP00000272317 | 1,545 | 0.6549 | 0.0793 |
| 7 | ENSP00000495360 | 1,547 | 0.6483 | 0.0794 |
| 8 | ENSP00000275493 | 1,527 | 0.6306 | 0.0784 |
| 9 | ENSP00000478887 | 1,579 | 0.6218 | 0.0810 |
| 10 | ENSP00000362680 | 1,451 | 0.5592 | 0.0745 |

### Key Findings

1. **Hub Gene Dominance:** Hub genes have 11.7× more connections than average (1,118.9 vs 95.39). Top hub has 2,267 interactions (24× the average).

2. **Network Structure:** Hub genes represent 0.26% of nodes but 3.01% of connections, demonstrating scale-free network structure.

3. **Community Structure:** 13 communities detected using Louvain algorithm, likely representing functional modules. Hub genes often connect multiple communities.

---

## Technical Implementation

### Technology Stack
Python 3.13, Pandas, NetworkX, Matplotlib, Pyvis, python-louvain, SciPy

### Pipeline
STRING Database → Data Download → Cleaning (confidence ≥400) → Graph Construction → Centrality Computation → Hub Identification → Visualization

```python
# Automated pipeline execution
python3 download_string_data.py 9606.protein.links.full.v12.0.txt.gz
python3 clean_data.py string_homo_sapiens.csv string_cleaned.csv
python3 build_graph.py string_cleaned.csv string_network.graphml
python3 compute_centrality.py string_network.graphml 50
python3 visualize_network.py string_network.graphml hub_genes.csv
```

### Computational Performance
- **Total Runtime:** ~3 hours (centrality computation: 2.5 hours)
- **Memory Usage:** ~1.3 GB (graph + computations)
- **Optimizations:** Confidence filtering (93% reduction), betweenness sampling (k=100), strategic visualization sampling

---

## Deliverables

### Required Deliverables ✅
1. **CSV file of gene list:** `string_homo_sapiens.csv` (13.7M interactions)
2. **Cleaned network data:** `string_cleaned.csv` (929K interactions)
3. **Graph file:** `string_network.graphml` (19,488 nodes, 929K edges)
4. **Hub genes list:** `hub_genes.csv` (top 50 hub genes)
5. **Interactive visualization:** `network_interactive.html`

### Additional Deliverables
- 4 static network visualizations (full network, hubs, communities, summary plots)
- Complete centrality results (`centrality_results.csv`)
- Comprehensive documentation (README, PRESENTATION, PROJECT_ESSAY, PORTFOLIO)

---

## Biological Interpretation

The network exhibits **scale-free topology** with power-law degree distribution, typical of biological networks. Hub genes (0.26% of nodes, 3.01% of connections) are critical for network integrity and are typically essential genes, disease-associated, and important drug targets. The 13 detected communities likely represent functional modules, with hub genes often bridging multiple communities.

---

## Challenges & Solutions

1. **Large Dataset:** Filtered to medium+ confidence (≥400), reducing from 13.7M to 929K interactions
2. **Computational Complexity:** Used sampling (k=100) for betweenness centrality
3. **Memory Constraints:** Efficient data structures and strategic visualization sampling
4. **Visualization Clarity:** Multiple scales and interactive exploration tools

---

## Conclusion

This project successfully analyzed the human protein-protein interaction network, identifying hub genes and characterizing network structure. The pipeline processed over 13 million interactions, identified the top 50 hub genes, and created comprehensive visualizations. The results demonstrate the scale-free structure of biological networks and highlight the critical importance of hub genes in cellular function.

### Key Takeaways

1. Successfully identified hub genes using computational methods
2. Confirmed power-law distribution (scale-free structure) in biological networks
3. Hub genes are disproportionately important (0.26% nodes, 3% connections)
4. Network organized into 13 functional communities
5. Results applicable to drug discovery, disease research, and systems biology

---

**Project Status:** ✅ Complete | **All Deliverables:** ✅ Generated | **Ready for Presentation:** ✅ Yes

