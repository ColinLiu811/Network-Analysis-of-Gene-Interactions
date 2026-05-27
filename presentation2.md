# 30-Minute Project Presentation (Pre-Sprint Context + 8 Sprints)

**Total Time:** ~30 minutes  
**Format:** 15 slides x ~2 minutes each

---

## Slide 1 (2 min) — Project Title and Goal

### Talking Points
- Project: Protein-Protein Interaction (PPI) Network Analysis.
- Goal: find meaningful hub genes from STRING interaction data.
- Emphasis: research quality + software engineering progression.

### Code
```python
project = {
    "name": "Protein-Protein Interaction Network Analysis",
    "goal": "Identify hub genes using network centrality + reproducible tooling",
    "data_source": "STRING database",
}
print(project)
```

---

## Slide 2 (2 min) — Before the 8 Sprints: Baseline State

### Talking Points
- Before sprint work, there was a basic linear script workflow.
- Core scripts existed but were less structured for testing, scaling, and reuse.
- Limited reproducibility and deployment readiness.

### Code
```bash
# baseline usage pattern before structured sprint improvements
python clean_data.py
python build_graph.py
python compute_centrality.py
python visualize_network.py
```

---

## Slide 3 (2 min) — Before the 8 Sprints: Initial Technical Foundation

### Talking Points
- Main graph and centrality pipeline already in place.
- Initial outputs: CSV rankings + static/interactive visualizations.
- Main gaps: QA depth, performance strategy, advanced analytics, packaging.

### Code
```python
# simplified baseline idea
import networkx as nx
G = nx.read_graphml("string_network.graphml")
degree = nx.degree_centrality(G)
top = sorted(degree.items(), key=lambda x: x[1], reverse=True)[:10]
print(top)
```

---

## Slide 4 (2 min) — Sprint 1: Testing and Quality Assurance

### Talking Points
- Added structured tests and coverage workflow.
- Established confidence around data-cleaning correctness.
- Introduced repeatable validation mindset.

### Code
```bash
# sprint 1 style quality check
pytest tests/ -q
pytest --cov=clean_data --cov-report=term-missing
```

---

## Slide 5 (2 min) — Sprint 2: Bug Fixes and Error Handling

### Talking Points
- Improved runtime reliability and input handling.
- Better interpreter portability using robust command execution.
- Reduced brittle behavior in pipeline stages.

### Code
```python
import sys, subprocess
cmd = [sys.executable, "run_pipeline.py", "--help"]
subprocess.run(cmd, check=True)
```

---

## Slide 6 (2 min) — Sprint 3: Performance and Scalability

### Talking Points
- Added optimization-oriented modules and benchmarking direction.
- Focused on large-network feasibility (memory/time awareness).
- Built performance documentation and analysis support.

### Code
```python
import time
start = time.time()
# placeholder for centrality run
# compute_centrality_optimized.main(...)
elapsed = time.time() - start
print(f"Elapsed: {elapsed:.2f}s")
```

---

## Slide 7 (2 min) — Sprint 4: Advanced Network Analysis Features

### Talking Points
- Expanded beyond basic centrality into deeper network analytics.
- Added advanced feature documentation and analysis scripts.
- Improved scientific interpretability of network structure.

### Code
```python
# representative advanced-analysis style call
from sprtfourdel.advanced_analysis import analyze_centrality_correlations
# correlations = analyze_centrality_correlations(df)
# print(correlations.head())
print("Advanced analysis module introduced in Sprint 4")
```

---

## Slide 8 (2 min) — Sprint 5: Enhanced Visualization and CLI UX

### Talking Points
- Major visualization upgrade: filtering/search, richer exports.
- Config-driven behavior via YAML.
- Better CLI ergonomics and advanced visualization wrapper.

### Code
```bash
python visualize_network.py string_network.graphml hub_genes.csv \
  --layout kamada_kawai \
  --color-scheme community \
  --formats svg,pdf \
  --dpi 600
```

---

## Slide 9 (2 min) — Sprint 6: Documentation and Examples

### Talking Points
- Added tutorials, examples, and notebooks for onboarding.
- Improved discoverability in README and contributor documentation.
- Shifted project from “works for author” to “usable by others”.

### Code
```python
from pathlib import Path
tutorials = list(Path("sprtsixdel").glob("tutorial_*.md"))
print("Tutorial count:", len(tutorials))
for t in tutorials:
    print("-", t.name)
```

---

## Slide 10 (2 min) — Sprint 7: Distribution and Deployment

### Talking Points
- Added package metadata and CLI entry points.
- Added Docker + compose support.
- Expanded CI to multi-OS, package builds, and Docker builds.

### Code
```toml
[project.scripts]
network-analysis = "run_pipeline:main"
network-visualize = "visualize_network:main"
network-visualize-advanced = "visualize_network_advanced:main"
```

---

## Slide 11 (2 min) — Sprint 8: Validation and Reproducibility

### Talking Points
- Added formal validation framework and reproducibility guide.
- Added run metadata capture and stability comparison scripts.
- Established acceptance criteria (overlap/correlation consistency).

### Code
```bash
python examples/validation/stability_analysis.py \
  hub_genes_run_a.csv hub_genes_run_b.csv \
  --top-n 50 --out validation_summary.json
```

---

## Slide 12 (2 min) — End-to-End Architecture After 8 Sprints

### Talking Points
- Pipeline now spans data ingestion to reproducible reporting.
- Better engineering lifecycle: dev, test, docs, package, deploy, validate.
- Stronger research/software integration.

### Code
```python
stages = [
    "ingest", "clean", "build_graph", "centrality",
    "visualize", "document", "package", "validate"
]
print(" -> ".join(stages))
```

---

## Slide 13 (2 min) — Representative Result Interpretation

### Talking Points
- Hub candidates interpreted using multiple metrics, not one.
- Visual context (communities + hub neighborhoods) improves confidence.
- Validation scripts support run-to-run stability checks.

### Code
```python
import pandas as pd
hubs = pd.read_csv("hub_genes.csv")
print(hubs[["protein_id", "hub_score", "degree"]].head(10).to_string(index=False))
```

---

## Slide 14 (2 min) — Lessons Learned Across the 8 Sprints

### Talking Points
- Data science success depends on software-engineering rigor.
- Reproducibility and usability are first-class technical goals.
- Iterative sprint structure made complexity manageable.

### Code
```python
lessons = {
    "quality": "tests + CI",
    "usability": "docs + examples + CLI",
    "reliability": "packaging + containers + reproducibility metadata",
}
print(lessons)
```

---

## Slide 15 (2 min) — Future Work and Q&A

### Talking Points
- Next directions: benchmark-grounded biological validation, CI-gated validation thresholds, richer comparative studies.
- Optional web interface and production release automation.
- Invite questions on methods, code, and research implications.

### Code
```python
next_steps = [
    "Automated validation thresholds in CI",
    "Expanded biological benchmark datasets",
    "Release automation + artifact publishing",
]
for i, step in enumerate(next_steps, 1):
    print(f"{i}. {step}")
```

---

## Optional Backup Demo Commands (if time remains)

```bash
python run_pipeline.py --help
python visualize_network.py --help
python examples/validation/run_metadata_capture.py --help
python examples/validation/stability_analysis.py --help
```
