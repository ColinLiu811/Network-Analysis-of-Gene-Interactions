"""
Data preprocessing module for gene interaction data.
"""

import pandas as pd
from pathlib import Path


class DataProcessor:
    """Handles loading and preprocessing of gene interaction data."""
    
    def __init__(self, input_file, confidence_threshold=0.0):
        """
        Initialize the data processor.
        
        Args:
            input_file: Path to input CSV/TSV file
            confidence_threshold: Minimum confidence score to keep (default: 0.0)
        """
        self.input_file = Path(input_file)
        self.confidence_threshold = confidence_threshold
    
    def load_data(self):
        """Load data from CSV or TSV file."""
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_file}")
        
        # Try to detect delimiter
        with open(self.input_file, 'r') as f:
            first_line = f.readline()
            delimiter = '\t' if '\t' in first_line else ','
        
        # Load the data
        df = pd.read_csv(self.input_file, delimiter=delimiter)
        
        # Expected columns: GeneA, GeneB, and optionally Score/Confidence
        required_cols = ['GeneA', 'GeneB']
        if not all(col in df.columns for col in required_cols):
            # Try case-insensitive matching
            df.columns = df.columns.str.strip()
            col_map = {}
            for col in df.columns:
                col_lower = col.lower()
                if 'genea' in col_lower or 'gene_a' in col_lower:
                    col_map[col] = 'GeneA'
                elif 'geneb' in col_lower or 'gene_b' in col_lower:
                    col_map[col] = 'GeneB'
                elif 'score' in col_lower or 'confidence' in col_lower:
                    col_map[col] = 'Score'
            
            df = df.rename(columns=col_map)
            
            if not all(col in df.columns for col in required_cols):
                raise ValueError(
                    f"Input file must contain 'GeneA' and 'GeneB' columns. "
                    f"Found columns: {list(df.columns)}"
                )
        
        return df
    
    def process(self):
        """
        Process the data: remove duplicates and filter by confidence.
        
        Returns:
            Cleaned pandas DataFrame
        """
        df = self.load_data()
        
        print(f"  Original data: {len(df)} interactions")
        
        # Remove rows with missing gene names
        df = df.dropna(subset=['GeneA', 'GeneB'])
        df['GeneA'] = df['GeneA'].astype(str).str.strip()
        df['GeneB'] = df['GeneB'].astype(str).str.strip()
        
        # Remove self-interactions
        df = df[df['GeneA'] != df['GeneB']]
        
        # Remove duplicates (considering both directions: A-B and B-A are the same)
        # Create normalized pairs (always smaller gene first)
        df['pair'] = df.apply(
            lambda row: tuple(sorted([row['GeneA'], row['GeneB']])),
            axis=1
        )
        df = df.drop_duplicates(subset=['pair'], keep='first')
        df = df.drop(columns=['pair'])
        
        print(f"  After removing duplicates: {len(df)} interactions")
        
        # Filter by confidence score if available
        if 'Score' in df.columns:
            initial_count = len(df)
            df['Score'] = pd.to_numeric(df['Score'], errors='coerce')
            df = df[df['Score'] >= self.confidence_threshold]
            print(f"  After confidence filtering (>= {self.confidence_threshold}): {len(df)} interactions")
        else:
            print("  No confidence score column found, skipping score filtering")
        
        return df.reset_index(drop=True)

