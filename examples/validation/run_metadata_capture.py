"""
Capture reproducibility metadata for a run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def capture_packages() -> List[str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture environment and file metadata for reproducibility.")
    parser.add_argument("--inputs", nargs="*", default=[])
    parser.add_argument("--outputs", nargs="*", default=[])
    parser.add_argument("--command", default="")
    parser.add_argument("--out", default="run_metadata.json")
    args = parser.parse_args()

    data: Dict[str, object] = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "command": args.command,
        "inputs": [],
        "outputs": [],
        "pip_freeze": capture_packages(),
    }

    for p in args.inputs:
        path = Path(p)
        if path.exists() and path.is_file():
            data["inputs"].append(
                {"path": str(path), "sha256": sha256_file(path), "size_bytes": path.stat().st_size}
            )
    for p in args.outputs:
        path = Path(p)
        if path.exists() and path.is_file():
            data["outputs"].append(
                {"path": str(path), "sha256": sha256_file(path), "size_bytes": path.stat().st_size}
            )

    out = Path(args.out)
    out.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Wrote metadata to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
