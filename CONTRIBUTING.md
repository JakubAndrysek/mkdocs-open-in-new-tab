# Development

The plugin supports Python 3.8 and newer (previously 3.7). The minimum MkDocs
version is 1.4, which provides the typed plugin configuration API used here.
Users can continue installing the package with pip; uv is only a development tool.

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then run:

```sh
uv sync --python 3.14 --locked --extra dev
uv run --locked --extra dev pytest -q
node --test tests/test_links.cjs
make docs-build
make package
```

`pyproject.toml` is the source of metadata and dependencies; `uv.lock` records
resolved development dependencies. `requirements.txt` and `devdeps.txt` remain
convenience entry points for pip. `pip install -e '.[dev]'` also works.
Use `uv lock` after intentional dependency changes and commit the updated lockfile.

CI tests Python 3.8–3.15. Dependency versions may differ by Python version, as
recorded in the lockfile. For example, old Python versions use an older build
frontend. CI also builds the documentation and validates distribution metadata.
The packaging regression test builds a wheel from the sdist and installs it with
pip outside the checkout, checking the plugin entry point and bundled JS/CSS.
The integration tests build root and nested pages with icons enabled and disabled.

The `uv_build` backend preserves the existing `open_in_new_tab/` layout and
includes the package's CSS and JavaScript in both distributions. Tests are included
in the sdist, but excluded from the wheel.

## Releases

Publishing remains manual: `make release-test` uploads to TestPyPI and
`make release` uploads to PyPI using your locally configured credentials.
Neither CI nor publishing documentation uploads a Python package.

Before a release, update the version in `pyproject.toml`, regenerate the lockfile,
run tests and review artifacts. Create a matching version tag and GitHub Release.
Automated Trusted Publishing will be handled separately; this migration keeps the
existing version 1.0.8 and does not publish it again.
