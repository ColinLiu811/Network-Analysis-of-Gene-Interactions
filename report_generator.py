"""
Report generation module.
"""

import networkx as nx
from pathlib import Path
from datetime import datetime


class ReportGenerator:
    """Generates text/markdown reports summarizing network analysis."""
    
    def __init__(self, analyzer, hub_genes, output_dir):
        """
        Initialize the report generator.
        
        Args:
            analyzer: NetworkAnalyzer instance
            hub_genes: DataFrame of hub genes
            output_dir: Output directory path
        """
        self.analyzer = analyzer
        self.hub_genes = hub_genes
        self.output_dir = Path(output_dir)
    
    def generate_report(self):
        """
        Generate a markdown report file.
        
        Returns:
            Path to generated report file
        """
        graph = self.analyzer.graph
        metrics_df = self.analyzer.metrics_df
        
        report_lines = [
            "# Gene Interaction Network Analysis Report",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Network Overview",
            "",
            f"- **Total Nodes (Genes):** {graph.number_of_nodes()}",
            f"- **Total Edges (Interactions):** {graph.number_of_edges()}",
            f"- **Network Density:** {nx.density(graph):.6f}",
            "",
            "## Network Metrics Summary",
            "",
            f"- **Average Degree Centrality:** {metrics_df['degree_centrality'].mean():.4f}",
            f"- **Average Betweenness Centrality:** {metrics_df['betweenness_centrality'].mean():.4f}",
            f"- **Average Closeness Centrality:** {metrics_df['closeness_centrality'].mean():.4f}",
            f"- **Average Clustering Coefficient:** {metrics_df['clustering_coefficient'].mean():.4f}",
            "",
            "## Top Hub Genes",
            "",
            "Hub genes are identified based on degree centrality (number of connections).",
            "These genes are likely to be key regulators in the network.",
            "",
            "| Rank | Gene | Degree Centrality | Betweenness Centrality | Closeness Centrality | Clustering Coefficient |",
            "|------|------|-------------------|------------------------|----------------------|------------------------|",
        ]
        
        # Add hub gene rows
        for i, (gene, row) in enumerate(self.hub_genes.iterrows(), 1):
            report_lines.append(
                f"| {i} | {gene} | {row['degree_centrality']:.4f} | "
                f"{row['betweenness_centrality']:.4f} | {row['closeness_centrality']:.4f} | "
                f"{row['clustering_coefficient']:.4f} |"
            )
        
        report_lines.extend([
            "",
            "## Interpretation",
            "",
            "### Degree Centrality",
            "Measures the number of direct connections a gene has. Higher values indicate genes that interact with many other genes.",
            "",
            "### Betweenness Centrality",
            "Measures how often a gene lies on the shortest path between other genes. High values indicate genes that act as bridges in the network.",
            "",
            "### Closeness Centrality",
            "Measures how close a gene is to all other genes in the network. High values indicate genes that can quickly reach other genes.",
            "",
            "### Clustering Coefficient",
            "Measures how connected a gene's neighbors are to each other. High values indicate local clustering around the gene.",
            "",
            "## Files Generated",
            "",
            "- `cleaned_interactions.csv`: Preprocessed interaction data",
            "- `network_metrics.csv`: Complete metrics for all genes",
            "- `network_visualization.png`: Static network visualization (if generated)",
            "- `network_visualization.html`: Interactive network visualization (if generated)",
            "- `analysis_report.md`: This report",
            "",
        ])
        
        # Write report
        report_file = self.output_dir / 'analysis_report.md'
        with open(report_file, 'w') as f:
            f.write('\n'.join(report_lines))
        
        return report_file

