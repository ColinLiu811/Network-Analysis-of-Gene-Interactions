# Installation Guide (Sprint 7)

## Option 1: Install from Source (Recommended for development)

```bash
git clone https://github.com/ColinLiu811/Network-Analysis-of-Gene-Interactions.git
cd Network-Analysis-of-Gene-Interactions
pip install -r requirements.txt
pip install -e .
```

Validate CLI entry points:

```bash
network-analysis --version
network-visualize --version
network-visualize-advanced --version
```

## Option 2: Local Package Build and Install

```bash
python -m pip install --upgrade pip build
python -m build
pip install dist/*.whl
```

## Running the Project

```bash
network-analysis --help
python run_pipeline.py --help
```

## Troubleshooting

- If `network-analysis` is not found, ensure your Python scripts directory is on `PATH`.
- If install fails, upgrade pip/setuptools/wheel and retry.
- Use a virtual environment to avoid dependency conflicts.
