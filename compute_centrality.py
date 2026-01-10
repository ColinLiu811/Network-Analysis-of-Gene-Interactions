"""
Compute centrality and connectivity measures to identify hub genes.

This script calculates various centrality measures for each gene/protein
in the network to identify the most important hub genes.
"""

import pandas as pd
import networkx as nx
import numpy as np
from collections import defaultdict

def load_graph(input_file='string_network.graphml'):
    """Load graph from file."""
    print(f"Loading graph from {input_file}...")
    
    if input_file.endswith('.graphml'):
        G = nx.read_graphml(input_file)
    elif input_file.endswith('.gexf'):
        G = nx.read_gexf(input_file)
    else:
        # Try to build from cleaned data
        print("Graph file not found. Building from cleaned data...")
        from build_graph import load_cleaned_data, build_network_graph
        df = load_cleaned_data('string_cleaned.csv')
        G = build_network_graph(df)
    
    print(f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    return G

def compute_centrality_measures(G):
    """
    Compute various centrality measures for all nodes.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network graph
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame with centrality measures for each node
    """
    print("\nComputing centrality measures...")
    print("This may take a while for large networks...")
    
    measures = {}
    
    # 1. Degree Centrality - simplest, most important
    print("  Computing degree centrality...")
    degree_centrality = nx.degree_centrality(G)
    measures['degree_centrality'] = degree_centrality
    
    # 2. Betweenness Centrality - nodes that act as bridges
    print("  Computing betweenness centrality...")
    try:
        betweenness = nx.betweenness_centrality(G, k=min(100, G.number_of_nodes()))
        measures['betweenness_centrality'] = betweenness
    except Exception as e:
        print(f"  Warning: Betweenness computation failed: {e}")
        measures['betweenness_centrality'] = {node: 0 for node in G.nodes()}
    
    # 3. Closeness Centrality - nodes close to all others
    print("  Computing closeness centrality...")
    try:
        # Only compute for largest connected component if graph is disconnected
        if nx.is_connected(G):
            closeness = nx.closeness_centrality(G)
        else:
            print("  Graph is disconnected, computing for largest component...")
            largest_cc = max(nx.connected_components(G), key=len)
            subgraph = G.subgraph(largest_cc)
            closeness = nx.closeness_centrality(subgraph)
            # Fill in zeros for nodes not in largest component
            full_closeness = {node: 0 for node in G.nodes()}
            full_closeness.update(closeness)
            closeness = full_closeness
        measures['closeness_centrality'] = closeness
    except Exception as e:
        print(f"  Warning: Closeness computation failed: {e}")
        measures['closeness_centrality'] = {node: 0 for node in G.nodes()}
    
    # 4. Eigenvector Centrality - importance based on connections to important nodes
    print("  Computing eigenvector centrality...")
    try:
        eigenvector = nx.eigenvector_centrality(G, max_iter=1000)
        measures['eigenvector_centrality'] = eigenvector
    except Exception as e:
        print(f"  Warning: Eigenvector computation failed: {e}")
        measures['eigenvector_centrality'] = {node: 0 for node in G.nodes()}
    
    # 5. PageRank - Google's algorithm adapted for networks
    print("  Computing PageRank...")
    try:
        pagerank = nx.pagerank(G, max_iter=100)
        measures['pagerank'] = pagerank
    except Exception as e:
        print(f"  Warning: PageRank computation failed: {e}")
        measures['pagerank'] = {node: 0 for node in G.nodes()}
    
    # 6. Clustering Coefficient - how well connected neighbors are
    print("  Computing clustering coefficient...")
    clustering = nx.clustering(G)
    measures['clustering_coefficient'] = clustering
    
    # 7. Degree (raw count)
    degrees = dict(G.degree())
    measures['degree'] = degrees
    
    # Combine all measures into DataFrame
    print("\nCombining measures into DataFrame...")
    nodes = list(G.nodes())
    df = pd.DataFrame({
        'protein_id': nodes,
        'degree': [measures['degree'].get(node, 0) for node in nodes],
        'degree_centrality': [measures['degree_centrality'].get(node, 0) for node in nodes],
        'betweenness_centrality': [measures['betweenness_centrality'].get(node, 0) for node in nodes],
        'closeness_centrality': [measures['closeness_centrality'].get(node, 0) for node in nodes],
        'eigenvector_centrality': [measures['eigenvector_centrality'].get(node, 0) for node in nodes],
        'pagerank': [measures['pagerank'].get(node, 0) for node in nodes],
        'clustering_coefficient': [measures['clustering_coefficient'].get(node, 0) for node in nodes],
    })
    
    # Compute composite hub score (normalized average of key measures)
    print("  Computing composite hub score...")
    key_measures = ['degree_centrality', 'betweenness_centrality', 'eigenvector_centrality', 'pagerank']
    for col in key_measures:
        if col in df.columns:
            # Normalize to 0-1 range
            max_val = df[col].max()
            if max_val > 0:
                df[f'{col}_normalized'] = df[col] / max_val
    
    # Composite score as average of normalized measures
    normalized_cols = [f'{col}_normalized' for col in key_measures if f'{col}_normalized' in df.columns]
    if normalized_cols:
        df['hub_score'] = df[normalized_cols].mean(axis=1)
    else:
        df['hub_score'] = df['degree_centrality']
    
    # Sort by hub score
    df = df.sort_values('hub_score', ascending=False).reset_index(drop=True)
    
    print(f"Computed centrality measures for {len(df)} nodes")
    return df

def identify_hub_genes(df, top_n=50, percentile=95):
    """
    Identify top hub genes based on centrality measures.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame with centrality measures
    top_n : int
        Number of top hubs to return
    percentile : float
        Percentile threshold for hub identification
    
    Returns:
    --------
    pandas.DataFrame
        Top hub genes
    """
    print(f"\nIdentifying top {top_n} hub genes...")
    
    # Multiple criteria for hub identification
    hub_score_threshold = df['hub_score'].quantile(percentile / 100)
    degree_threshold = df['degree'].quantile(percentile / 100)
    
    # Top hubs by composite score
    top_hubs = df.head(top_n).copy()
    
    print(f"\nHub identification thresholds:")
    print(f"  Hub score (95th percentile): {hub_score_threshold:.4f}")
    print(f"  Degree (95th percentile): {degree_threshold:.2f}")
    
    return top_hubs

def save_centrality_results(df, hub_genes, output_file='centrality_results.csv', hub_file='hub_genes.csv'):
    """Save centrality results to CSV files."""
    print(f"\nSaving results...")
    
    # Save all centrality measures
    df.to_csv(output_file, index=False)
    print(f"  Saved all centrality measures to {output_file}")
    
    # Save hub genes
    hub_genes.to_csv(hub_file, index=False)
    print(f"  Saved hub genes to {hub_file}")
    
    return output_file, hub_file

def print_hub_summary(hub_genes, top_n=20):
    """Print summary of top hub genes."""
    print("\n" + "="*80)
    print(f"TOP {min(top_n, len(hub_genes))} HUB GENES")
    print("="*80)
    
    display_cols = ['protein_id', 'degree', 'hub_score', 'degree_centrality', 
                   'betweenness_centrality', 'pagerank']
    available_cols = [col for col in display_cols if col in hub_genes.columns]
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 30)
    
    print(hub_genes[available_cols].head(top_n).to_string(index=False))
    print("="*80)

if __name__ == "__main__":
    import sys
    
    graph_file = sys.argv[1] if len(sys.argv) > 1 else 'string_network.graphml'
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    
    # Load graph
    G = load_graph(graph_file)
    
    # Compute centrality measures
    centrality_df = compute_centrality_measures(G)
    
    # Identify hub genes
    hub_genes = identify_hub_genes(centrality_df, top_n=top_n)
    
    # Print summary
    print_hub_summary(hub_genes, top_n=20)
    
    # Save results
    save_centrality_results(centrality_df, hub_genes)
    
    print("\nNext step: Run visualize_network.py to create network visualizations")

