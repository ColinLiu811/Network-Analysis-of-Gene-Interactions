"""
Build network graph from cleaned STRING data using NetworkX.

This script creates a graph representation of the protein-protein
interaction network and saves it in GraphML format.
"""

import pandas as pd
import networkx as nx
import os

def load_cleaned_data(input_file='string_cleaned.csv'):
    """Load cleaned STRING data."""
    print(f"Loading cleaned data from {input_file}...")
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} interactions")
    return df

def build_network_graph(df, weight_column='combined_score'):
    """
    Build NetworkX graph from interaction data.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Cleaned interaction data with protein1_clean and protein2_clean columns
    weight_column : str
        Column name to use as edge weight (if available)
    """
    print("\nBuilding network graph...")
    
    # Create undirected graph (interactions are bidirectional)
    G = nx.Graph()
    
    # Add edges
    for idx, row in df.iterrows():
        protein1 = row['protein1_clean']
        protein2 = row['protein2_clean']
        
        # Prepare edge attributes
        edge_attrs = {}
        if weight_column in df.columns:
            edge_attrs['weight'] = float(row[weight_column])
            # Normalize weight to 0-1 range for better visualization
            edge_attrs['normalized_weight'] = float(row[weight_column]) / 1000.0
        
        # Add all other columns as edge attributes
        for col in df.columns:
            if col not in ['protein1_clean', 'protein2_clean']:
                edge_attrs[col] = row[col]
        
        G.add_edge(protein1, protein2, **edge_attrs)
    
    print(f"Graph created with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    
    return G

def get_graph_statistics(G):
    """Print basic graph statistics."""
    print("\n" + "="*50)
    print("GRAPH STATISTICS")
    print("="*50)
    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Number of edges: {G.number_of_edges()}")
    print(f"Average degree: {2 * G.number_of_edges() / G.number_of_nodes():.2f}")
    
    # Check if graph is connected
    if nx.is_connected(G):
        print(f"Graph is connected")
        print(f"Diameter: {nx.diameter(G)}")
        print(f"Average path length: {nx.average_shortest_path_length(G):.2f}")
    else:
        print(f"Graph has {nx.number_connected_components(G)} connected components")
        largest_cc = max(nx.connected_components(G), key=len)
        print(f"Largest component: {len(largest_cc)} nodes")
    
    # Density
    density = nx.density(G)
    print(f"Graph density: {density:.6f}")
    
    print("="*50)

def save_graph(G, output_file='string_network.graphml', format='graphml'):
    """
    Save graph to file.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network graph
    output_file : str
        Output filename
    format : str
        Format to save ('graphml' or 'gexf')
    """
    print(f"\nSaving graph to {output_file}...")
    
    if format == 'graphml':
        nx.write_graphml(G, output_file)
    elif format == 'gexf':
        nx.write_gexf(G, output_file)
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    print(f"Graph saved successfully!")
    return output_file

def load_graph(input_file='string_network.graphml'):
    """Load graph from file."""
    print(f"Loading graph from {input_file}...")
    
    if input_file.endswith('.graphml'):
        G = nx.read_graphml(input_file)
    elif input_file.endswith('.gexf'):
        G = nx.read_gexf(input_file)
    else:
        raise ValueError(f"Unsupported file format: {input_file}")
    
    print(f"Loaded graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    return G

if __name__ == "__main__":
    import sys
    
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'string_cleaned.csv'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'string_network.graphml'
    format_type = 'graphml' if output_file.endswith('.graphml') else 'gexf'
    
    # Load cleaned data
    df = load_cleaned_data(input_file)
    
    # Build graph
    G = build_network_graph(df)
    
    # Print statistics
    get_graph_statistics(G)
    
    # Save graph
    save_graph(G, output_file, format_type)
    
    print("\nNext step: Run compute_centrality.py to calculate hub genes")

