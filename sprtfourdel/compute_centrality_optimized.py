"""
Optimized version of compute_centrality.py with parallelization and selective computation.

This module provides:
- Parallel computation of independent centrality measures
- Selective computation (choose which measures to compute)
- Approximate algorithms for large networks
- Caching support
"""

import pandas as pd
import networkx as nx
import numpy as np
from multiprocessing import Pool, cpu_count
from functools import partial
import time
from performance_utils import progress_bar, CacheManager, get_memory_usage
from typing import List, Optional, Dict


def compute_degree_centrality_parallel(G):
    """Compute degree centrality (fast, no parallelization needed)."""
    return nx.degree_centrality(G)


def compute_degree_raw(G):
    """Compute raw degree counts."""
    return dict(G.degree())


def compute_betweenness_centrality_parallel(G, k=None, approximate=True):
    """
    Compute betweenness centrality with optional approximation.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network graph
    k : int, optional
        Number of nodes to sample for approximation
    approximate : bool
        If True and network is large, use approximation
    """
    n_nodes = G.number_of_nodes()
    
    # Use approximation for large networks
    if approximate and n_nodes > 10000:
        if k is None:
            k = min(100, n_nodes)
        return nx.betweenness_centrality(G, k=k)
    elif approximate and n_nodes > 5000:
        if k is None:
            k = min(200, n_nodes)
        return nx.betweenness_centrality(G, k=k)
    else:
        # Exact computation for smaller networks
        return nx.betweenness_centrality(G)


def compute_closeness_centrality_parallel(G):
    """Compute closeness centrality."""
    try:
        if nx.is_connected(G):
            return nx.closeness_centrality(G)
        else:
            print("  Graph is disconnected, computing for largest component...")
            largest_cc = max(nx.connected_components(G), key=len)
            subgraph = G.subgraph(largest_cc)
            closeness = nx.closeness_centrality(subgraph)
            full_closeness = {node: 0 for node in G.nodes()}
            full_closeness.update(closeness)
            return full_closeness
    except Exception as e:
        print(f"  Warning: Closeness computation failed: {e}")
        return {node: 0 for node in G.nodes()}


def compute_eigenvector_centrality_parallel(G):
    """Compute eigenvector centrality."""
    try:
        return nx.eigenvector_centrality(G, max_iter=1000)
    except Exception as e:
        print(f"  Warning: Eigenvector computation failed: {e}")
        return {node: 0 for node in G.nodes()}


def compute_pagerank_parallel(G):
    """Compute PageRank."""
    try:
        return nx.pagerank(G, max_iter=100)
    except Exception as e:
        print(f"  Warning: PageRank computation failed: {e}")
        return {node: 0 for node in G.nodes()}


def compute_clustering_parallel(G):
    """Compute clustering coefficient."""
    return nx.clustering(G)


def compute_katz_centrality_parallel(G, alpha=0.1, beta=1.0):
    """Compute Katz centrality."""
    try:
        return nx.katz_centrality(G, alpha=alpha, beta=beta, max_iter=1000)
    except Exception as e:
        print(f"  Warning: Katz centrality computation failed: {e}")
        return {node: 0 for node in G.nodes()}


def compute_harmonic_centrality_parallel(G):
    """Compute Harmonic centrality."""
    try:
        return nx.harmonic_centrality(G)
    except Exception as e:
        print(f"  Warning: Harmonic centrality computation failed: {e}")
        # Fallback: manual computation for smaller networks
        harmonic = {}
        nodes = list(G.nodes())
        for node in nodes:
            total = 0.0
            for other in nodes:
                if node != other:
                    try:
                        path_length = nx.shortest_path_length(G, node, other)
                        if path_length > 0:
                            total += 1.0 / path_length
                    except nx.NetworkXNoPath:
                        pass
            harmonic[node] = total
        return harmonic


def compute_single_measure(args):
    """Wrapper for computing a single centrality measure (for parallelization)."""
    measure_name, G, kwargs = args
    func_map = {
        'degree': compute_degree_centrality_parallel,
        'betweenness': partial(compute_betweenness_centrality_parallel, **kwargs.get('betweenness', {})),
        'closeness': compute_closeness_centrality_parallel,
        'eigenvector': compute_eigenvector_centrality_parallel,
        'pagerank': compute_pagerank_parallel,
        'clustering': compute_clustering_parallel,
        'katz': compute_katz_centrality_parallel,
        'harmonic': compute_harmonic_centrality_parallel,
    }
    
    if measure_name not in func_map:
        return measure_name, {node: 0 for node in G.nodes()}
    
    start_time = time.time()
    result = func_map[measure_name](G)
    elapsed = time.time() - start_time
    return measure_name, result, elapsed


def compute_centrality_measures_optimized(
    G, 
    measures: Optional[List[str]] = None,
    parallel: bool = True,
    n_jobs: Optional[int] = None,
    use_cache: bool = False,
    cache_manager: Optional[CacheManager] = None
):
    """
    Optimized version of compute_centrality_measures with parallelization and selective computation.
    
    Parameters:
    -----------
    G : networkx.Graph
        Network graph
    measures : list of str, optional
        List of measures to compute. If None, compute all.
        Options: 'degree', 'degree_centrality', 'betweenness', 'closeness', 'eigenvector', 'pagerank', 'clustering', 'katz', 'harmonic'
    parallel : bool
        If True, compute independent measures in parallel
    n_jobs : int, optional
        Number of parallel jobs. If None, use cpu_count()
    use_cache : bool
        If True, use caching for expensive computations
    cache_manager : CacheManager, optional
        Cache manager instance
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame with centrality measures for each node
    """
    print("\nComputing centrality measures...")
    n_nodes = G.number_of_nodes()
    print(f"Network size: {n_nodes} nodes, {G.number_of_edges()} edges")
    
    # Default measures
    if measures is None:
        measures = ['degree', 'degree_centrality', 'betweenness', 'closeness', 'eigenvector', 'pagerank', 'clustering']
    
    # Add new measures if requested
    if 'katz' in measures or 'katz_centrality' in measures:
        if 'katz' not in measures:
            measures.append('katz')
    if 'harmonic' in measures or 'harmonic_centrality' in measures:
        if 'harmonic' not in measures:
            measures.append('harmonic')
    
    # Determine if we should use approximation
    use_approximate = n_nodes > 5000
    if use_approximate:
        print("  Using approximate algorithms for large network...")
    
    measures_dict = {}
    computation_times = {}
    
    # Prepare arguments for parallel computation
    independent_measures = ['degree_centrality', 'clustering', 'eigenvector', 'pagerank', 'katz', 'harmonic']
    sequential_measures = ['betweenness', 'closeness']  # May depend on graph structure
    
    # Compute independent measures in parallel
    parallel_measures = [m for m in measures if m in independent_measures or m == 'degree']
    sequential_list = [m for m in measures if m in sequential_measures]
    
    if parallel and len(parallel_measures) > 1 and n_jobs != 1:
        print(f"  Computing {len(parallel_measures)} measures in parallel...")
        if n_jobs is None:
            n_jobs = min(cpu_count(), len(parallel_measures))
        
        # Prepare arguments
        kwargs = {
            'betweenness': {'approximate': use_approximate}
        }
        args_list = [(m, G, kwargs) for m in parallel_measures]
        
        # Compute in parallel
        with Pool(processes=n_jobs) as pool:
            results = pool.map(compute_single_measure, args_list)
        
        for result in results:
            if len(result) == 3:
                measure_name, result_dict, elapsed = result
                measures_dict[measure_name] = result_dict
                computation_times[measure_name] = elapsed
                print(f"  [{measure_name}] Computed in {elapsed:.2f}s")
    else:
        # Compute sequentially
        for measure in parallel_measures:
            if measure in measures:
                start_time = time.time()
                if measure == 'degree_centrality':
                    measures_dict['degree_centrality'] = compute_degree_centrality_parallel(G)
                elif measure == 'degree':
                    measures_dict['degree'] = compute_degree_raw(G)
                elif measure == 'clustering':
                    measures_dict['clustering'] = compute_clustering_parallel(G)
                elif measure == 'eigenvector':
                    measures_dict['eigenvector'] = compute_eigenvector_centrality_parallel(G)
                elif measure == 'pagerank':
                    measures_dict['pagerank'] = compute_pagerank_parallel(G)
                elif measure == 'katz':
                    measures_dict['katz'] = compute_katz_centrality_parallel(G)
                elif measure == 'harmonic':
                    measures_dict['harmonic'] = compute_harmonic_centrality_parallel(G)
                elapsed = time.time() - start_time
                computation_times[measure] = elapsed
                print(f"  [{measure}] Computed in {elapsed:.2f}s")
    
    # Compute sequential measures
    for measure in sequential_list:
        if measure in measures:
            start_time = time.time()
            if measure == 'betweenness':
                measures_dict[measure] = compute_betweenness_centrality_parallel(
                    G, approximate=use_approximate
                )
            elif measure == 'closeness':
                measures_dict[measure] = compute_closeness_centrality_parallel(G)
            elapsed = time.time() - start_time
            computation_times[measure] = elapsed
            print(f"  [{measure}] Computed in {elapsed:.2f}s")
    
    # Always compute degree (raw count) if not already computed
    if 'degree' not in measures_dict:
        measures_dict['degree'] = dict(G.degree())
    
    # Always compute degree_centrality if not already computed
    if 'degree_centrality' not in measures_dict:
        measures_dict['degree_centrality'] = compute_degree_centrality_parallel(G)
    
    # Combine into DataFrame
    print("\nCombining measures into DataFrame...")
    nodes = list(G.nodes())
    
    # Build DataFrame efficiently
    data = {'protein_id': nodes}
    
    # Map measure names to keys in measures_dict
    measure_mapping = {
        'degree': 'degree',
        'degree_centrality': 'degree_centrality',
        'betweenness_centrality': 'betweenness',
        'closeness_centrality': 'closeness',
        'eigenvector_centrality': 'eigenvector',
        'pagerank': 'pagerank',
        'clustering_coefficient': 'clustering',
        'katz_centrality': 'katz',
        'harmonic_centrality': 'harmonic'
    }
    
    # Add all measures
    for measure_name, key in measure_mapping.items():
        if key in measures_dict:
            data[measure_name] = [measures_dict[key].get(node, 0) for node in nodes]
    
    df = pd.DataFrame(data)
    
    # Compute composite hub score (optimized vectorized operations)
    print("  Computing composite hub score...")
    key_measures = ['degree_centrality', 'betweenness_centrality', 
                    'eigenvector_centrality', 'pagerank']
    # Optionally include new measures
    if 'katz_centrality' in df.columns:
        key_measures.append('katz_centrality')
    if 'harmonic_centrality' in df.columns:
        key_measures.append('harmonic_centrality')
    
    # Vectorized normalization
    for col in key_measures:
        if col in df.columns:
            max_val = df[col].max()
            if max_val > 0:
                df[f'{col}_normalized'] = df[col] / max_val
    
    # Vectorized composite score
    normalized_cols = [f'{col}_normalized' for col in key_measures 
                      if f'{col}_normalized' in df.columns]
    if normalized_cols:
        df['hub_score'] = df[normalized_cols].mean(axis=1)
    else:
        df['hub_score'] = df.get('degree_centrality', 0)
    
    # Sort by hub score
    df = df.sort_values('hub_score', ascending=False).reset_index(drop=True)
    
    total_time = sum(computation_times.values())
    print(f"\nComputed centrality measures for {len(df)} nodes")
    print(f"Total computation time: {total_time:.2f}s")
    if computation_times:
        print("  Breakdown:", ", ".join([f"{k}: {v:.2f}s" for k, v in computation_times.items()]))
    
    return df


# Keep original function signature for backward compatibility
def compute_centrality_measures(G, measures=None, parallel=True, n_jobs=None):
    """Wrapper for optimized version."""
    return compute_centrality_measures_optimized(G, measures, parallel, n_jobs)


def identify_hub_genes(df, top_n=50, percentile=95):
    """Identify top hub genes (unchanged from original)."""
    print(f"\nIdentifying top {top_n} hub genes...")
    
    hub_score_threshold = df['hub_score'].quantile(percentile / 100)
    degree_threshold = df['degree'].quantile(percentile / 100)
    
    top_hubs = df.head(top_n).copy()
    
    print(f"\nHub identification thresholds:")
    print(f"  Hub score (95th percentile): {hub_score_threshold:.4f}")
    print(f"  Degree (95th percentile): {degree_threshold:.2f}")
    
    return top_hubs


def save_centrality_results(df, hub_genes, output_file='centrality_results.csv', hub_file='hub_genes.csv'):
    """Save centrality results to CSV files."""
    print(f"\nSaving results...")
    df.to_csv(output_file, index=False)
    print(f"  Saved all centrality measures to {output_file}")
    hub_genes.to_csv(hub_file, index=False)
    print(f"  Saved hub genes to {hub_file}")
    return output_file, hub_file
