"""
Performance benchmark script for network analysis pipeline.

This script benchmarks the pipeline with various network sizes to measure
performance improvements.
"""

import time
import pandas as pd
import networkx as nx
from pathlib import Path
import json
from performance_utils import get_memory_usage, profile_function
import sys

# Import both original and optimized versions
try:
    from clean_data import load_string_data as load_orig, clean_string_data as clean_orig
    from clean_data_optimized import load_string_data as load_opt, clean_string_data as clean_opt
except ImportError:
    print("Warning: Could not import all modules")
    sys.exit(1)

try:
    from compute_centrality import compute_centrality_measures as compute_orig
    from compute_centrality_optimized import compute_centrality_measures_optimized as compute_opt
except ImportError:
    print("Warning: Could not import centrality modules")
    sys.exit(1)

try:
    from build_graph import build_network_graph as build_orig
    from build_graph_optimized import build_network_graph_optimized as build_opt
except ImportError:
    print("Warning: Could not import graph building modules")
    build_opt = None


def generate_test_data(n_interactions=1000, output_file='test_data.csv'):
    """Generate test data for benchmarking."""
    import random
    genes = [f"GENE_{i:04d}" for i in range(1, min(1000, n_interactions // 2))]
    
    interactions = []
    seen = set()
    for _ in range(n_interactions):
        g1 = random.choice(genes)
        g2 = random.choice(genes)
        if g1 != g2:
            pair = tuple(sorted([g1, g2]))
            if pair not in seen:
                seen.add(pair)
                interactions.append({
                    'protein1': f"9606.{g1}",
                    'protein2': f"9606.{g2}",
                    'combined_score': random.randint(400, 1000)
                })
    
    df = pd.DataFrame(interactions)
    df.to_csv(output_file, index=False)
    return output_file


def benchmark_data_cleaning(input_file, use_optimized=True):
    """Benchmark data cleaning step."""
    start_time = time.time()
    start_memory = get_memory_usage()
    
    if use_optimized:
        df = load_opt(input_file, use_chunked=False)
        df_cleaned = clean_opt(df, use_chunked=False)
    else:
        df = load_orig(input_file)
        df_cleaned = clean_orig(df)
    
    end_time = time.time()
    end_memory = get_memory_usage()
    
    return {
        'time': end_time - start_time,
        'memory_delta': end_memory - start_memory,
        'rows_processed': len(df_cleaned)
    }


def benchmark_graph_building(df, use_optimized=True):
    """Benchmark graph building step."""
    start_time = time.time()
    start_memory = get_memory_usage()
    
    if use_optimized and build_opt:
        G = build_opt(df)
    else:
        from build_graph import build_network_graph
        G = build_network_graph(df)
    
    end_time = time.time()
    end_memory = get_memory_usage()
    
    return {
        'time': end_time - start_time,
        'memory_delta': end_memory - start_memory,
        'nodes': G.number_of_nodes(),
        'edges': G.number_of_edges()
    }


def benchmark_centrality(G, use_optimized=True, parallel=True):
    """Benchmark centrality computation."""
    start_time = time.time()
    start_memory = get_memory_usage()
    
    if use_optimized:
        df = compute_opt(G, parallel=parallel)
    else:
        df = compute_orig(G)
    
    end_time = time.time()
    end_memory = get_memory_usage()
    
    return {
        'time': end_time - start_time,
        'memory_delta': end_memory - start_memory,
        'nodes_processed': len(df)
    }


def run_benchmark_suite(network_sizes=[100, 500, 1000, 5000]):
    """Run complete benchmark suite."""
    results = []
    
    for size in network_sizes:
        print(f"\n{'='*60}")
        print(f"Benchmarking with {size} interactions")
        print(f"{'='*60}")
        
        # Generate test data
        test_file = f'test_benchmark_{size}.csv'
        generate_test_data(size, test_file)
        
        # Benchmark data cleaning
        print("\n[Data Cleaning]")
        print("  Original version...")
        clean_orig_result = benchmark_data_cleaning(test_file, use_optimized=False)
        print(f"    Time: {clean_orig_result['time']:.2f}s, Memory: {clean_orig_result['memory_delta']:.1f} MB")
        
        print("  Optimized version...")
        clean_opt_result = benchmark_data_cleaning(test_file, use_optimized=True)
        print(f"    Time: {clean_opt_result['time']:.2f}s, Memory: {clean_opt_result['memory_delta']:.1f} MB")
        
        speedup = clean_orig_result['time'] / clean_opt_result['time'] if clean_opt_result['time'] > 0 else 1
        print(f"    Speedup: {speedup:.2f}x")
        
        # Load cleaned data for graph building
        df_cleaned_orig = clean_orig(load_orig(test_file))
        df_cleaned_opt = clean_opt(load_opt(test_file))
        
        # Benchmark graph building
        print("\n[Graph Building]")
        if build_opt:
            print("  Original version...")
            build_orig_result = benchmark_graph_building(df_cleaned_orig, use_optimized=False)
            print(f"    Time: {build_orig_result['time']:.2f}s")
            
            print("  Optimized version...")
            build_opt_result = benchmark_graph_building(df_cleaned_opt, use_optimized=True)
            print(f"    Time: {build_opt_result['time']:.2f}s")
        else:
            build_orig_result = benchmark_graph_building(df_cleaned_orig, use_optimized=False)
            build_opt_result = build_orig_result
        
        # Build graphs for centrality benchmark
        from build_graph import build_network_graph
        G_orig = build_network_graph(df_cleaned_orig)
        G_opt = build_network_graph(df_cleaned_opt) if not build_opt else build_opt(df_cleaned_opt)
        
        # Benchmark centrality computation
        print("\n[Centrality Computation]")
        print("  Original version...")
        compute_orig_result = benchmark_centrality(G_orig, use_optimized=False)
        print(f"    Time: {compute_orig_result['time']:.2f}s")
        
        print("  Optimized version (parallel)...")
        compute_opt_result = benchmark_centrality(G_opt, use_optimized=True, parallel=True)
        print(f"    Time: {compute_opt_result['time']:.2f}s")
        
        speedup_centrality = compute_orig_result['time'] / compute_opt_result['time'] if compute_opt_result['time'] > 0 else 1
        print(f"    Speedup: {speedup_centrality:.2f}x")
        
        # Store results
        results.append({
            'network_size': size,
            'cleaning_original_time': clean_orig_result['time'],
            'cleaning_optimized_time': clean_opt_result['time'],
            'cleaning_speedup': speedup,
            'graph_building_original_time': build_orig_result['time'],
            'graph_building_optimized_time': build_opt_result['time'],
            'centrality_original_time': compute_orig_result['time'],
            'centrality_optimized_time': compute_opt_result['time'],
            'centrality_speedup': speedup_centrality,
        })
        
        # Cleanup
        Path(test_file).unlink(missing_ok=True)
    
    return results


def save_benchmark_results(results, output_file='benchmark_results.json'):
    """Save benchmark results to JSON file."""
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nBenchmark results saved to {output_file}")


if __name__ == "__main__":
    print("="*60)
    print("PERFORMANCE BENCHMARK SUITE")
    print("="*60)
    
    # Run benchmarks
    results = run_benchmark_suite(network_sizes=[100, 500, 1000])
    
    # Save results
    save_benchmark_results(results)
    
    # Print summary
    print("\n" + "="*60)
    print("BENCHMARK SUMMARY")
    print("="*60)
    df_results = pd.DataFrame(results)
    print(df_results.to_string(index=False))
