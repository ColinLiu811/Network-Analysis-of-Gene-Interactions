"""
Advanced network analysis features.

This module provides:
- Additional centrality measures (Katz, Harmonic)
- Network motif detection
- Path analysis
- Network comparison tools
- Statistical analysis
"""

import pandas as pd
import networkx as nx
import numpy as np
from collections import defaultdict, Counter
from itertools import combinations, permutations
import time
from performance_utils import progress_bar
from typing import Dict, List, Tuple, Optional, Set

# Optional scipy imports for statistical analysis
try:
    from scipy import stats
    from scipy.optimize import curve_fit
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("Warning: scipy not available. Some statistical features may be limited.")


def compute_katz_centrality(G, alpha=0.1, beta=1.0, max_iter=1000, tol=1e-6):
    """
    Compute Katz centrality.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network graph
    alpha : float
        Attenuation factor (must be < 1/largest_eigenvalue)
    beta : float
        Weight given to immediate neighbors
    max_iter : int
        Maximum iterations
    tol : float
        Tolerance for convergence
    
    Returns:
    --------
    dict
        Katz centrality for each node
    """
    try:
        # Use NetworkX implementation if available, otherwise compute manually
        katz = nx.katz_centrality(G, alpha=alpha, beta=beta, max_iter=max_iter, tol=tol)
        return katz
    except:
        # Fallback: simple iterative computation
        nodes = list(G.nodes())
        n = len(nodes)
        katz = {node: 1.0 for node in nodes}
        
        for _ in range(max_iter):
            katz_new = {node: beta for node in nodes}
            for node in nodes:
                for neighbor in G.neighbors(node):
                    katz_new[node] += alpha * katz[neighbor]
            
            # Check convergence
            diff = sum(abs(katz_new[node] - katz[node]) for node in nodes)
            if diff < tol * n:
                break
            katz = katz_new
        
        return katz


def compute_harmonic_centrality(G):
    """
    Compute Harmonic centrality.
    
    Harmonic centrality is the sum of reciprocals of shortest path distances.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network graph
    
    Returns:
    --------
    dict
        Harmonic centrality for each node
    """
    harmonic = {}
    nodes = list(G.nodes())
    
    for node in progress_bar(nodes, desc="Computing harmonic centrality"):
        total = 0.0
        for other in nodes:
            if node != other:
                try:
                    path_length = nx.shortest_path_length(G, node, other)
                    if path_length > 0:
                        total += 1.0 / path_length
                except nx.NetworkXNoPath:
                    pass  # No path exists, contribution is 0
        harmonic[node] = total
    
    return harmonic


def detect_3node_motifs(G, sample_size=None):
    """
    Detect 3-node motifs in the network.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network graph
    sample_size : int, optional
        If provided, sample this many 3-node subgraphs (for large networks)
    
    Returns:
    --------
    dict
        Count of each motif type
    """
    print("Detecting 3-node motifs...")
    nodes = list(G.nodes())
    n_nodes = len(nodes)
    
    # For large networks, sample
    if sample_size and n_nodes > sample_size:
        import random
        nodes = random.sample(nodes, min(sample_size, n_nodes))
        print(f"  Sampling {len(nodes)} nodes for motif detection")
    
    motif_counts = defaultdict(int)
    total_subgraphs = 0
    
    # All possible 3-node combinations
    for triplet in progress_bar(combinations(nodes, 3), desc="Analyzing motifs"):
        subgraph = G.subgraph(triplet)
        edges = subgraph.number_of_edges()
        
        # Classify motif type by number of edges
        if edges == 0:
            motif_type = "no_edges"
        elif edges == 1:
            motif_type = "single_edge"
        elif edges == 2:
            motif_type = "two_edges"
        elif edges == 3:
            motif_type = "triangle"
        else:
            motif_type = "unknown"
        
        motif_counts[motif_type] += 1
        total_subgraphs += 1
    
    # Normalize to frequencies
    motif_frequencies = {k: v / total_subgraphs for k, v in motif_counts.items()}
    
    return {
        'counts': dict(motif_counts),
        'frequencies': motif_frequencies,
        'total_subgraphs': total_subgraphs
    }


def compute_motif_significance(G, motif_results, n_random=100):
    """
    Compute Z-scores for motif significance by comparing to random networks.
    
    Parameters:
    -----------
    G : networkx.Graph
        Original network graph
    motif_results : dict
        Results from detect_3node_motifs
    n_random : int
        Number of random networks to generate
    
    Returns:
    --------
    dict
        Z-scores for each motif type
    """
    print(f"Computing motif significance (comparing to {n_random} random networks)...")
    
    # Generate random networks with same degree distribution
    n_nodes = G.number_of_nodes()
    degree_sequence = [d for n, d in G.degree()]
    
    random_counts = defaultdict(list)
    
    for i in progress_bar(range(n_random), desc="Generating random networks"):
        try:
            # Create random graph with same degree sequence
            G_random = nx.configuration_model(degree_sequence)
            G_random = nx.Graph(G_random)  # Remove parallel edges
            G_random.remove_edges_from(nx.selfloop_edges(G_random))
            
            # Detect motifs in random network (use same sample size if provided)
            sample_size = 1000 if n_nodes > 1000 else None
            random_motifs = detect_3node_motifs(G_random, sample_size=sample_size)
            
            for motif_type, count in random_motifs['counts'].items():
                random_counts[motif_type].append(count)
        except Exception as e:
            # Skip if random network generation fails
            continue
    
    # Compute Z-scores
    z_scores = {}
    for motif_type, observed_count in motif_results['counts'].items():
        if motif_type in random_counts and len(random_counts[motif_type]) > 0:
            random_counts_list = random_counts[motif_type]
            mean_random = np.mean(random_counts_list)
            std_random = np.std(random_counts_list)
            
            if std_random > 0:
                z_score = (observed_count - mean_random) / std_random
            else:
                z_score = 0.0
            
            z_scores[motif_type] = {
                'observed': observed_count,
                'mean_random': mean_random,
                'std_random': std_random,
                'z_score': z_score
            }
    
    return z_scores


def analyze_paths(G, max_nodes=1000):
    """
    Analyze shortest paths in the network.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network graph
    max_nodes : int
        Maximum nodes to analyze (for large networks)
    
    Returns:
    --------
    dict
        Path analysis results
    """
    print("Analyzing network paths...")
    
    if not nx.is_connected(G):
        print("  Graph is disconnected, analyzing largest component...")
        largest_cc = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_cc)
    
    nodes = list(G.nodes())
    if len(nodes) > max_nodes:
        import random
        nodes = random.sample(nodes, max_nodes)
        print(f"  Sampling {len(nodes)} nodes for path analysis")
    
    # Compute all-pairs shortest paths (sample if large)
    path_lengths = []
    critical_paths = []
    
    node_pairs = list(combinations(nodes, 2))[:min(10000, len(nodes) * (len(nodes) - 1) // 2)]
    
    for source, target in progress_bar(node_pairs, desc="Computing paths"):
        try:
            path = nx.shortest_path(G, source, target)
            path_length = len(path) - 1
            path_lengths.append(path_length)
            
            # Track critical paths (longest shortest paths)
            if path_length > 5:  # Arbitrary threshold
                critical_paths.append({
                    'source': source,
                    'target': target,
                    'length': path_length,
                    'path': path
                })
        except nx.NetworkXNoPath:
            pass
    
    # Compute statistics
    if path_lengths:
        path_lengths_array = np.array(path_lengths)
        results = {
            'average_path_length': np.mean(path_lengths_array),
            'median_path_length': np.median(path_lengths_array),
            'max_path_length': np.max(path_lengths_array),
            'min_path_length': np.min(path_lengths_array),
            'std_path_length': np.std(path_lengths_array),
            'path_length_distribution': dict(Counter(path_lengths)),
            'critical_paths': critical_paths[:10]  # Top 10 longest paths
        }
        
        # Diameter (longest shortest path)
        try:
            results['diameter'] = nx.diameter(G)
        except:
            results['diameter'] = np.max(path_lengths_array) if path_lengths else 0
    else:
        results = {
            'average_path_length': 0,
            'median_path_length': 0,
            'max_path_length': 0,
            'min_path_length': 0,
            'std_path_length': 0,
            'path_length_distribution': {},
            'critical_paths': [],
            'diameter': 0
        }
    
    return results


def compare_networks(G1, G2, name1="Network 1", name2="Network 2"):
    """
    Compare two networks and compute similarity metrics.
    
    Parameters:
    -----------
    G1, G2 : networkx.Graph
        Networks to compare
    name1, name2 : str
        Names for the networks
    
    Returns:
    --------
    dict
        Comparison metrics
    """
    print(f"Comparing {name1} and {name2}...")
    
    nodes1 = set(G1.nodes())
    nodes2 = set(G2.nodes())
    edges1 = set(G1.edges())
    edges2 = set(G2.edges())
    
    # Node overlap
    common_nodes = nodes1 & nodes2
    unique_to_1 = nodes1 - nodes2
    unique_to_2 = nodes2 - nodes1
    
    # Edge overlap
    common_edges = edges1 & edges2
    unique_edges_1 = edges1 - edges2
    unique_edges_2 = edges2 - edges1
    
    # Jaccard similarity
    node_jaccard = len(common_nodes) / len(nodes1 | nodes2) if (nodes1 | nodes2) else 0
    edge_jaccard = len(common_edges) / len(edges1 | edges2) if (edges1 | edges2) else 0
    
    # Basic statistics
    results = {
        'network1': {
            'name': name1,
            'nodes': len(nodes1),
            'edges': len(edges1),
            'density': nx.density(G1)
        },
        'network2': {
            'name': name2,
            'nodes': len(nodes2),
            'edges': len(edges2),
            'density': nx.density(G2)
        },
        'node_overlap': {
            'common': len(common_nodes),
            'unique_to_1': len(unique_to_1),
            'unique_to_2': len(unique_to_2),
            'jaccard_similarity': node_jaccard
        },
        'edge_overlap': {
            'common': len(common_edges),
            'unique_to_1': len(unique_edges_1),
            'unique_to_2': len(unique_edges_2),
            'jaccard_similarity': edge_jaccard
        }
    }
    
    return results


def analyze_network_statistics(G):
    """
    Perform advanced statistical analysis of network topology.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network graph
    
    Returns:
    --------
    dict
        Statistical analysis results
    """
    print("Performing statistical analysis...")
    
    results = {}
    
    # Degree distribution
    degrees = [d for n, d in G.degree()]
    results['degree_distribution'] = {
        'mean': np.mean(degrees),
        'median': np.median(degrees),
        'std': np.std(degrees),
        'min': np.min(degrees),
        'max': np.max(degrees),
        'histogram': dict(Counter(degrees))
    }
    
    # Power-law fitting
    try:
        # Fit power-law: P(k) ~ k^(-gamma)
        degree_counts = Counter(degrees)
        k_values = np.array([k for k in degree_counts.keys() if k > 0])
        p_values = np.array([degree_counts[k] / len(degrees) for k in k_values])
        
        # Log-log fit
        log_k = np.log(k_values[k_values > 0])
        log_p = np.log(p_values[k_values > 0])
        
        if len(log_k) > 1:
            slope, intercept = np.polyfit(log_k, log_p, 1)
            gamma = -slope
            results['power_law'] = {
                'gamma': gamma,
                'fitted': True
            }
        else:
            results['power_law'] = {'fitted': False}
    except:
        results['power_law'] = {'fitted': False}
    
    # Clustering statistics
    clustering = nx.clustering(G)
    clustering_values = list(clustering.values())
    results['clustering'] = {
        'average': np.mean(clustering_values),
        'global': nx.average_clustering(G),
        'transitivity': nx.transitivity(G)
    }
    
    # Small-world properties
    try:
        if nx.is_connected(G):
            avg_path_length = nx.average_shortest_path_length(G)
            results['small_world'] = {
                'average_path_length': avg_path_length,
                'average_clustering': results['clustering']['average'],
                'is_small_world': results['clustering']['average'] > 0.1 and avg_path_length < np.log(len(G.nodes()))
            }
        else:
            results['small_world'] = {'is_small_world': False, 'note': 'Graph is disconnected'}
    except:
        results['small_world'] = {'is_small_world': False, 'note': 'Could not compute'}
    
    # Centrality correlations (if centrality measures available)
    # This would require centrality data to be passed in
    
    return results


def compute_centrality_correlations(centrality_df):
    """
    Compute correlations between different centrality measures.
    
    Parameters:
    -----------
    centrality_df : pandas.DataFrame
        DataFrame with centrality measures
    
    Returns:
    --------
    pandas.DataFrame
        Correlation matrix
    """
    centrality_cols = [col for col in centrality_df.columns 
                      if col not in ['protein_id', 'hub_score'] and 
                      'normalized' not in col]
    
    if len(centrality_cols) < 2:
        return pd.DataFrame()
    
    correlation_matrix = centrality_df[centrality_cols].corr()
    return correlation_matrix


def run_advanced_analysis(G, centrality_df=None, output_dir='.'):
    """
    Run complete advanced analysis suite.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network graph
    centrality_df : pandas.DataFrame, optional
        DataFrame with centrality measures (for correlation analysis)
    output_dir : str
        Directory to save results
    
    Returns:
    --------
    dict
        All analysis results
    """
    print("="*60)
    print("ADVANCED NETWORK ANALYSIS")
    print("="*60)
    
    results = {}
    
    # 1. Additional centrality measures
    print("\n1. Computing additional centrality measures...")
    katz = compute_katz_centrality(G)
    harmonic = compute_harmonic_centrality(G)
    results['additional_centrality'] = {
        'katz': katz,
        'harmonic': harmonic
    }
    
    # 2. Motif detection
    print("\n2. Detecting network motifs...")
    motif_results = detect_3node_motifs(G, sample_size=5000 if G.number_of_nodes() > 5000 else None)
    motif_significance = compute_motif_significance(G, motif_results, n_random=50)
    results['motifs'] = {
        'counts': motif_results['counts'],
        'frequencies': motif_results['frequencies'],
        'significance': motif_significance
    }
    
    # 3. Path analysis
    print("\n3. Analyzing network paths...")
    path_results = analyze_paths(G)
    results['paths'] = path_results
    
    # 4. Statistical analysis
    print("\n4. Performing statistical analysis...")
    stats_results = analyze_network_statistics(G)
    results['statistics'] = stats_results
    
    # 5. Centrality correlations
    if centrality_df is not None:
        print("\n5. Computing centrality correlations...")
        correlation_matrix = compute_centrality_correlations(centrality_df)
        results['centrality_correlations'] = correlation_matrix
    
    # Save results
    print("\nSaving results...")
    save_advanced_results(results, output_dir)
    
    return results


def save_advanced_results(results, output_dir='.'):
    """Save advanced analysis results to files."""
    from pathlib import Path
    output_path = Path(output_dir)
    
    # Save additional centrality measures
    if 'additional_centrality' in results:
        katz_df = pd.DataFrame([
            {'protein_id': node, 'katz_centrality': score}
            for node, score in results['additional_centrality']['katz'].items()
        ])
        harmonic_df = pd.DataFrame([
            {'protein_id': node, 'harmonic_centrality': score}
            for node, score in results['additional_centrality']['harmonic'].items()
        ])
        katz_df.to_csv(output_path / 'katz_centrality.csv', index=False)
        harmonic_df.to_csv(output_path / 'harmonic_centrality.csv', index=False)
    
    # Save motif results
    if 'motifs' in results:
        motif_df = pd.DataFrame([
            {
                'motif_type': motif_type,
                'count': data.get('observed', 0),
                'z_score': data.get('z_score', 0),
                'mean_random': data.get('mean_random', 0),
                'std_random': data.get('std_random', 0)
            }
            for motif_type, data in results['motifs']['significance'].items()
        ])
        motif_df.to_csv(output_path / 'motif_analysis.csv', index=False)
    
    # Save path analysis
    if 'paths' in results:
        path_df = pd.DataFrame([results['paths']])
        path_df.to_csv(output_path / 'path_analysis.csv', index=False)
    
    # Save statistics
    if 'statistics' in results:
        stats_data = results['statistics']
        stats_df = pd.DataFrame([{
            'metric': 'average_degree',
            'value': stats_data['degree_distribution']['mean']
        }, {
            'metric': 'power_law_gamma',
            'value': stats_data['power_law'].get('gamma', 0)
        }, {
            'metric': 'average_clustering',
            'value': stats_data['clustering']['average']
        }, {
            'metric': 'average_path_length',
            'value': stats_data['small_world'].get('average_path_length', 0)
        }])
        stats_df.to_csv(output_path / 'network_statistics.csv', index=False)
    
    # Save centrality correlations
    if 'centrality_correlations' in results and not results['centrality_correlations'].empty:
        results['centrality_correlations'].to_csv(output_path / 'centrality_correlations.csv')
    
    print(f"Results saved to {output_path}")


if __name__ == "__main__":
    import sys
    from build_graph import load_graph
    
    graph_file = sys.argv[1] if len(sys.argv) > 1 else 'string_network.graphml'
    
    # Load graph
    G = load_graph(graph_file)
    
    # Load centrality results if available
    centrality_df = None
    try:
        centrality_df = pd.read_csv('centrality_results.csv')
    except:
        pass
    
    # Run advanced analysis
    results = run_advanced_analysis(G, centrality_df)
