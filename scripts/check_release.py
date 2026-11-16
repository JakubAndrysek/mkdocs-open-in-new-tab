"""Validate a stable release before building; run with Python 3.11+."""
import argparse
from pathlib import Path
import re
import subprocess
import tomllib


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
    print("Validated " + ("TestPyPI build " if args.test else "release ") + tag)


if __name__ == "__main__":
    main()
