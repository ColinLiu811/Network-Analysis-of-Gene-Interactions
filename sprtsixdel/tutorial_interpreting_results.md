# Tutorial: Interpreting Results

This guide helps connect output metrics to biological interpretation.

## 1. Start With `hub_genes.csv`

Prioritize these columns:
- `protein_id`
- `degree`
- `hub_score`
- `betweenness_centrality`
- `pagerank`

Interpretation hints:
- high `degree`: broadly connected proteins
- high `betweenness`: potential bridge or bottleneck proteins
- high `hub_score`: consistently important across multiple metrics

## 2. Use Visual Outputs Together

- `network_full.png`: global structure and major hubs
- `network_hubs.png`: local neighborhood around key proteins
- `network_communities.png`: modular structure and subnetwork groups
- `network_interactive.html`: search/filter proteins and inspect tooltips

## 3. Compare Signal Across Metrics

Do not rely on one metric alone; consistency across degree, PageRank, and
betweenness often provides stronger confidence for candidate prioritization.

## 4. Document Candidate Selection

For each selected candidate, record:
- metric evidence (rank/score)
- network position (bridge, community core, peripheral)
- biological rationale from external literature

## Success Check

Given completed outputs, when candidate review is performed, then each selected
hub should have both quantitative metric support and contextual explanation.
