"""
Advanced and batch visualization options (Sprint 5).

Wraps ``visualize_network`` with presets (publication / slide figures) and a
convenient ``--batch`` mode that adds multi-format static exports and graph
data exports (GraphML, GEXF, node-link JSON).
"""

from __future__ import annotations

import sys
from typing import List

from visualize_network import __version__ as VIZ_VERSION
from visualize_network import main as visualize_main


PRESETS: dict[str, List[str]] = {
    "publication": [
        "--dpi",
        "600",
        "--formats",
        "png,svg,pdf",
        "--export-graph-data",
    ],
    "slides": ["--dpi", "200", "--formats", "png,pdf"],
    "web": ["--dpi", "150", "--formats", "png,svg"],
}


def main(argv: List[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--version" in args:
        print(f"visualize_network_advanced.py {VIZ_VERSION}")
        return 0
    if "-h" in args or "--help" in args:
        print(
            "Usage: python visualize_network_advanced.py [--preset NAME] [--batch] [--] [visualize_network args]\n"
            f"  Presets: {', '.join(sorted(PRESETS))}\n"
            "  --batch   Multi-format PNG/SVG/PDF static figures and graph data export.\n"
            "  Pass-through arguments are forwarded to visualize_network.py (place after -- if needed).\n"
        )
        return 0

    preset: str | None = None
    batch = False
    rest: List[str] = []
    i = 0
    while i < len(args):
        if args[i] == "--preset" and i + 1 < len(args):
            preset = args[i + 1]
            if preset not in PRESETS:
                print(f"Unknown preset: {preset}. Choose from: {', '.join(sorted(PRESETS))}", file=sys.stderr)
                return 2
            i += 2
            continue
        if args[i] == "--batch":
            batch = True
            i += 1
            continue
        rest.append(args[i])
        i += 1

    prefix: List[str] = []
    if preset:
        prefix.extend(PRESETS[preset])
    if batch:
        prefix.extend(["--formats", "png,svg,pdf", "--export-graph-data"])

    return visualize_main(prefix + rest)


if __name__ == "__main__":
    raise SystemExit(main())
