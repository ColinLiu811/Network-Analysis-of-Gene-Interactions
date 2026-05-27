"""
Automated pipeline to run the complete protein-protein interaction network analysis.

This script runs all steps of the analysis pipeline:
1. Download/process STRING data
2. Clean data
3. Build network graph
4. Compute centrality measures
5. Visualize network
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

PIPELINE_VERSION = "1.1.0"


def _use_color() -> bool:
    return sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def _c(text: str, code: str) -> str:
    if not _use_color():
        return text
    return f"\033[{code}m{text}\033[0m"


def run_command(cmd, description):
    """Run a command and handle errors."""
    title = _c(f"STEP: {description}", "1;36")
    print(f"\n{'='*60}")
    print(title)
    print(f"{'='*60}")
    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(_c(f"Error: {e}", "31"))
        print(f"Output: {e.stdout}")
        print(f"Error output: {e.stderr}")
        return False
    except FileNotFoundError:
        print(_c("Error: Command not found. Ensure Python scripts are in the current directory.", "31"))
        return False


def check_file_exists(filename, description):
    """Check if a required file exists."""
    if os.path.exists(filename):
        print(_c(f"[OK] {description} found: {filename}", "32"))
        return True
    print(_c(f"[MISSING] {description} not found: {filename}", "33"))
    return False


def main() -> int:
    """Run the complete pipeline."""
    parser = argparse.ArgumentParser(
        description="Run the full PPI network analysis pipeline.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {PIPELINE_VERSION}")
    parser.add_argument(
        "string_file",
        nargs="?",
        default=None,
        help="Optional STRING protein.links file to process in step 1",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="YAML config (e.g. copy config.default.yaml to config.yaml). Used for top_n_hubs.",
    )
    parser.add_argument(
        "--viz-formats",
        default=None,
        help="Comma-separated extra static figure formats for visualize_network (e.g. svg,pdf)",
    )
    args = parser.parse_args()

    py = sys.executable

    top_n = 50
    if args.config:
        try:
            from pipeline_config import load_config

            cfg = load_config(args.config)
            top_n = int(cfg.get("pipeline", {}).get("top_n_hubs", 50))
        except (OSError, ImportError, ValueError, TypeError):
            pass

    print("=" * 60)
    print(_c("PROTEIN-PROTEIN INTERACTION NETWORK ANALYSIS PIPELINE", "1;36"))
    print("=" * 60)

    string_file = args.string_file
    if string_file and not os.path.exists(string_file):
        print(_c(f"Error: Input file not found: {string_file}", "31"))
        return 1

    # Step 1: Download/Process STRING data
    if string_file:
        if not run_command(
            [py, "download_string_data.py", string_file],
            "Processing STRING data file",
        ):
            print("Failed at step 1. Exiting.")
            return 1
    else:
        print("\nSkipping data download step.")
        print("If you have a STRING file, run:")
        print(f"  {py} download_string_data.py <filename>")
        if not check_file_exists("string_homo_sapiens.csv", "Processed STRING data"):
            print("Please download STRING data first.")
            return 1

    # Step 2: Clean data
    if not check_file_exists("string_homo_sapiens.csv", "Input data file"):
        print("Error: string_homo_sapiens.csv not found.")
        return 1

    if not run_command(
        [py, "clean_data.py", "string_homo_sapiens.csv", "string_cleaned.csv"],
        "Cleaning and formatting data",
    ):
        print("Failed at step 2. Exiting.")
        return 1

    # Step 3: Build network graph
    if not check_file_exists("string_cleaned.csv", "Cleaned data file"):
        print("Error: string_cleaned.csv not found.")
        return 1

    if not run_command(
        [py, "build_graph.py", "string_cleaned.csv", "string_network.graphml"],
        "Building network graph",
    ):
        print("Failed at step 3. Exiting.")
        return 1

    # Step 4: Compute centrality measures
    if not check_file_exists("string_network.graphml", "Network graph file"):
        print("Error: string_network.graphml not found.")
        return 1

    if not run_command(
        [py, "compute_centrality.py", "string_network.graphml", str(top_n)],
        "Computing centrality measures and identifying hub genes",
    ):
        print("Failed at step 4. Exiting.")
        return 1

    # Step 5: Visualize network
    if not check_file_exists("hub_genes.csv", "Hub genes file"):
        print("Error: hub_genes.csv not found.")
        return 1

    viz_cmd = [py, "visualize_network.py", "string_network.graphml", "hub_genes.csv"]
    if args.viz_formats:
        viz_cmd.extend(["--formats", args.viz_formats])
    if args.config:
        viz_cmd.extend(["--config", args.config])

    if not run_command(viz_cmd, "Creating network visualizations"):
        print("Failed at step 5. Exiting.")
        return 1

    # Summary
    print("\n" + "=" * 60)
    print(_c("PIPELINE COMPLETE!", "1;32"))
    print("=" * 60)
    print("\nGenerated files:")
    output_files = [
        ("string_cleaned.csv", "Cleaned interaction data"),
        ("string_network.graphml", "Network graph"),
        ("centrality_results.csv", "Centrality measures"),
        ("hub_genes.csv", "Hub genes list"),
        ("network_full.png", "Full network visualization"),
        ("network_hubs.png", "Hub network visualization"),
        ("network_communities.png", "Community visualization"),
        ("network_interactive.html", "Interactive visualization"),
        ("summary_plots.png", "Summary statistics plots"),
    ]

    for filename, description in output_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            size_mb = size / (1024 * 1024)
            print(f"  [OK] {filename} ({size_mb:.2f} MB) - {description}")
        else:
            print(f"  [MISSING] {filename} - {description} (not found)")

    print("\nNext steps:")
    print("  1. Review hub_genes.csv for top hub genes")
    print("  2. Open network_interactive.html in a web browser")
    print("  3. Check the PNG visualizations")
    print("  4. See docs/visualization_guide.md for CLI and export options")

    return 0


if __name__ == "__main__":
    sys.exit(main())
