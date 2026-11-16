"""Release guard tests run independently of publishing credentials."""
import importlib.util
from pathlib import Path
import subprocess
import sys

import pytest

# The release helper uses stdlib tomllib; runtime support still starts at 3.8.
pytestmark = pytest.mark.skipif(sys.version_info < (3, 11), reason="Release tooling uses Python 3.14")


@pytest.fixture
def guard():
    spec = importlib.util.spec_from_file_location(
        "check_release", Path(__file__).resolve().parents[1] / "scripts/check_release.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("tag,version", [("1.0.9", "1.0.9"), ("v1.0.8", "1.0.9"), ("v1.0.9rc1", "1.0.9rc1")])
def test_invalid_release_tag(guard, tag, version):
    with pytest.raises(ValueError):
        guard.validate_tag(tag, version)


def test_valid_release_tag(guard):
    guard.validate_tag("v1.0.9", "1.0.9")


def test_release_commit_must_belong_to_main(guard, tmp_path):
    def git(*args):
        return subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True)

    git("init", "-b", "main")
    git("config", "user.name", "Release Test")
    git("config", "user.email", "test@example.com")
    git("commit", "--allow-empty", "-m", "base")
    git("update-ref", "refs/remotes/origin/main", "HEAD")
    guard.validate_commit(tmp_path)
    git("checkout", "-b", "unmerged")
    git("commit", "--allow-empty", "-m", "unreviewed")
    with pytest.raises(subprocess.CalledProcessError):
        guard.validate_commit(tmp_path)
