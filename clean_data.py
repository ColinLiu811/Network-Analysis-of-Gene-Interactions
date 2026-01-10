"""
Clean and format STRING dataset using Pandas.

This script processes the raw STRING data, cleans it, and prepares it
for graph analysis.
"""

import pandas as pd
import numpy as np

def load_string_data(input_file='string_homo_sapiens.csv'):
    """Load STRING data from CSV file."""
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    print(f"Loaded {len(df)} interactions")
    return df

def clean_string_data(df):
    """
    Clean and format STRING dataset.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Raw STRING interaction data
    """
    print("\nCleaning dataset...")
    print(f"Initial shape: {df.shape}")
    
    # Remove any rows with missing values
    initial_count = len(df)
    df = df.dropna()
    print(f"Removed {initial_count - len(df)} rows with missing values")
    
    # Ensure we have the required columns
    required_cols = ['protein1', 'protein2']
    if not all(col in df.columns for col in required_cols):
        # Try to identify columns
        if len(df.columns) >= 2:
            df.columns = ['protein1', 'protein2'] + list(df.columns[2:])
        else:
            raise ValueError("DataFrame must contain protein1 and protein2 columns")
    
    # Extract gene names from protein IDs (STRING format: species.ENSP...)
    # We'll keep the full protein IDs for now, but can extract gene names
    print("Extracting gene identifiers...")
    
    # Remove species prefix if present (e.g., "9606.ENSP..." -> "ENSP...")
    df['protein1_clean'] = df['protein1'].str.replace(r'^\d+\.', '', regex=True)
    df['protein2_clean'] = df['protein2'].str.replace(r'^\d+\.', '', regex=True)
    
    # Filter by confidence score if available
    if 'combined_score' in df.columns:
        # STRING scores range from 0-1000
        # Medium confidence: >= 400, High confidence: >= 700
        initial_count = len(df)
        df = df[df['combined_score'] >= 400]  # Medium confidence threshold
        print(f"Filtered to medium+ confidence interactions: {len(df)} (removed {initial_count - len(df)})")
    
    # Remove self-interactions
    initial_count = len(df)
    df = df[df['protein1_clean'] != df['protein2_clean']]
    print(f"Removed {initial_count - len(df)} self-interactions")
    
    # Remove duplicate interactions (A-B is same as B-A)
    initial_count = len(df)
    df['interaction_pair'] = df.apply(
        lambda x: tuple(sorted([x['protein1_clean'], x['protein2_clean']])), 
        axis=1
    )
    df = df.drop_duplicates(subset=['interaction_pair'])
    df = df.drop('interaction_pair', axis=1)
    print(f"Removed {initial_count - len(df)} duplicate interactions")
    
    # Reset index
    df = df.reset_index(drop=True)
    
    print(f"\nFinal cleaned dataset shape: {df.shape}")
    print(f"Unique proteins: {len(set(df['protein1_clean'].tolist() + df['protein2_clean'].tolist()))}")
    
    return df

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
    
    # Count interactions per protein
    protein_counts = {}
    for _, row in df.iterrows():
        p1 = row['protein1_clean']
        p2 = row['protein2_clean']
        protein_counts[p1] = protein_counts.get(p1, 0) + 1
        protein_counts[p2] = protein_counts.get(p2, 0) + 1
    
    if protein_counts:
        counts = list(protein_counts.values())
        print(f"\nProtein Interaction Counts:")
        print(f"  Mean interactions per protein: {np.mean(counts):.2f}")
        print(f"  Median interactions per protein: {np.median(counts):.2f}")
        print(f"  Max interactions: {max(counts)}")
        print(f"  Min interactions: {min(counts)}")
    
    print("="*50)

if __name__ == "__main__":
    import sys
    
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'string_homo_sapiens.csv'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'string_cleaned.csv'
    
    # Load data
    df = load_string_data(input_file)
    
    # Clean data
    df_cleaned = clean_string_data(df)
    
    # Get statistics
    get_data_statistics(df_cleaned)
    
    # Save cleaned data
    save_cleaned_data(df_cleaned, output_file)
    
    print("\nNext step: Run build_graph.py to create the network graph")
