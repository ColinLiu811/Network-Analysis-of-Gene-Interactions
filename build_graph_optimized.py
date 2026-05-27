"""
Optimized version of build_graph.py with improved performance.

This module provides optimized graph construction with sparse representations
and efficient edge addition.
"""

import pandas as pd
import networkx as nx
from performance_utils import progress_bar, get_memory_usage
from typing import Optional


def build_network_graph_optimized(df, weight_column='combined_score', use_sparse=False):
    """
    Optimized version of build_network_graph with improved performance.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Cleaned interaction data with protein1_clean and protein2_clean columns
    weight_column : str
        Column name to use as edge weight (if available)
    use_sparse : bool
        If True, use sparse graph representation (for very large networks)
    """
    print("\nBuilding network graph (optimized)...")
    initial_memory = get_memory_usage()
    
    # Use appropriate graph type
    if use_sparse:
        G = nx.Graph()
    else:
        G = nx.Graph()
    
    # Prepare edge list for batch additiom
    edges = []
    edge_attrs_list = []
    
    # Process in batches for very large datasets
    batch_size = 10000
    total_rows = len(df)
    
    for start_idx in progress_bar(range(0, total_rows, batch_size), desc="Building graph"):
        end_idx = min(start_idx + batch_size, total_rows)
        batch = df.iloc[start_idx:end_idx]
        
        for _, row in batch.iterrows():
            protein1 = row['protein1_clean']
            protein2 = row['protein2_clean']
            
            # Prepare edge attributes
            edge_attrs = {}
            if weight_column in df.columns:
                edge_attrs['weight'] = float(row[weight_column])
                edge_attrs['normalized_weight'] = float(row[weight_column]) / 1000.0
            
            # Add other columns as attributes to save memory
            for col in ['combined_score']:  # Only add essential columns
                if col in df.columns and col != weight_column:
                    edge_attrs[col] = row[col]
            
            edges.append((protein1, protein2))
            edge_attrs_list.append(edge_attrs)
    
    # Add edges in batch (more efficient than one-by-one)
    print("  Adding edges...")
    G.add_edges_from(edges)
    
    # Add edge attributes
    for (u, v), attrs in zip(edges, edge_attrs_list):
        for key, value in attrs.items():
            G[u][v][key] = value
    
    final_memory = get_memory_usage()
    print(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    print(f"Memory usage: {final_memory - initial_memory:.1f} MB")
    
    return G


# Keep original function for backward compatibility
def build_network_graph(df, weight_column='combined_score'):
    """Wrapper for optimized version."""
    return build_network_graph_optimized(df, weight_column, use_sparse=False)
