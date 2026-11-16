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

The Makefile provides shortcuts for common tasks:

- `make test`: runs both `uv run --locked --extra dev pytest -q` and
  `node --test tests/test_links.cjs` (requires Node.js 20+).
- `make docs-serve` / `make docs-build`: prepares documentation copies, then
  runs `uv run --locked --extra dev mkdocs serve` or `mkdocs build --clean --strict`.
- `make package`: runs `uv build` and
  `uv run --locked --extra dev twine check dist/*` after removing old artifacts.
- `make clean`: removes build artifacts.

For development setup use `uv sync --locked --extra dev`; to install the package
with its runtime dependencies use `python -m pip install .`.

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

Publishing uses PyPI Trusted Publishing (OIDC); no upload token is stored in GitHub.
The owner prepares the version in a PR, tests it on TestPyPI, then creates the
GitHub Release and approves the production upload. The workflow supports stable
`X.Y.Z` versions only and rejects prereleases. Nothing is published on an ordinary
push or PR. Build validation runs on PRs that change the publishing workflow.

### One-time setup

The repository environments have been configured as follows; preserve these
settings when changing publishing configuration. Use `testpypi` and `pypi`, each with `JakubAndrysek` as the
only required reviewer. Allow self-review (the owner initiates the release),
disable administrator bypass, and restrict `testpypi` to branch `main` and `pypi`
to tags `v*`.

Configure a GitHub Trusted Publisher in **both** PyPI and TestPyPI. These are
separate accounts/services; configure each independently:

| Field | Value |
| --- | --- |
| Owner | `JakubAndrysek` |
| Repository | `mkdocs-open-in-new-tab` |
| Workflow filename | `publish.yaml` |
| Environment | `pypi` on PyPI; `testpypi` on TestPyPI |

On PyPI, use the existing project's Publishing settings. On TestPyPI, use a
pending publisher if the project does not yet exist. Enable account 2FA and keep
recovery codes safe. See the [PyPI setup guide](https://docs.pypi.org/trusted-publishers/adding-a-publisher/).

### Prepare and test a version

1. Update `project.version` in `pyproject.toml` to an unused version, run `uv lock`,
   and add release notes to `CHANGELOG.md`. The current 1.0.8 is already on PyPI;
   it must not be published again. Merge the version PR after all CI checks pass.
2. Open Actions → **Build and publish release** → **Run workflow** on `main`.
   Manual runs publish only to TestPyPI. Approve the `testpypi` environment after
   the build succeeds and inspect the resulting package.
3. Test installation in a fresh environment. Install runtime dependencies from
   PyPI first, then install the exact test package from TestPyPI without resolving
   dependencies there (replace `X.Y.Z`):

   ```sh
   uv venv /tmp/newtab-release-check
   uv pip install --python /tmp/newtab-release-check/bin/python 'mkdocs>=1.4'
   uv pip install --python /tmp/newtab-release-check/bin/python --no-deps \
     --index-url https://test.pypi.org/simple/ 'mkdocs-open-in-new-tab==X.Y.Z'
   ```

   Build a small MkDocs site with the plugin, including `add_icon` and
   `exclude_hosts`. Each service forbids reusing an uploaded filename: if the
   package needs changes, choose a new version and repeat. A TestPyPI run does
   not automatically promote its artifact; production rebuilds and verifies the
   release commit. Keep that commit identical to the tested commit.

### Publish on PyPI

1. As `JakubAndrysek`, create a GitHub Release with tag `vX.Y.Z` at the exact
   tested commit on `main`, using the changelog as release notes. Publishing the
   release starts the workflow. A draft does not publish a package.
2. The build validates the tag against metadata, checks that the commit belongs
   to `main`, runs tests and docs, and builds/checks wheel and sdist. Artifacts are
   available on the workflow run for 14 days.
3. Review the build and approve the `pypi` environment. A separate job downloads
   and publishes those artifacts with OIDC and attestations; it does not check
   out code or rebuild the package. Only the publishing job has `id-token: write`.
4. Verify the version on PyPI and installation from a fresh environment, then
   close release-dependent issues such as #15.

The workflow accepts production releases only from `JakubAndrysek`. The required
environment approval is the final publishing gate. If the build fails, fix the
problem through a PR and use a new version/tag as needed. If upload fails before
any files reach PyPI, fix the configuration and rerun the failed job. For a partial
upload, inspect PyPI before retrying; existing files cannot be overwritten.
