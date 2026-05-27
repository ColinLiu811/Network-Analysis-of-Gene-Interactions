# Tutorial: Troubleshooting Common Issues

## 1. Missing Dependencies

Symptom:
- `ModuleNotFoundError` for `pandas`, `networkx`, `pyvis`, or others

Fix:
```bash
pip install -r requirements.txt
```

## 2. Input File Not Found

Symptom:
- pipeline exits early with missing CSV/GraphML/hub file errors

Fix:
- verify file names and paths
- run prior stage to generate required intermediate outputs
- ensure current working directory is project root

## 3. Slow or Heavy Visualizations

Symptom:
- long runtime or high memory use during visualization

Fix:
- lower visualization node counts (`--max-nodes`, `--interactive-max-nodes`)
- use static output only with `--skip-interactive`
- export vector formats selectively to reduce repeated heavy renders

## 4. Interactive HTML Not Generated as Expected

Symptom:
- no pyvis output or browser issues

Fix:
- use default vis.js backend (`--interactive-backend visjs`)
- verify output file opens in a modern browser
- if needed, generate both backends: `--interactive-backend both`

## 5. Centrality Stage Takes Too Long

Symptom:
- long processing on very large graphs

Fix:
- test with smaller subset first
- reduce top-N for exploratory iterations
- run heavy analysis in stages and checkpoint outputs

## Success Check

Given an execution failure, when the matching issue class is addressed, then
the failing stage should complete and produce expected output files.
