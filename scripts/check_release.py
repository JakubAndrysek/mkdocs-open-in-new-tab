"""Validate a stable release before building; run with Python 3.11+."""
import argparse
from pathlib import Path
import re
import subprocess
import tomllib
from urllib.error import HTTPError
from urllib.request import urlopen


def validate_tag(tag, version):
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
        raise ValueError("Only stable X.Y.Z releases are supported")
    if tag != "v" + version:
        raise ValueError("Release tag must be v" + version)


def validate_commit(repository):
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", "HEAD", "refs/remotes/origin/main"],
        cwd=repository, check=True,
    )


def require_unused_version(version, index="https://pypi.org"):
    url = index + "/pypi/mkdocs-open-in-new-tab/" + version + "/json"
    try:
        with urlopen(url, timeout=30):
            pass
    except HTTPError as error:
        if error.code == 404:
            return
        raise
    raise ValueError("Version " + version + " already exists on " + index)


def require_testpypi_run(sha):
    repo = "repos/JakubAndrysek/mkdocs-open-in-new-tab"
    # Paginate both APIs so older successful test runs are not overlooked.
    runs = subprocess.check_output([
        "gh", "api", "--paginate", repo + "/actions/workflows/publish.yaml/runs?event=workflow_dispatch&status=success&head_sha=" + sha,
        "--jq", '.workflow_runs[] | select(.head_sha == "' + sha + '" and .head_branch == "main" and .actor.login == "JakubAndrysek") | .id',
    ], text=True).split()
    for run in runs:
        jobs = subprocess.check_output([
            "gh", "api", "--paginate", repo + "/actions/runs/" + run + "/jobs?filter=latest",
            "--jq", '.jobs[] | select(.name == "publish-test" and .conclusion == "success") | .id',
        ], text=True).strip()
        if jobs:
            return
    raise ValueError("No successful TestPyPI upload found for commit " + sha)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", nargs="?")
    parser.add_argument("--test", action="store_true", help="Validate a TestPyPI build without a release tag")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    version = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    if args.tag is None and not args.test:
        parser.error("a release tag is required unless --test is specified")
    tag = args.tag if args.tag is not None else "v" + version
    validate_tag(tag, version)
    validate_commit(root)
    require_unused_version(version)
    if args.test:
        require_unused_version(version, "https://test.pypi.org")
    else:
        sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        require_testpypi_run(sha)
    print("Validated " + ("TestPyPI build " if args.test else "release ") + tag)


if __name__ == "__main__":
    main()
