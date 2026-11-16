# Changelog

## Unreleased

- Add `exclude_hosts` to skip selected hosts in the external-link rule, with
  validated configuration and safe JSON serialization.
- Support InstantClick navigation alongside existing Material instant navigation.
- Fix building wheels from source distributions by moving package metadata to
  `pyproject.toml` and adopting `uv_build`.
- Add locked uv development dependencies and Python/JavaScript regression tests.
- Raise the minimum supported Python version from 3.7 to 3.8 and declare the
  existing requirement for MkDocs 1.4 or newer.
- Add approval-gated Trusted Publishing: manual TestPyPI uploads followed by
  production publishing when the owner publishes a matching GitHub Release.
