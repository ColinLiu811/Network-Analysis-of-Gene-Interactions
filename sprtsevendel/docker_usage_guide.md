# Docker Usage Guide (Sprint 7)

## Build the Image

```bash
docker build -t network-analysis-gene-interactions:latest .
```

## Run Help Command

```bash
docker run --rm network-analysis-gene-interactions:latest
```

## Run a Specific Script in Container

```bash
docker run --rm -v "$(pwd)":/app -w /app network-analysis-gene-interactions:latest \
  python run_pipeline.py --help
```

## Using Docker Compose

```bash
docker compose up --build
```

Run ad-hoc command:

```bash
docker compose run --rm network-analysis python visualize_network.py --help
```

## Notes

- Mounting the repository (`-v "$(pwd)":/app`) keeps generated outputs on host.
- Large input datasets should be placed in the mounted project directory.
