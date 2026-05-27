"""
Compare two network files with quick overlap statistics.
"""

from __future__ import annotations

import argparse
import networkx as nx


def load_graph(path: str) -> nx.Graph:
    if path.endswith(".graphml"):
        return nx.read_graphml(path)
    if path.endswith(".gexf"):
        return nx.read_gexf(path)
    raise ValueError(f"Unsupported format: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two graph files.")
    parser.add_argument("graph_a")
    parser.add_argument("graph_b")
    args = parser.parse_args()

    ga = load_graph(args.graph_a)
    gb = load_graph(args.graph_b)

    na = set(map(str, ga.nodes()))
    nb = set(map(str, gb.nodes()))
    overlap = na & nb
    union = na | nb
    jaccard = len(overlap) / len(union) if union else 0.0

    print("Graph A:", ga.number_of_nodes(), "nodes,", ga.number_of_edges(), "edges")
    print("Graph B:", gb.number_of_nodes(), "nodes,", gb.number_of_edges(), "edges")
    print("Node overlap:", len(overlap))
    print("Node Jaccard:", f"{jaccard:.4f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
