# Release Checklist

## Pre-Release

- [ ] Update `CHANGELOG.md` under `[Unreleased]`
- [ ] Confirm version in `pyproject.toml`
- [ ] Run local tests: `pytest tests/ -q`
- [ ] Validate CLI entry points (`network-analysis --version`, etc.)
- [ ] Build package artifacts: `python -m build`
- [ ] Build Docker image locally
- [ ] Review documentation links and examples

## Release Actions

- [ ] Create git tag: `vX.Y.Z`
- [ ] Push tag to remote
- [ ] Create GitHub release using release notes template
- [ ] Attach built wheel/sdist artifacts if desired

## Post-Release

- [ ] Verify install from wheel in clean environment
- [ ] Verify Docker image usability
- [ ] Move next changes into `[Unreleased]` section
