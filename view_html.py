#!/usr/bin/env python3
"""
Helper script to serve HTML visualization files in GitHub Codespaces or locally.
"""

import http.server
import socketserver
import sys
from pathlib import Path
import webbrowser

PORT = 8000

def main():
    """Start a simple HTTP server to view HTML files."""
    output_dir = Path('output')
    
    if not output_dir.exists():
        print("Error: 'output' directory not found.")
        print("Please run the analysis first to generate output files.")
        sys.exit(1)
    
    html_file = output_dir / 'network_visualization.html'
    if not html_file.exists():
        print(f"Warning: {html_file} not found.")
        print("The server will still start, but the visualization file may not exist.")
    
    # Change to output directory
    import os
    os.chdir(output_dir)
    
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("=" * 60)
            print("HTML Visualization Server")
            print("=" * 60)
            print(f"\nServing files from: {output_dir.absolute()}")
            print(f"Server running on port {PORT}")
            print(f"\nTo view the visualization:")
            print(f"  1. In GitHub Codespaces: Check the 'Ports' tab")
            print(f"  2. Click on port {PORT} and select 'Open in Browser'")
            print(f"  3. Navigate to: /network_visualization.html")
            print(f"\nOr access directly at:")
            print(f"  http://localhost:{PORT}/network_visualization.html")
            print("\nPress Ctrl+C to stop the server")
            print("=" * 60)
            
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"Error: Port {PORT} is already in use.")
            print(f"Try a different port or stop the process using port {PORT}.")
        else:
            print(f"Error starting server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        sys.exit(0)

if __name__ == '__main__':
    main()

