"""
Network visualization module.
"""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pathlib import Path

try:
    from pyvis.network import Network
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False


class NetworkVisualizer:
    """Handles network visualization using matplotlib and pyvis."""
    
    def __init__(self, graph, metrics_df):
        """
        Initialize the visualizer.
        
        Args:
            graph: NetworkX graph object
            metrics_df: DataFrame with node metrics
        """
        self.graph = graph
        self.metrics_df = metrics_df.set_index('Gene') if 'Gene' in metrics_df.columns else metrics_df
    
    def visualize_png(self, output_file, hub_genes=None, figsize=(16, 12)):
        """
        Create a static PNG visualization using matplotlib.
        
        Args:
            output_file: Path to save PNG file
            hub_genes: DataFrame of hub genes to highlight
            figsize: Figure size tuple
        """
        if self.graph.number_of_nodes() == 0:
            print("  Warning: Empty graph, skipping visualization")
            return
        
        # Use a layout algorithm
        if self.graph.number_of_nodes() > 1000:
            pos = nx.spring_layout(self.graph, k=0.5, iterations=50, seed=42)
        else:
            pos = nx.spring_layout(self.graph, k=1, iterations=100, seed=42)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # Get node sizes based on degree centrality
        if hub_genes is not None and len(hub_genes) > 0:
            node_sizes = []
            node_colors = []
            hub_gene_set = set(hub_genes.index)
            
            for node in self.graph.nodes():
                if node in self.metrics_df.index:
                    degree = self.metrics_df.loc[node, 'degree_centrality']
                    node_sizes.append(300 + degree * 2000)
                    # Color hub genes differently
                    if node in hub_gene_set:
                        node_colors.append('#ff6b6b')  # Red for hubs
                    else:
                        node_colors.append('#4ecdc4')  # Teal for others
                else:
                    node_sizes.append(100)
                    node_colors.append('#95a5a6')  # Gray for nodes without metrics
        else:
            node_sizes = [300] * self.graph.number_of_nodes()
            node_colors = ['#4ecdc4'] * self.graph.number_of_nodes()
        
        # Draw edges
        nx.draw_networkx_edges(
            self.graph, pos,
            alpha=0.2,
            width=0.5,
            ax=ax
        )
        
        # Draw nodes
        nx.draw_networkx_nodes(
            self.graph, pos,
            node_size=node_sizes,
            node_color=node_colors,
            alpha=0.8,
            ax=ax
        )
        
        # Label only hub genes to avoid clutter
        if hub_genes is not None and len(hub_genes) > 0:
            hub_labels = {gene: gene for gene in hub_genes.index if gene in self.graph.nodes()}
            nx.draw_networkx_labels(
                self.graph, pos,
                labels=hub_labels,
                font_size=8,
                font_weight='bold',
                ax=ax
            )
        
        ax.set_title(
            f'Gene Interaction Network\n'
            f'Nodes: {self.graph.number_of_nodes()}, '
            f'Edges: {self.graph.number_of_edges()}',
            fontsize=16,
            fontweight='bold'
        )
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
    
    def visualize_html(self, output_file, hub_genes=None):
        """
        Create an interactive HTML visualization using pyvis.
        
        Args:
            output_file: Path to save HTML file
            hub_genes: DataFrame of hub genes to highlight
        """
        if not PYVIS_AVAILABLE:
            print("  Warning: pyvis not available. Install with: pip install pyvis")
            return
        
        if self.graph.number_of_nodes() == 0:
            print("  Warning: Empty graph, skipping visualization")
            return
        
        # Create pyvis network
        net = Network(
            height='800px',
            width='100%',
            bgcolor='#222222',
            font_color='white',
            directed=False
        )
        
        # Add nodes with attributes
        hub_gene_set = set(hub_genes.index) if hub_genes is not None else set()
        
        for node in self.graph.nodes():
            node_attrs = {
                'label': node,
                'title': node
            }
            
            if node in self.metrics_df.index:
                degree = self.metrics_df.loc[node, 'degree_centrality']
                betweenness = self.metrics_df.loc[node, 'betweenness_centrality']
                clustering = self.metrics_df.loc[node, 'clustering_coefficient']
                
                # Size based on degree
                node_attrs['size'] = 10 + degree * 30
                
                # Color based on hub status
                if node in hub_gene_set:
                    node_attrs['color'] = '#ff6b6b'
                    node_attrs['title'] = (
                        f"{node}\n"
                        f"Degree Centrality: {degree:.4f}\n"
                        f"Betweenness: {betweenness:.4f}\n"
                        f"Clustering: {clustering:.4f}\n"
                        f"[HUB GENE]"
                    )
                else:
                    node_attrs['color'] = '#4ecdc4'
                    node_attrs['title'] = (
                        f"{node}\n"
                        f"Degree Centrality: {degree:.4f}\n"
                        f"Betweenness: {betweenness:.4f}\n"
                        f"Clustering: {clustering:.4f}"
                    )
            else:
                node_attrs['size'] = 10
                node_attrs['color'] = '#95a5a6'
            
            net.add_node(node, **node_attrs)
        
        # Add edges
        for edge in self.graph.edges(data=True):
            edge_attrs = {}
            if 'weight' in edge[2]:
                edge_attrs['width'] = edge[2]['weight'] * 2
            net.add_edge(edge[0], edge[1], **edge_attrs)
        
        # Configure physics
        net.set_options("""
        {
          "physics": {
            "barnesHut": {
              "gravitationalConstant": -2000,
              "centralGravity": 0.1,
              "springLength": 200,
              "springConstant": 0.04,
              "damping": 0.09
            }
          }
        }
        """)
        
        net.save_graph(str(output_file))

