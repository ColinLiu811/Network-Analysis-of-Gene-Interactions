#!/usr/bin/env python3
"""
Gene Interaction Network Analysis Tool

A comprehensive tool for analyzing gene interaction networks using graph theory.
"""

import argparse
import sys
from pathlib import Path
from data_processor import DataProcessor
from network_analyzer import NetworkAnalyzer
from network_visualizer import NetworkVisualizer
from report_generator import ReportGenerator


def main():
    """Main entry point for the Gene Interaction Network Analysis Tool."""
    parser = argparse.ArgumentParser(
        description='Analyze gene interaction networks from CSV/TSV files'
    )
    parser.add_argument(
        'input_file',
        type=str,
        help='Path to input CSV/TSV file with gene interactions'
    )
    parser.add_argument(
        '-o', '--output-dir',
        type=str,
        default='output',
        help='Output directory for results (default: output)'
    )
    parser.add_argument(
        '-c', '--confidence-threshold',
        type=float,
        default=0.0,
        help='Minimum confidence score threshold (default: 0.0)'
    )
    parser.add_argument(
        '--top-hubs',
        type=int,
        default=10,
        help='Number of top hub genes to highlight (default: 10)'
    )
    parser.add_argument(
        '--visualize',
        action='store_true',
        help='Generate network visualization'
    )
    parser.add_argument(
        '--format',
        type=str,
        choices=['png', 'html', 'both'],
        default='png',
        help='Visualization format: png, html, or both (default: png)'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print("=" * 60)
    print("Gene Interaction Network Analysis Tool")
    print("=" * 60)
    print(f"\nInput file: {args.input_file}")
    print(f"Output directory: {output_dir}")
    print(f"Confidence threshold: {args.confidence_threshold}")
    print()
    
    try:
        # Step 1: Load and preprocess data
        print("Step 1: Loading and preprocessing data...")
        processor = DataProcessor(args.input_file, args.confidence_threshold)
        df_cleaned = processor.process()
        
        if len(df_cleaned) == 0:
            raise ValueError(
                "No valid interactions found after preprocessing. "
                "Please check your input file and confidence threshold."
            )
        
        cleaned_file = output_dir / 'cleaned_interactions.csv'
        df_cleaned.to_csv(cleaned_file, index=False)
        print(f"  ✓ Cleaned data saved to: {cleaned_file}")
        print(f"  ✓ Total interactions: {len(df_cleaned)}")
        print()
        
        # Step 2: Build network graph
        print("Step 2: Constructing network graph...")
        analyzer = NetworkAnalyzer(df_cleaned)
        graph = analyzer.build_graph()
        print(f"  ✓ Network constructed: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
        print()
        
        # Step 3: Compute network metrics
        print("Step 3: Computing network metrics...")
        metrics_df = analyzer.compute_metrics()
        metrics_file = output_dir / 'network_metrics.csv'
        metrics_df.to_csv(metrics_file, index=False)
        print(f"  ✓ Metrics saved to: {metrics_file}")
        print()
        
        # Step 4: Identify hub genes
        print("Step 4: Identifying hub genes...")
        hub_genes = analyzer.get_hub_genes(args.top_hubs)
        print(f"  ✓ Top {args.top_hubs} hub genes identified")
        print()
        
        # Step 5: Generate visualization
        if args.visualize:
            print("Step 5: Generating visualizations...")
            visualizer = NetworkVisualizer(graph, metrics_df)
            
            if args.format in ['png', 'both']:
                png_file = output_dir / 'network_visualization.png'
                visualizer.visualize_png(png_file, hub_genes)
                print(f"  ✓ PNG visualization saved to: {png_file}")
            
            if args.format in ['html', 'both']:
                html_file = output_dir / 'network_visualization.html'
                visualizer.visualize_html(html_file, hub_genes)
                print(f"  ✓ Interactive HTML visualization saved to: {html_file}")
            print()
        
        # Step 6: Generate report
        print("Step 6: Generating summary report...")
        reporter = ReportGenerator(analyzer, hub_genes, output_dir)
        report_file = reporter.generate_report()
        print(f"  ✓ Report saved to: {report_file}")
        print()
        
        # Display summary
        print("=" * 60)
        print("Analysis Complete!")
        print("=" * 60)
        print(f"\nResults saved in: {output_dir}")
        print(f"\nTop {min(5, len(hub_genes))} Hub Genes:")
        for i, (gene, data) in enumerate(hub_genes.head(5).iterrows(), 1):
            print(f"  {i}. {gene} (Degree: {data['degree_centrality']:.4f})")
        print()
        
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

