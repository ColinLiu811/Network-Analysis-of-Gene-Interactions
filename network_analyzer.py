"""
Network analysis module using NetworkX.
"""

import pandas as pd
import networkx as nx
import numpy as np


class NetworkAnalyzer:
    """Handles network construction and metric computation."""
    
    def __init__(self, df_interactions):
        """
        Initialize the network analyzer.
        
        Args:
            df_interactions: DataFrame with columns GeneA, GeneB, and optionally Score
        """
        self.df_interactions = df_interactions
        self.graph = None
        self.metrics_df = None
    
    def build_graph(self):
        """
        Build an undirected NetworkX graph from interaction data.
        
        Returns:
            networkx.Graph object
        """
        self.graph = nx.Graph()
        
        # Add edges (and nodes automatically)
        for _, row in self.df_interactions.iterrows():
            gene_a = str(row['GeneA'])
            gene_b = str(row['GeneB'])
            
            # Add edge with optional weight
            edge_attrs = {}
            if 'Score' in row and pd.notna(row['Score']):
                edge_attrs['weight'] = float(row['Score'])
            
            self.graph.add_edge(gene_a, gene_b, **edge_attrs)
        
        return self.graph
    
    def compute_metrics(self):
        """
        Compute network centrality metrics for all nodes.
        
        Returns:
            DataFrame with columns: Gene, degree_centrality, betweenness_centrality,
            closeness_centrality, clustering_coefficient
        """
        if self.graph is None:
            self.build_graph()
        
        if self.graph.number_of_nodes() == 0:
            return pd.DataFrame(columns=[
                'Gene', 'degree_centrality', 'betweenness_centrality',
                'closeness_centrality', 'clustering_coefficient'
            ])
        
        metrics = []
        
        # Compute metrics
        degree_cent = nx.degree_centrality(self.graph)
        betweenness_cent = nx.betweenness_centrality(self.graph)
        closeness_cent = nx.closeness_centrality(self.graph)
        clustering = nx.clustering(self.graph)
        
        # Store in DataFrame
        for node in self.graph.nodes():
            metrics.append({
                'Gene': node,
                'degree_centrality': degree_cent[node],
                'betweenness_centrality': betweenness_cent[node],
                'closeness_centrality': closeness_cent[node],
                'clustering_coefficient': clustering[node]
            })
        
        self.metrics_df = pd.DataFrame(metrics)
        self.metrics_df = self.metrics_df.sort_values(
            'degree_centrality',
            ascending=False
        ).reset_index(drop=True)
        
        return self.metrics_df
    
    def get_hub_genes(self, top_n=10):
        """
        Get top hub genes sorted by degree centrality.
        
        Args:
            top_n: Number of top hub genes to return
            
        Returns:
            DataFrame with top hub genes and their metrics
        """
        if self.metrics_df is None:
            self.compute_metrics()
        
        return self.metrics_df.head(top_n).set_index('Gene')

