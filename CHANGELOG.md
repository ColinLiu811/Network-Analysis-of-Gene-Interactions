# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Sprint 7 distribution assets:
  - `pyproject.toml` packaging metadata and CLI entry points
  - Docker support (`Dockerfile`, `docker-compose.yml`, `.dockerignore`)
  - sprint deliverables in `sprtsevendel/` (installation, Docker, release docs)
- CI workflow enhancements for:
  - multi-OS and multi-version test matrix
  - package build artifacts
  - Docker image build validation
- Sprint 8 validation and reproducibility assets:
  - `sprteightdel/` deliverables (framework, guide, template, config)
  - `examples/validation/` scripts for stability analysis and metadata capture
  - `examples/notebooks/validation_stability.ipynb`

## [1.0.0] - 2024-12-XX

### Added
- Complete protein-protein interaction network analysis pipeline
- STRING database data download and processing (`download_string_data.py`)
- Data cleaning and formatting (`clean_data.py`)
- Network graph construction using NetworkX (`build_graph.py`)
- Centrality computation with multiple measures (`compute_centrality.py`)
  - Degree centrality
  - Betweenness centrality
  - Closeness centrality
  - Eigenvector centrality
  - PageRank
  - Clustering coefficient
- Hub gene identification with composite scoring
- Network visualization tools (`visualize_network.py`)
  - Full network visualization
  - Hub gene network visualization
  - Community structure visualization
  - Interactive HTML visualizations
  - Summary statistics plots
- Automated pipeline execution (`run_pipeline.py`)
- Comprehensive documentation
  - README.md with usage instructions
  - QUICKSTART.md guide
  - Project portfolio and presentation materials
- GitHub Actions CI workflow
- Support for GraphML and GEXF graph formats
- Community detection using Louvain algorithm

### Changed
- Updated project structure to focus on STRING database analysis
- Improved data processing pipeline
- Enhanced visualization capabilities

### Fixed
- Data cleaning and deduplication issues
- Graph construction edge cases
- Visualization performance for large networks

## [0.1.0] - Previous Version

### Added
- Initial gene interaction network analysis tool
- Basic network analysis functionality
- Example data generation
- Static and interactive visualizations

[Unreleased]: https://github.com/ColinLiu811/Network-Analysis-of-Gene-Interactions/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/ColinLiu811/Network-Analysis-of-Gene-Interactions/releases/tag/v1.0.0

