"""
Automated pipeline to run the complete protein-protein interaction network analysis.

This script runs all steps of the analysis pipeline:
1. Download/process STRING data
2. Clean data
3. Build network graph
4. Compute centrality measures
5. Visualize network
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Error: Command not found. Make sure Python scripts are in the current directory.")
        return False

def check_file_exists(filename, description):
    """Check if a required file exists."""
    if os.path.exists(filename):
        print(f"✓ {description} found: {filename}")
        return True
    else:
        print(f"✗ {description} not found: {filename}")
        return False

def main():
    """Run the complete pipeline."""
    print("="*60)
    print("PROTEIN-PROTEIN INTERACTION NETWORK ANALYSIS PIPELINE")
    print("="*60)
    
    # Check for required input file
    string_file = None
    if len(sys.argv) > 1:
        string_file = sys.argv[1]
        if not os.path.exists(string_file):
            print(f"Error: Input file not found: {string_file}")
            return 1
    
    # Step 1: Download/Process STRING data
    if string_file:
        if not run_command(
            ['python', 'download_string_data.py', string_file],
            'Processing STRING data file'
        ):
            print("Failed at step 1. Exiting.")
            return 1
    else:
        print("\nSkipping data download step.")
        print("If you have a STRING file, run:")
        print("  python download_string_data.py <filename>")
        if not check_file_exists('string_homo_sapiens.csv', 'Processed STRING data'):
            print("Please download STRING data first.")
            return 1
    
    # Step 2: Clean data
    if not check_file_exists('string_homo_sapiens.csv', 'Input data file'):
        print("Error: string_homo_sapiens.csv not found.")
        return 1
    
    if not run_command(
        ['python', 'clean_data.py', 'string_homo_sapiens.csv', 'string_cleaned.csv'],
        'Cleaning and formatting data'
    ):
        print("Failed at step 2. Exiting.")
        return 1
    
    # Step 3: Build network graph
    if not check_file_exists('string_cleaned.csv', 'Cleaned data file'):
        print("Error: string_cleaned.csv not found.")
        return 1
    
    if not run_command(
        ['python', 'build_graph.py', 'string_cleaned.csv', 'string_network.graphml'],
        'Building network graph'
    ):
        print("Failed at step 3. Exiting.")
        return 1
    
    # Step 4: Compute centrality measures
    if not check_file_exists('string_network.graphml', 'Network graph file'):
        print("Error: string_network.graphml not found.")
        return 1
    
    if not run_command(
        ['python', 'compute_centrality.py', 'string_network.graphml', '50'],
        'Computing centrality measures and identifying hub genes'
    ):
        print("Failed at step 4. Exiting.")
        return 1
    
    # Step 5: Visualize network
    if not check_file_exists('hub_genes.csv', 'Hub genes file'):
        print("Error: hub_genes.csv not found.")
        return 1
    
    if not run_command(
        ['python', 'visualize_network.py', 'string_network.graphml', 'hub_genes.csv'],
        'Creating network visualizations'
    ):
        print("Failed at step 5. Exiting.")
        return 1
    
    # Summary
    print("\n" + "="*60)
    print("PIPELINE COMPLETE!")
    print("="*60)
    print("\nGenerated files:")
    output_files = [
        ('string_cleaned.csv', 'Cleaned interaction data'),
        ('string_network.graphml', 'Network graph'),
        ('centrality_results.csv', 'Centrality measures'),
        ('hub_genes.csv', 'Hub genes list'),
        ('network_full.png', 'Full network visualization'),
        ('network_hubs.png', 'Hub network visualization'),
        ('network_communities.png', 'Community visualization'),
        ('network_interactive.html', 'Interactive visualization'),
        ('summary_plots.png', 'Summary statistics plots'),
    ]
    
    for filename, description in output_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            size_mb = size / (1024 * 1024)
            print(f"  ✓ {filename} ({size_mb:.2f} MB) - {description}")
        else:
            print(f"  ✗ {filename} - {description} (not found)")
    
    print("\nNext steps:")
    print("  1. Review hub_genes.csv for top hub genes")
    print("  2. Open network_interactive.html in a web browser")
    print("  3. Check the PNG visualizations")
    print("  4. Review docs/PORTFOLIO.md for detailed results")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

