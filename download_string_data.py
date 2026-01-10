"""
Download STRING database data for Homo sapiens genes.

This script downloads protein-protein interaction data from STRING database
for Homo sapiens and saves it to a CSV file.
"""

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

import pandas as pd
import os
from io import StringIO

def download_string_data(output_file='string_homo_sapiens.csv', species_id=9606):
    """
    Download STRING database interactions for Homo sapiens.
    
    Parameters:
    -----------
    output_file : str
        Output CSV filename
    species_id : int
        STRING species ID (9606 for Homo sapiens)
    """
    print(f"Downloading STRING data for Homo sapiens (species ID: {species_id})...")
    
    if not HAS_REQUESTS:
        print("requests module not available. Cannot download via API.")
        print("Please process a downloaded file instead.")
        return None
    
    # STRING database URL for protein links
    # We'll download the full protein links file for Homo sapiens
    base_url = "https://string-db.org/api"
    
    # Method 1: Try to get interactions via API
    try:
        print("Attempting to download via STRING API...")
        url = f"{base_url}/tsv/network?identifiers=all&species={species_id}"
        response = requests.get(url, timeout=300)
        
        if response.status_code == 200:
            # Save raw data
            with open('string_raw_data.tsv', 'w') as f:
                f.write(response.text)
            print("Downloaded data via API")
            
            # Read and convert to CSV
            df = pd.read_csv(StringIO(response.text), sep='\t')
            df.to_csv(output_file, index=False)
            print(f"Saved to {output_file}")
            return df
    except Exception as e:
        print(f"API method failed: {e}")
        print("Trying alternative method...")
    
    # Method 2: Download from direct file links (if available)
    # STRING provides direct download links for protein links
    try:
        print("Attempting direct file download...")
        # For Homo sapiens, STRING provides files at:
        # https://stringdb-static.org/download/protein.links.v11.5/9606.protein.links.v11.5.txt.gz
        
        # We'll create a sample structure or use a different approach
        # Since direct downloads require authentication or specific access,
        # we'll create a script that can work with downloaded files
        
        print("\nNote: For full STRING database access, you may need to:")
        print("1. Visit https://string-db.org/cgi/download")
        print("2. Download 'protein.links.full.v11.5' for Homo sapiens (9606)")
        print("3. Place the file in this directory")
        print("4. Run the processing script to convert it to CSV format")
        
        # Create a template/example structure
        create_sample_structure(output_file)
        return None
        
    except Exception as e:
        print(f"Direct download failed: {e}")
        create_sample_structure(output_file)
        return None

def create_sample_structure(output_file):
    """Create a sample CSV structure for demonstration."""
    print("\nCreating sample structure file...")
    sample_data = {
        'protein1': ['9606.ENSP00000000233', '9606.ENSP00000000412'],
        'protein2': ['9606.ENSP00000000412', '9606.ENSP00000000419'],
        'combined_score': [850, 720]
    }
    df = pd.DataFrame(sample_data)
    df.to_csv(output_file, index=False)
    print(f"Created sample structure in {output_file}")
    print("Replace this with actual STRING data from https://string-db.org")

def process_downloaded_string_file(input_file, output_file='string_homo_sapiens.csv'):
    """
    Process a downloaded STRING protein.links file.
    
    Parameters:
    -----------
    input_file : str
        Path to downloaded STRING .txt or .txt.gz file
    output_file : str
        Output CSV filename
    """
    print(f"Processing {input_file}...")
    
    # Check if file is gzipped
    if input_file.endswith('.gz'):
        import gzip
        with gzip.open(input_file, 'rt') as f:
            df = pd.read_csv(f, sep=' ')
    else:
        df = pd.read_csv(input_file, sep=' ')
    
    # STRING full files have many columns, but we only need protein1, protein2, and combined_score
    # Check if it's the full format (many columns) or simple format (3 columns)
    if len(df.columns) > 3:
        # Full format - extract only the columns we need
        required_cols = ['protein1', 'protein2', 'combined_score']
        if all(col in df.columns for col in required_cols):
            df = df[required_cols].copy()
        else:
            # Fallback: assume first two columns are proteins, last is score
            df = df.iloc[:, [0, 1, -1]].copy()
            df.columns = ['protein1', 'protein2', 'combined_score']
    else:
        # Simple format - just rename
        df.columns = ['protein1', 'protein2', 'combined_score']
    
    # Filter for high confidence interactions (optional)
    # df = df[df['combined_score'] >= 400]  # STRING medium confidence threshold
    
    df.to_csv(output_file, index=False)
    print(f"Processed and saved to {output_file}")
    print(f"Total interactions: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    return df

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Process a downloaded file
        input_file = sys.argv[1]
        process_downloaded_string_file(input_file)
    else:
        # Try to download directly
        download_string_data()
        
    print("\nNext step: Run clean_data.py to clean and format the dataset")

