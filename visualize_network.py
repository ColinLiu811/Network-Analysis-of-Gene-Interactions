"""
Create visualizations of the protein-protein interaction network.

This script generates various visualizations including:
- Full network overview
- Hub gene visualization
- Network clusters and communities
- Interactive visualizations (vis.js or pyvis)
"""

from __future__ import annotations

import argparse
import json
import os
import warnings
from typing import Any, Dict, List, Optional, Sequence, Set

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

__version__ = "1.1.0"


def load_graph(input_file: str = "string_network.graphml"):
    """Load graph from file."""
    print(f"Loading graph from {input_file}...")

    if input_file.endswith(".graphml"):
        g = nx.read_graphml(input_file)
    elif input_file.endswith(".gexf"):
        g = nx.read_gexf(input_file)
    else:
        raise ValueError(f"Unsupported file format: {input_file}")

    print(f"Loaded graph with {g.number_of_nodes()} nodes and {g.number_of_edges()} edges")
    return g


def load_hub_genes(hub_file: str = "hub_genes.csv", top_n: int = 50) -> Tuple[Set[str], pd.DataFrame]:
    """Load hub genes data."""
    print(f"Loading hub genes from {hub_file}...")
    df = pd.read_csv(hub_file)
    top_hubs = set(df.head(top_n)["protein_id"].tolist())
    print(f"Loaded {len(top_hubs)} hub genes")
    return top_hubs, df


def load_centrality_table(path: str) -> Optional[pd.DataFrame]:
    """Load centrality_results.csv if present."""
    if not path or not os.path.isfile(path):
        return None
    try:
        return pd.read_csv(path)
    except OSError:
        return None


def read_highlight_genes(path: Optional[str]) -> Set[str]:
    """Load gene/protein IDs from a text file (one ID per line or comma-separated)."""
    if not path or not os.path.isfile(path):
        return set()
    ids: Set[str] = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "," in line:
                for part in line.split(","):
                    p = part.strip()
                    if p:
                        ids.add(p)
            else:
                ids.add(line)
    print(f"Loaded {len(ids)} highlight gene IDs from {path}")
    return ids


def detect_communities(g: nx.Graph) -> Dict[Any, int]:
    """
    Detect communities/clusters in the network using Louvain algorithm.
    """
    print("\nDetecting communities using Louvain algorithm...")

    try:
        import community.community_louvain as community_louvain

        communities = community_louvain.best_partition(g)
        num_communities = len(set(communities.values()))
        print(f"Detected {num_communities} communities")
        return communities
    except ImportError:
        print("python-louvain not installed. Using greedy modularity communities instead...")
        from networkx.algorithms import community as nx_comm

        communities_generator = nx_comm.greedy_modularity_communities(g)
        communities = {}
        for i, comm in enumerate(communities_generator):
            for node in comm:
                communities[node] = i
        num_communities = len(set(communities.values()))
        print(f"Detected {num_communities} communities")
        return communities


def _save_figure_extra_formats(dpi: int, output_file: str, extra_formats: Sequence[str]) -> None:
    """Save current matplotlib figure to additional formats (same basename)."""
    base, _ = os.path.splitext(output_file)
    for fmt in extra_formats:
        fmt_clean = fmt.lower().lstrip(".")
        if fmt_clean not in ("svg", "pdf", "png"):
            continue
        alt = f"{base}.{fmt_clean}"
        if os.path.abspath(alt) == os.path.abspath(output_file):
            continue
        plt.savefig(alt, dpi=dpi, bbox_inches="tight")
        print(f"Saved also: {alt}")


def visualize_full_network(
    g: nx.Graph,
    hub_genes: Optional[Set[str]] = None,
    communities: Optional[Dict[Any, int]] = None,
    output_file: str = "network_full.png",
    max_nodes: int = 5000,
    layout: str = "spring",
    dpi: int = 300,
    extra_formats: Optional[Sequence[str]] = None,
    highlight_extra: Optional[Set[str]] = None,
    color_scheme: str = "hub",
):
    """
    Visualize the full network with hub genes highlighted.

    color_scheme: 'hub' (red/blue), 'community' (requires communities dict)
    highlight_extra: additional nodes to highlight (e.g. from file) in orange
    """
    print("\nCreating full network visualization...")
    extra_formats = extra_formats or ()
    highlight_extra = highlight_extra or set()

    if g.number_of_nodes() > max_nodes:
        print(f"Graph has {g.number_of_nodes()} nodes. Using largest connected component...")
        largest_cc = max(nx.connected_components(g), key=len)
        g_viz = g.subgraph(largest_cc).copy()
        if g_viz.number_of_nodes() > max_nodes:
            nodes_sample = list(g_viz.nodes())[:max_nodes]
            g_viz = g.subgraph(nodes_sample).copy()
    else:
        g_viz = g.copy()

    print(f"Visualizing {g_viz.number_of_nodes()} nodes and {g_viz.number_of_edges()} edges")

    if layout == "spring":
        pos = nx.spring_layout(g_viz, k=1, iterations=50, seed=42)
    elif layout == "circular":
        pos = nx.circular_layout(g_viz)
    elif layout == "kamada_kawai":
        pos = nx.kamada_kawai_layout(g_viz)
    elif layout == "spectral":
        pos = nx.spectral_layout(g_viz)
    else:
        pos = nx.spring_layout(g_viz, k=1, iterations=50, seed=42)

    plt.figure(figsize=(20, 20))
    nx.draw_networkx_edges(g_viz, pos, alpha=0.1, width=0.5, edge_color="gray")

    cmap = plt.colormaps["tab20"]
    if color_scheme == "community" and communities:
        node_colors = [cmap(communities.get(node, 0) % 20) for node in g_viz.nodes()]
        node_sizes = [50 for _ in g_viz.nodes()]
    elif hub_genes:
        node_colors = []
        node_sizes = []
        for node in g_viz.nodes():
            if node in hub_genes:
                node_colors.append("red")
                node_sizes.append(300)
            elif node in highlight_extra:
                node_colors.append("orange")
                node_sizes.append(260)
            else:
                node_colors.append("lightblue")
                node_sizes.append(50)
    else:
        node_colors = "lightblue"
        node_sizes = 50

    nx.draw_networkx_nodes(
        g_viz, pos, node_color=node_colors, node_size=node_sizes, alpha=0.7
    )

    if hub_genes:
        patches = [
            mpatches.Patch(color="red", label="Hub Genes"),
            mpatches.Patch(color="lightblue", label="Other Genes"),
        ]
        if highlight_extra:
            patches.append(mpatches.Patch(color="orange", label="Highlighted set"))
        plt.legend(handles=patches, loc="upper right")

    plt.title(
        f"Protein-Protein Interaction Network\n{g_viz.number_of_nodes()} nodes, "
        f"{g_viz.number_of_edges()} edges",
        fontsize=16,
        fontweight="bold",
    )
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_file, dpi=dpi, bbox_inches="tight")
    _save_figure_extra_formats(dpi, output_file, extra_formats)
    print(f"Saved visualization to {output_file}")
    plt.close()


def visualize_hub_network(
    g: nx.Graph,
    hub_genes: Set[str],
    output_file: str = "network_hubs.png",
    dpi: int = 300,
    extra_formats: Optional[Sequence[str]] = None,
):
    """Visualize hub genes and their immediate neighbors."""
    print("\nCreating hub gene network visualization...")
    extra_formats = extra_formats or ()

    hub_subgraph_nodes = set(hub_genes)
    for hub in hub_genes:
        if hub in g:
            hub_subgraph_nodes.update(g.neighbors(hub))

    g_hubs = g.subgraph(hub_subgraph_nodes).copy()
    print(f"Hub subgraph: {g_hubs.number_of_nodes()} nodes, {g_hubs.number_of_edges()} edges")

    pos = nx.spring_layout(g_hubs, k=1, iterations=50, seed=42)

    plt.figure(figsize=(16, 16))
    nx.draw_networkx_edges(g_hubs, pos, alpha=0.2, width=0.5, edge_color="gray")

    node_colors = ["red" if node in hub_genes else "lightblue" for node in g_hubs.nodes()]
    node_sizes = [500 if node in hub_genes else 100 for node in g_hubs.nodes()]

    nx.draw_networkx_nodes(
        g_hubs, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8
    )

    hub_labels = {
        node: node[:15] + "..." if len(node) > 15 else node
        for node in hub_genes
        if node in g_hubs
    }
    nx.draw_networkx_labels(g_hubs, pos, hub_labels, font_size=8, font_weight="bold")

    red_patch = mpatches.Patch(color="red", label="Hub Genes")
    blue_patch = mpatches.Patch(color="lightblue", label="Neighbors")
    plt.legend(handles=[red_patch, blue_patch], loc="upper right")

    plt.title("Hub Gene Network", fontsize=16, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_file, dpi=dpi, bbox_inches="tight")
    _save_figure_extra_formats(dpi, output_file, extra_formats)
    print(f"Saved visualization to {output_file}")
    plt.close()


def visualize_communities(
    g: nx.Graph,
    communities: Dict[Any, int],
    output_file: str = "network_communities.png",
    max_nodes: int = 5000,
    dpi: int = 300,
    extra_formats: Optional[Sequence[str]] = None,
):
    """Visualize network with community structure."""
    print("\nCreating community visualization...")
    extra_formats = extra_formats or ()

    if g.number_of_nodes() > max_nodes:
        largest_cc = max(nx.connected_components(g), key=len)
        g_viz = g.subgraph(largest_cc).copy()
        if g_viz.number_of_nodes() > max_nodes:
            nodes_sample = list(g_viz.nodes())[:max_nodes]
            g_viz = g.subgraph(nodes_sample).copy()
    else:
        g_viz = g.copy()

    pos = nx.spring_layout(g_viz, k=1, iterations=50, seed=42)
    unique_communities = list(set(communities.values()))
    num_communities = len(unique_communities)

    plt.figure(figsize=(20, 20))
    nx.draw_networkx_edges(g_viz, pos, alpha=0.1, width=0.3, edge_color="gray")

    cmap = plt.colormaps["tab20"]
    node_colors = [cmap(communities.get(node, 0) % 20) for node in g_viz.nodes()]

    nx.draw_networkx_nodes(g_viz, pos, node_color=node_colors, node_size=30, alpha=0.7)

    plt.title(
        f"Network Communities\n{num_communities} communities detected",
        fontsize=16,
        fontweight="bold",
    )
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_file, dpi=dpi, bbox_inches="tight")
    _save_figure_extra_formats(dpi, output_file, extra_formats)
    print(f"Saved visualization to {output_file}")
    plt.close()


def create_summary_plots(hub_genes_df: pd.DataFrame, output_file: str = "summary_plots.png"):
    """Create summary statistics plots."""
    print("\nCreating summary plots...")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    ax1 = axes[0, 0]
    degrees = hub_genes_df["degree"].values
    ax1.hist(degrees, bins=50, edgecolor="black", alpha=0.7)
    ax1.set_xlabel("Degree", fontsize=12)
    ax1.set_ylabel("Frequency", fontsize=12)
    ax1.set_title("Degree Distribution", fontsize=14, fontweight="bold")
    ax1.set_yscale("log")

    ax2 = axes[0, 1]
    hub_scores = hub_genes_df["hub_score"].values
    ax2.hist(hub_scores, bins=50, edgecolor="black", alpha=0.7, color="green")
    ax2.set_xlabel("Hub Score", fontsize=12)
    ax2.set_ylabel("Frequency", fontsize=12)
    ax2.set_title("Hub Score Distribution", fontsize=14, fontweight="bold")

    ax3 = axes[1, 0]
    top_20 = hub_genes_df.head(20)
    ax3.barh(range(len(top_20)), top_20["hub_score"].values)
    ax3.set_yticks(range(len(top_20)))
    ax3.set_yticklabels(
        [pid[:20] + "..." if len(pid) > 20 else pid for pid in top_20["protein_id"]],
        fontsize=8,
    )
    ax3.set_xlabel("Hub Score", fontsize=12)
    ax3.set_title("Top 20 Hub Genes", fontsize=14, fontweight="bold")
    ax3.invert_yaxis()

    ax4 = axes[1, 1]
    centrality_cols = [
        "degree_centrality",
        "betweenness_centrality",
        "eigenvector_centrality",
        "pagerank",
    ]
    available_cols = [col for col in centrality_cols if col in hub_genes_df.columns]
    if len(available_cols) > 1:
        corr_matrix = hub_genes_df[available_cols].corr()
        im = ax4.imshow(corr_matrix, cmap="coolwarm", aspect="auto", vmin=-1, vmax=1)
        ax4.set_xticks(range(len(available_cols)))
        ax4.set_yticks(range(len(available_cols)))
        ax4.set_xticklabels(available_cols, rotation=45, ha="right", fontsize=8)
        ax4.set_yticklabels(available_cols, fontsize=8)
        ax4.set_title("Centrality Measures Correlation", fontsize=14, fontweight="bold")
        plt.colorbar(im, ax=ax4)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Saved summary plots to {output_file}")
    plt.close()


def create_interactive_visualization_visjs(
    g: nx.Graph,
    hub_genes: Optional[Set[str]] = None,
    centrality_df: Optional[pd.DataFrame] = None,
    output_file: str = "network_interactive.html",
    max_nodes: int = 1000,
):
    """
    Interactive HTML using vis.js: search, min-degree and min-betweenness filters,
    zoom/pan (built-in), tooltips with centrality info.
    """
    print("\nCreating interactive visualization (vis.js)...")
    hub_genes = hub_genes or set()

    if g.number_of_nodes() > max_nodes:
        print(f"Graph large ({g.number_of_nodes()} nodes). Sampling {max_nodes} nodes...")
        nodes_sample = list(g.nodes())[:max_nodes]
        g_viz = g.subgraph(nodes_sample).copy()
    else:
        g_viz = g.copy()

    cent_index: Dict[str, Dict[str, float]] = {}
    if centrality_df is not None and "protein_id" in centrality_df.columns:
        for _, row in centrality_df.iterrows():
            pid = str(row["protein_id"])
            cent_index[pid] = {
                "degree_centrality": float(row.get("degree_centrality", 0) or 0),
                "betweenness_centrality": float(row.get("betweenness_centrality", 0) or 0),
                "closeness_centrality": float(row.get("closeness_centrality", 0) or 0),
                "hub_score": float(row.get("hub_score", 0) or 0),
            }

    vis_nodes: List[Dict[str, Any]] = []
    for n in g_viz.nodes():
        sid = str(n)
        deg = int(g_viz.degree(n))
        bc = cent_index.get(sid, {}).get("betweenness_centrality", 0.0)
        hs = cent_index.get(sid, {}).get("hub_score", 0.0)
        dc = cent_index.get(sid, {}).get("degree_centrality", 0.0)
        is_hub = sid in hub_genes
        title_lines = [
            f"ID: {sid}",
            f"Degree: {deg}",
            f"Degree centrality: {dc:.4f}",
            f"Betweenness: {bc:.6f}",
            f"Hub score: {hs:.4f}",
        ]
        if is_hub:
            title_lines.insert(1, "(Hub gene)")
        color = "#ff5555" if is_hub else "#66b3ff"
        vis_nodes.append(
            {
                "id": sid,
                "label": sid if len(sid) <= 28 else sid[:25] + "...",
                "title": "\n".join(title_lines),
                "value": max(8, min(36, deg // 2 + 8)),
                "deg": deg,
                "bc": bc,
                "color": color,
            }
        )

    vis_edges = [{"from": str(u), "to": str(v)} for u, v in g_viz.edges()]

    nodes_json = json.dumps(vis_nodes)
    edges_json = json.dumps(vis_edges)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Network (interactive)</title>
  <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 0; background: #1a1a1a; color: #eee; }}
    #toolbar {{
      padding: 10px 14px; background: #2a2a2a; border-bottom: 1px solid #444;
      display: flex; flex-wrap: wrap; gap: 12px; align-items: center;
    }}
    #toolbar label {{ margin-right: 6px; font-size: 13px; }}
    #toolbar input[type="text"] {{ width: 220px; padding: 6px 8px; }}
    #toolbar input[type="range"] {{ width: 140px; vertical-align: middle; }}
    #network {{ width: 100%; height: calc(100vh - 56px); background: #222; }}
    .hint {{ font-size: 12px; color: #aaa; }}
  </style>
</head>
<body>
  <div id="toolbar">
    <div>
      <label for="search">Search gene ID</label>
      <input type="text" id="search" placeholder="Substring match (case-insensitive)">
    </div>
    <div>
      <label for="mindeg">Min degree: <span id="mindegv">0</span></label>
      <input type="range" id="mindeg" min="0" max="500" value="0">
    </div>
    <div>
      <label for="minbc">Min betweenness: <span id="minbcv">0</span></label>
      <input type="range" id="minbc" min="0" max="1000" value="0">
    </div>
    <span class="hint">Scroll to zoom; drag background to pan; drag nodes to rearrange.</span>
  </div>
  <div id="network"></div>
  <script>
    var rawNodes = {nodes_json};
    var rawEdges = {edges_json};
    var maxBc = 0.001;
    rawNodes.forEach(function(n) {{
      if (n.bc > maxBc) maxBc = n.bc;
    }});
    if (maxBc <= 0) maxBc = 1;
    var minbcSlider = document.getElementById('minbc');
    minbcSlider.max = 1000;

    var nodes = new vis.DataSet(rawNodes);
    var edges = new vis.DataSet(rawEdges);
    var container = document.getElementById('network');
    var data = {{ nodes: nodes, edges: edges }};
    var options = {{
      nodes: {{
        shape: 'dot',
        font: {{ size: 12, color: '#ffffff' }},
        borderWidth: 1,
        scaling: {{ min: 6, max: 40 }}
      }},
      edges: {{ color: {{ inherit: 'from' }}, smooth: {{ type: 'continuous' }} }},
      physics: {{
        barnesHut: {{ gravitationalConstant: -12000, springLength: 120 }},
        stabilization: {{ iterations: 80 }}
      }},
      interaction: {{ hover: true, navigationButtons: true, keyboard: true, tooltipDelay: 80 }}
    }};
    var network = new vis.Network(container, data, options);

    function applyFilters() {{
      var q = (document.getElementById('search').value || '').toLowerCase().trim();
      var minDeg = parseInt(document.getElementById('mindeg').value, 10) || 0;
      var bcFrac = parseInt(document.getElementById('minbc').value, 10) / 1000;
      var minBc = bcFrac * maxBc;
      document.getElementById('mindegv').textContent = minDeg;
      document.getElementById('minbcv').textContent = minBc.toExponential(2);

      var updates = [];
      rawNodes.forEach(function(n) {{
        var match = !q || (String(n.id).toLowerCase().indexOf(q) !== -1);
        var degOk = n.deg >= minDeg;
        var bcOk = n.bc >= minBc;
        updates.push({{ id: n.id, hidden: !(match && degOk && bcOk) }});
      }});
      nodes.update(updates);
    }}

    document.getElementById('search').addEventListener('input', applyFilters);
    document.getElementById('mindeg').addEventListener('input', applyFilters);
    document.getElementById('minbc').addEventListener('input', applyFilters);
  </script>
</body>
</html>
"""

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Saved interactive visualization to {output_file}")


def create_interactive_visualization_pyvis(
    g: nx.Graph,
    hub_genes: Optional[Set[str]] = None,
    output_file: str = "network_interactive_pyvis.html",
    max_nodes: int = 1000,
):
    """Create interactive HTML using Pyvis (optional fallback)."""
    print("\nCreating interactive visualization (pyvis)...")
    try:
        from pyvis.network import Network
    except ImportError:
        print("Pyvis not installed. Skipping pyvis interactive output.")
        return

    hub_genes = hub_genes or set()
    if g.number_of_nodes() > max_nodes:
        print(f"Graph too large ({g.number_of_nodes()} nodes). Sampling {max_nodes} nodes...")
        nodes_sample = list(g.nodes())[:max_nodes]
        g_viz = g.subgraph(nodes_sample).copy()
    else:
        g_viz = g.copy()

    net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white")
    net.from_nx(g_viz)

    for node in net.nodes:
        if node["id"] in hub_genes:
            node["color"] = "#ff0000"
            node["size"] = 30
            node["title"] = f"Hub Gene: {node['id']}"
        else:
            node["size"] = 10

    net.show(output_file)
    print(f"Saved pyvis interactive visualization to {output_file}")


def export_graph_data_files(
    g: nx.Graph,
    stem: str = "network_export",
    formats: Optional[Sequence[str]] = None,
) -> None:
    """Export the graph as GraphML, GEXF, and node-link JSON."""
    formats = formats or ("graphml", "gexf", "json")
    from networkx.readwrite import json_graph

    if "graphml" in formats:
        path = f"{stem}.graphml"
        nx.write_graphml(g, path)
        print(f"Exported {path}")
    if "gexf" in formats:
        path = f"{stem}.gexf"
        nx.write_gexf(g, path)
        print(f"Exported {path}")
    if "json" in formats:
        path = f"{stem}_nodelink.json"
        data = json_graph.node_link_data(g)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Exported {path}")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Create PPI network static and interactive visualizations.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    p.add_argument("graph_file", nargs="?", default="string_network.graphml", help="GraphML or GEXF file")
    p.add_argument("hub_file", nargs="?", default="hub_genes.csv", help="Hub genes CSV")
    p.add_argument("--config", default=None, help="YAML config (merged with defaults)")
    p.add_argument("--layout", choices=("spring", "circular", "kamada_kawai", "spectral"), default="spring")
    p.add_argument("--color-scheme", choices=("hub", "community"), default="hub")
    p.add_argument("--dpi", type=int, default=300, help="Raster resolution (PNG)")
    p.add_argument(
        "--formats",
        default="png",
        help="Comma-separated extra static figure formats: png,svg,pdf",
    )
    p.add_argument("--max-nodes", type=int, default=5000, help="Cap nodes for full/community static plots")
    p.add_argument("--interactive-max-nodes", type=int, default=1000, help="Sample size for interactive HTML")
    p.add_argument("--centrality-csv", default="centrality_results.csv", help="For tooltips / filters")
    p.add_argument("--highlight-genes", default=None, help="File with gene IDs to highlight")
    p.add_argument(
        "--interactive-backend",
        choices=("visjs", "pyvis", "both"),
        default="visjs",
    )
    p.add_argument("--skip-interactive", action="store_true")
    p.add_argument("--export-graph-data", action="store_true", help="Write GraphML, GEXF, JSON exports")
    p.add_argument("--no-summary", action="store_true", help="Skip summary_plots.png")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_arg_parser().parse_args(list(argv) if argv is not None else None)

    dpi = args.dpi
    layout = args.layout
    color_scheme = args.color_scheme
    if args.config:
        try:
            from pipeline_config import load_config

            cfg = load_config(args.config)
            v = cfg.get("visualization", {})
            if "dpi" in v:
                dpi = int(v["dpi"])
            if v.get("layout"):
                layout = v["layout"]
            if v.get("color_scheme"):
                color_scheme = v["color_scheme"]
        except (OSError, ImportError):
            pass

    extra_formats = [x.strip().lower() for x in args.formats.split(",") if x.strip()]
    seen = set()
    extra_formats = [x for x in extra_formats if not (x in seen or seen.add(x))]

    g = load_graph(args.graph_file)
    hub_genes, hub_genes_df = load_hub_genes(args.hub_file)
    highlight = read_highlight_genes(args.highlight_genes)
    centrality_df = load_centrality_table(args.centrality_csv)

    communities = detect_communities(g)

    visualize_full_network(
        g,
        hub_genes=hub_genes,
        communities=communities,
        output_file="network_full.png",
        max_nodes=args.max_nodes,
        layout=layout,
        dpi=dpi,
        extra_formats=extra_formats,
        highlight_extra=highlight,
        color_scheme=color_scheme,
    )

    visualize_hub_network(g, hub_genes, output_file="network_hubs.png", dpi=dpi, extra_formats=extra_formats)
    visualize_communities(
        g,
        communities,
        output_file="network_communities.png",
        max_nodes=args.max_nodes,
        dpi=dpi,
        extra_formats=extra_formats,
    )

    if not args.no_summary:
        create_summary_plots(hub_genes_df, output_file="summary_plots.png")

    if not args.skip_interactive:
        if args.interactive_backend in ("visjs", "both"):
            create_interactive_visualization_visjs(
                g,
                hub_genes=hub_genes,
                centrality_df=centrality_df,
                output_file="network_interactive.html",
                max_nodes=args.interactive_max_nodes,
            )
        if args.interactive_backend in ("pyvis", "both"):
            create_interactive_visualization_pyvis(
                g,
                hub_genes=hub_genes,
                output_file="network_interactive_pyvis.html",
                max_nodes=args.interactive_max_nodes,
            )

    if args.export_graph_data:
        export_graph_data_files(g, stem="network_export", formats=("graphml", "gexf", "json"))

    print("\nAll visualizations created successfully!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
