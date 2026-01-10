"""
Create visualizations of the protein-protein interaction network.

This script generates various visualizations including:
- Full network overview
- Hub gene visualization
- Network clusters and communities
- Interactive visualizations
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')

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

def load_hub_genes(hub_file='hub_genes.csv', top_n=50):
    """Load hub genes data."""
    print(f"Loading hub genes from {hub_file}...")
    df = pd.read_csv(hub_file)
    top_hubs = set(df.head(top_n)['protein_id'].tolist())
    print(f"Loaded {len(top_hubs)} hub genes")
    return top_hubs, df

def detect_communities(G):
    """
    Detect communities/clusters in the network using Louvain algorithm.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network graph
    
    Returns:
    --------
    dict
        Dictionary mapping node to community ID
    """
    print("\nDetecting communities using Louvain algorithm...")
    
    try:
        import community.community_louvain as community_louvain
        communities = community_louvain.best_partition(G)
        num_communities = len(set(communities.values()))
        print(f"Detected {num_communities} communities")
        return communities
    except ImportError:
        print("python-louvain not installed. Using greedy modularity communities instead...")
        from networkx.algorithms import community
        communities_generator = community.greedy_modularity_communities(G)
        communities = {}
        for i, comm in enumerate(communities_generator):
            for node in comm:
                communities[node] = i
        num_communities = len(set(communities.values()))
        print(f"Detected {num_communities} communities")
        return communities

def visualize_full_network(G, hub_genes=None, communities=None, output_file='network_full.png', 
                           max_nodes=5000, layout='spring'):
    """
    Visualize the full network with hub genes highlighted.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network graph
    hub_genes : set
        Set of hub gene IDs
    communities : dict
        Community assignment for each node
    output_file : str
        Output filename
    max_nodes : int
        Maximum number of nodes to visualize (for performance)
    layout : str
        Layout algorithm ('spring', 'circular', 'kamada_kawai')
    """
    print(f"\nCreating full network visualization...")
    
    # If graph is too large, sample or use largest component
    if G.number_of_nodes() > max_nodes:
        print(f"Graph has {G.number_of_nodes()} nodes. Using largest connected component...")
        largest_cc = max(nx.connected_components(G), key=len)
        G_viz = G.subgraph(largest_cc).copy()
        
        # Further sample if still too large
        if G_viz.number_of_nodes() > max_nodes:
            nodes_sample = list(G_viz.nodes())[:max_nodes]
            G_viz = G_viz.subgraph(nodes_sample).copy()
    else:
        G_viz = G.copy()
    
    print(f"Visualizing {G_viz.number_of_nodes()} nodes and {G_viz.number_of_edges()} edges")
    
    # Choose layout
    if layout == 'spring':
        pos = nx.spring_layout(G_viz, k=1, iterations=50)
    elif layout == 'circular':
        pos = nx.circular_layout(G_viz)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G_viz)
    else:
        pos = nx.spring_layout(G_viz)
    
    # Create figure
    plt.figure(figsize=(20, 20))
    
    # Draw edges
    nx.draw_networkx_edges(G_viz, pos, alpha=0.1, width=0.5, edge_color='gray')
    
    # Draw nodes - color by hub status or community
    if hub_genes:
        node_colors = ['red' if node in hub_genes else 'lightblue' for node in G_viz.nodes()]
        node_sizes = [300 if node in hub_genes else 50 for node in G_viz.nodes()]
    elif communities:
        # Color by community
        cmap = plt.cm.get_cmap('tab20')
        node_colors = [cmap(communities.get(node, 0) % 20) for node in G_viz.nodes()]
        node_sizes = [50 for _ in G_viz.nodes()]
    else:
        node_colors = 'lightblue'
        node_sizes = 50
    
    nx.draw_networkx_nodes(G_viz, pos, node_color=node_colors, 
                          node_size=node_sizes, alpha=0.7)
    
    # Add legend
    if hub_genes:
        red_patch = mpatches.Patch(color='red', label='Hub Genes')
        blue_patch = mpatches.Patch(color='lightblue', label='Other Genes')
        plt.legend(handles=[red_patch, blue_patch], loc='upper right')
    
    plt.title(f'Protein-Protein Interaction Network\n{G_viz.number_of_nodes()} nodes, {G_viz.number_of_edges()} edges', 
              fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved visualization to {output_file}")
    plt.close()

def visualize_hub_network(G, hub_genes, output_file='network_hubs.png'):
    """Visualize hub genes and their immediate neighbors."""
    print(f"\nCreating hub gene network visualization...")
    
    # Get hub genes and their neighbors
    hub_subgraph_nodes = set(hub_genes)
    for hub in hub_genes:
        if hub in G:
            hub_subgraph_nodes.update(G.neighbors(hub))
    
    G_hubs = G.subgraph(hub_subgraph_nodes).copy()
    print(f"Hub subgraph: {G_hubs.number_of_nodes()} nodes, {G_hubs.number_of_edges()} edges")
    
    pos = nx.spring_layout(G_hubs, k=1, iterations=50)
    
    plt.figure(figsize=(16, 16))
    
    # Draw edges
    nx.draw_networkx_edges(G_hubs, pos, alpha=0.2, width=0.5, edge_color='gray')
    
    # Draw nodes
    node_colors = ['red' if node in hub_genes else 'lightblue' for node in G_hubs.nodes()]
    node_sizes = [500 if node in hub_genes else 100 for node in G_hubs.nodes()]
    
    nx.draw_networkx_nodes(G_hubs, pos, node_color=node_colors, 
                          node_size=node_sizes, alpha=0.8)
    
    # Label hub genes
    hub_labels = {node: node[:15] + '...' if len(node) > 15 else node 
                  for node in hub_genes if node in G_hubs}
    nx.draw_networkx_labels(G_hubs, pos, hub_labels, font_size=8, font_weight='bold')
    
    red_patch = mpatches.Patch(color='red', label='Hub Genes')
    blue_patch = mpatches.Patch(color='lightblue', label='Neighbors')
    plt.legend(handles=[red_patch, blue_patch], loc='upper right')
    
    plt.title('Hub Gene Network', fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved visualization to {output_file}")
    plt.close()

def visualize_communities(G, communities, output_file='network_communities.png', max_nodes=5000):
    """Visualize network with community structure."""
    print(f"\nCreating community visualization...")
    
    if G.number_of_nodes() > max_nodes:
        largest_cc = max(nx.connected_components(G), key=len)
        G_viz = G.subgraph(largest_cc).copy()
        if G_viz.number_of_nodes() > max_nodes:
            nodes_sample = list(G_viz.nodes())[:max_nodes]
            G_viz = G_viz.subgraph(nodes_sample).copy()
    else:
        G_viz = G.copy()
    
    pos = nx.spring_layout(G_viz, k=1, iterations=50)
    
    # Get unique communities
    unique_communities = list(set(communities.values()))
    num_communities = len(unique_communities)
    
    plt.figure(figsize=(20, 20))
    
    # Draw edges
    nx.draw_networkx_edges(G_viz, pos, alpha=0.1, width=0.3, edge_color='gray')
    
    # Color nodes by community
    cmap = plt.cm.get_cmap('tab20')
    node_colors = [cmap(communities.get(node, 0) % 20) for node in G_viz.nodes()]
    
    nx.draw_networkx_nodes(G_viz, pos, node_color=node_colors, 
                          node_size=30, alpha=0.7)
    
    plt.title(f'Network Communities\n{num_communities} communities detected', 
              fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved visualization to {output_file}")
    plt.close()

def create_summary_plots(hub_genes_df, output_file='summary_plots.png'):
    """Create summary statistics plots."""
    print(f"\nCreating summary plots...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Degree distribution
    ax1 = axes[0, 0]
    degrees = hub_genes_df['degree'].values
    ax1.hist(degrees, bins=50, edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Degree', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title('Degree Distribution', fontsize=14, fontweight='bold')
    ax1.set_yscale('log')
    
    # Hub score distribution
    ax2 = axes[0, 1]
    hub_scores = hub_genes_df['hub_score'].values
    ax2.hist(hub_scores, bins=50, edgecolor='black', alpha=0.7, color='green')
    ax2.set_xlabel('Hub Score', fontsize=12)
    ax2.set_ylabel('Frequency', fontsize=12)
    ax2.set_title('Hub Score Distribution', fontsize=14, fontweight='bold')
    
    # Top hubs bar chart
    ax3 = axes[1, 0]
    top_20 = hub_genes_df.head(20)
    ax3.barh(range(len(top_20)), top_20['hub_score'].values)
    ax3.set_yticks(range(len(top_20)))
    ax3.set_yticklabels([pid[:20] + '...' if len(pid) > 20 else pid for pid in top_20['protein_id']], 
                        fontsize=8)
    ax3.set_xlabel('Hub Score', fontsize=12)
    ax3.set_title('Top 20 Hub Genes', fontsize=14, fontweight='bold')
    ax3.invert_yaxis()
    
    # Centrality correlation
    ax4 = axes[1, 1]
    centrality_cols = ['degree_centrality', 'betweenness_centrality', 
                       'eigenvector_centrality', 'pagerank']
    available_cols = [col for col in centrality_cols if col in hub_genes_df.columns]
    if len(available_cols) > 1:
        corr_matrix = hub_genes_df[available_cols].corr()
        im = ax4.imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
        ax4.set_xticks(range(len(available_cols)))
        ax4.set_yticks(range(len(available_cols)))
        ax4.set_xticklabels(available_cols, rotation=45, ha='right', fontsize=8)
        ax4.set_yticklabels(available_cols, fontsize=8)
        ax4.set_title('Centrality Measures Correlation', fontsize=14, fontweight='bold')
        plt.colorbar(im, ax=ax4)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved summary plots to {output_file}")
    plt.close()

def create_interactive_visualization(G, hub_genes=None, output_file='network_interactive.html'):
    """Create interactive HTML visualization using Pyvis."""
    print(f"\nCreating interactive visualization...")
    
    try:
        from pyvis.network import Network
        
        # Sample if too large
        if G.number_of_nodes() > 1000:
            print(f"Graph too large ({G.number_of_nodes()} nodes). Sampling 1000 nodes...")
            nodes_sample = list(G.nodes())[:1000]
            G_viz = G.subgraph(nodes_sample).copy()
        else:
            G_viz = G.copy()
        
        net = Network(height='800px', width='100%', bgcolor='#222222', font_color='white')
        net.from_nx(G_viz)
        
        # Highlight hub genes if provided
        if hub_genes:
            for node in net.nodes:
                if node['id'] in hub_genes:
                    node['color'] = '#ff0000'
                    node['size'] = 30
                    node['title'] = f"Hub Gene: {node['id']}"
                else:
                    node['size'] = 10
        
        net.show(output_file)
        print(f"Saved interactive visualization to {output_file}")
    except ImportError:
        print("Pyvis not installed. Skipping interactive visualization.")
        print("Install with: pip install pyvis")

if __name__ == "__main__":
    import sys
    
    graph_file = sys.argv[1] if len(sys.argv) > 1 else 'string_network.graphml'
    hub_file = sys.argv[2] if len(sys.argv) > 2 else 'hub_genes.csv'
    
    # Load graph
    G = load_graph(graph_file)
    
    # Load hub genes
    hub_genes, hub_genes_df = load_hub_genes(hub_file)
    
    # Detect communities
    communities = detect_communities(G)
    
    # Create visualizations
    visualize_full_network(G, hub_genes=hub_genes, output_file='network_full.png')
    visualize_hub_network(G, hub_genes, output_file='network_hubs.png')
    visualize_communities(G, communities, output_file='network_communities.png')
    create_summary_plots(hub_genes_df, output_file='summary_plots.png')
    create_interactive_visualization(G, hub_genes=hub_genes, output_file='network_interactive.html')
    
    print("\nAll visualizations created successfully!")

