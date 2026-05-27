# Versioning Strategy

This project follows Semantic Versioning (`MAJOR.MINOR.PATCH`).

## Rules

- **MAJOR**: incompatible API or workflow changes
- **MINOR**: backward-compatible feature additions
- **PATCH**: backward-compatible bug fixes/documentation-only fixes

## Examples

- `1.1.0` -> add new visualization features and CLI options
- `1.1.1` -> fix parsing bug in existing command
- `2.0.0` -> break CLI behavior or output contract

## Process

1. Update version in `pyproject.toml`.
2. Add changelog entries under `CHANGELOG.md`.
3. Tag release (`vX.Y.Z`) and publish release notes.
