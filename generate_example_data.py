#!/usr/bin/env python3
"""
Generate example gene interaction data for testing.
"""

import pandas as pd
import random
import argparse


def generate_example_data(n_genes=50, n_interactions=200, output_file='example_interactions.csv'):
    """
    Generate synthetic gene interaction data.
    
    Args:
        n_genes: Number of unique genes
        n_interactions: Number of interactions to generate
        output_file: Output CSV file path
    """
    # Generate gene names (using common gene naming conventions)
    genes = [f"GENE_{i:04d}" for i in range(1, n_genes + 1)]
    
    # Create interactions
    interactions = []
    seen_pairs = set()
    
    # Ensure we have enough unique pairs
    max_pairs = n_genes * (n_genes - 1) // 2
    n_interactions = min(n_interactions, max_pairs)
    
    while len(interactions) < n_interactions:
        gene_a = random.choice(genes)
        gene_b = random.choice(genes)
        
        if gene_a == gene_b:
            continue
        
        # Normalize pair (smaller first)
        pair = tuple(sorted([gene_a, gene_b]))
        
        if pair not in seen_pairs:
            seen_pairs.add(pair)
            # Generate confidence score (0.0 to 1.0)
            score = random.uniform(0.3, 1.0)
            interactions.append({
                'GeneA': gene_a,
                'GeneB': gene_b,
                'Score': round(score, 3)
            })
    
    # Create DataFrame
    df = pd.DataFrame(interactions)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Generated {len(df)} interactions between {n_genes} genes")
    print(f"Saved to: {output_file}")
    
    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate example gene interaction data')
    parser.add_argument(
        '-n', '--n-genes',
        type=int,
        default=50,
        help='Number of unique genes (default: 50)'
    )
    parser.add_argument(
        '-i', '--n-interactions',
        type=int,
        default=200,
        help='Number of interactions (default: 200)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='example_interactions.csv',
        help='Output file path (default: example_interactions.csv)'
    )
    
    args = parser.parse_args()
    generate_example_data(args.n_genes, args.n_interactions, args.output)

