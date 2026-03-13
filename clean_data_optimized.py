"""
Optimized version of clean_data.py with chunked processing and memory optimization.

This module provides memory-efficient data loading and cleaning for large datasets.
"""

import pandas as pd
import numpy as np
from performance_utils import progress_bar, get_memory_usage, check_memory_threshold
import os


def load_string_data_chunked(input_file='string_homo_sapiens.csv', chunksize=10000):
    """
    Load STRING data from CSV file in chunks for memory efficiency.
    
    Parameters:
    -----------
    input_file : str
        Path to input CSV file
    chunksize : int
        Number of rows to read per chunk
    
    Yields:
    -------
    pandas.DataFrame
        Chunk of data
    """
    print(f"Loading data from {input_file} in chunks of {chunksize}...")
    
    # Check file size to decide if chunking is needed
    file_size = os.path.getsize(input_file) / (1024 * 1024)  # MB
    if file_size < 50:  # Less than 50MB, load normally
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} interactions")
        yield df
        return
    
    # Load in chunks
    total_rows = 0
    for chunk in progress_bar(pd.read_csv(input_file, chunksize=chunksize), 
                              desc="Loading chunks"):
        total_rows += len(chunk)
        yield chunk
    
    print(f"Loaded {total_rows} interactions total")


def clean_string_data_optimized(df, use_chunked=False):
    """
    Optimized version of clean_string_data with memory-efficient operations.
    
    Parameters:
    -----------
    df : pandas.DataFrame or generator
        Raw STRING interaction data (or generator of chunks)
    use_chunked : bool
        If True, process data in chunks
    """
    if use_chunked:
        return _clean_chunked(df)
    else:
        return _clean_single(df)


def _clean_single(df):
    """Clean a single DataFrame."""
    print("\nCleaning dataset...")
    print(f"Initial shape: {df.shape}")
    initial_memory = get_memory_usage()
    
    # Remove any rows with missing values
    initial_count = len(df)
    df = df.dropna()
    print(f"Removed {initial_count - len(df)} rows with missing values")
    
    # Ensure we have the required columns
    required_cols = ['protein1', 'protein2']
    if not all(col in df.columns for col in required_cols):
        if len(df.columns) >= 2:
            df.columns = ['protein1', 'protein2'] + list(df.columns[2:])
        else:
            raise ValueError("DataFrame must contain protein1 and protein2 columns")
    
    # Extract gene identifiers (vectorized operation)
    print("Extracting gene identifiers...")
    df['protein1_clean'] = df['protein1'].str.replace(r'^\d+\.', '', regex=True)
    df['protein2_clean'] = df['protein2'].str.replace(r'^\d+\.', '', regex=True)
    
    # Filter by confidence score if available
    if 'combined_score' in df.columns:
        initial_count = len(df)
        df = df[df['combined_score'] >= 400]
        print(f"Filtered to medium+ confidence interactions: {len(df)} (removed {initial_count - len(df)})")
    
    # Remove self-interactions (vectorized)
    initial_count = len(df)
    df = df[df['protein1_clean'] != df['protein2_clean']]
    print(f"Removed {initial_count - len(df)} self-interactions")
    
    # Remove duplicate interactions (optimized)
    initial_count = len(df)
    # Create sorted pairs for deduplication
    pairs = pd.DataFrame({
        'p1': df[['protein1_clean', 'protein2_clean']].min(axis=1),
        'p2': df[['protein1_clean', 'protein2_clean']].max(axis=1)
    })
    df = df[~pairs.duplicated()].copy()
    print(f"Removed {initial_count - len(df)} duplicate interactions")
    
    # Reset index
    df = df.reset_index(drop=True)
    
    final_memory = get_memory_usage()
    print(f"\nFinal cleaned dataset shape: {df.shape}")
    print(f"Unique proteins: {len(set(df['protein1_clean'].tolist() + df['protein2_clean'].tolist()))}")
    print(f"Memory usage: {final_memory - initial_memory:.1f} MB")
    
    # Check memory threshold
    check_memory_threshold()
    
    return df


def _clean_chunked(chunk_generator):
    """Clean data in chunks and combine results."""
    print("\nCleaning dataset in chunks...")
    cleaned_chunks = []
    total_initial = 0
    
    for chunk in progress_bar(chunk_generator, desc="Cleaning chunks"):
        total_initial += len(chunk)
        cleaned = _clean_single(chunk)
        cleaned_chunks.append(cleaned)
    
    print(f"\nCombining {len(cleaned_chunks)} cleaned chunks...")
    df_combined = pd.concat(cleaned_chunks, ignore_index=True)
    
    # Final deduplication across chunks
    initial_count = len(df_combined)
    pairs = pd.DataFrame({
        'p1': df_combined[['protein1_clean', 'protein2_clean']].min(axis=1),
        'p2': df_combined[['protein1_clean', 'protein2_clean']].max(axis=1)
    })
    df_combined = df_combined[~pairs.duplicated()].copy()
    df_combined = df_combined.reset_index(drop=True)
    
    print(f"Final combined dataset: {len(df_combined)} interactions "
          f"(removed {initial_count - len(df_combined)} duplicates across chunks)")
    
    return df_combined


def load_string_data(input_file='string_homo_sapiens.csv', use_chunked=False):
    """Load STRING data from CSV file (with optional chunking)."""
    if use_chunked:
        # Return generator
        return load_string_data_chunked(input_file)
    else:
        print(f"Loading data from {input_file}...")
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} interactions")
        return df


def clean_string_data(df, use_chunked=False):
    """Clean STRING data (wrapper for optimized version)."""
    if hasattr(df, '__iter__') and not isinstance(df, pd.DataFrame):
        # It's a generator
        return clean_string_data_optimized(df, use_chunked=True)
    else:
        return clean_string_data_optimized(df, use_chunked=False)


# Keep original functions for backward compatibility
def save_cleaned_data(df, output_file='string_cleaned.csv'):
    """Save cleaned data to CSV."""
    print(f"\nSaving cleaned data to {output_file}...")
    df.to_csv(output_file, index=False)
    print("Data saved successfully!")
    return output_file


def get_data_statistics(df):
    """Print statistics about the cleaned dataset."""
    print("\n" + "="*50)
    print("DATASET STATISTICS")
    print("="*50)
    
    all_proteins = set(df['protein1_clean'].tolist() + df['protein2_clean'].tolist())
    
    print(f"Total interactions: {len(df)}")
    print(f"Unique proteins: {len(all_proteins)}")
    
    if 'combined_score' in df.columns:
        print(f"\nConfidence Score Statistics:")
        print(f"  Mean: {df['combined_score'].mean():.2f}")
        print(f"  Median: {df['combined_score'].median():.2f}")
        print(f"  Min: {df['combined_score'].min():.2f}")
        print(f"  Max: {df['combined_score'].max():.2f}")
        print(f"  Std: {df['combined_score'].std():.2f}")
    
    # Count interactions per protein (optimized)
    protein_counts = pd.concat([
        df['protein1_clean'].value_counts(),
        df['protein2_clean'].value_counts()
    ]).groupby(level=0).sum()
    
    if len(protein_counts) > 0:
        counts = protein_counts.values
        print(f"\nProtein Interaction Counts:")
        print(f"  Mean interactions per protein: {np.mean(counts):.2f}")
        print(f"  Median interactions per protein: {np.median(counts):.2f}")
        print(f"  Max interactions: {max(counts)}")
        print(f"  Min interactions: {min(counts)}")
    
    print("="*50)
