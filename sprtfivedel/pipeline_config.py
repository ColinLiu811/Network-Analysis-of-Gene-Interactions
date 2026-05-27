"""
Load and merge pipeline / visualization configuration from YAML.

Falls back to built-in defaults when no file is provided or PyYAML is missing.
"""

from __future__ import annotations

import copy
import os
from typing import Any, Dict, Optional

DEFAULT_CONFIG: Dict[str, Any] = {
    "pipeline": {
        "top_n_hubs": 50,
        "confidence_threshold": 400,
    },
    "visualization": {
        "dpi": 300,
        "layout": "spring",
        "color_scheme": "hub",
        "static_max_nodes": 5000,
        "interactive_max_nodes": 1000,
        "export_formats": ["png"],
        "interactive_backend": "visjs",
    },
}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    out = copy.deepcopy(base)
    for key, val in override.items():
        if key in out and isinstance(out[key], dict) and isinstance(val, dict):
            out[key] = _deep_merge(out[key], val)
        else:
            out[key] = copy.deepcopy(val)
    return out


def load_config(path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from YAML path, or return defaults.

    If path is None, looks for ``config.yaml`` in the current working directory
    when present; otherwise returns defaults.
    """
    cfg_path = path
    if cfg_path is None:
        candidate = os.path.join(os.getcwd(), "config.yaml")
        if os.path.isfile(candidate):
            cfg_path = candidate
        else:
            return copy.deepcopy(DEFAULT_CONFIG)

    if not os.path.isfile(cfg_path):
        return copy.deepcopy(DEFAULT_CONFIG)

    try:
        import yaml  # type: ignore
    except ImportError:
        return copy.deepcopy(DEFAULT_CONFIG)

    with open(cfg_path, "r", encoding="utf-8") as f:
        loaded = yaml.safe_load(f) or {}
    return _deep_merge(DEFAULT_CONFIG, loaded)
