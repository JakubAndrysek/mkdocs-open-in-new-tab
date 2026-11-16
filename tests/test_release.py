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


@pytest.mark.parametrize("index", ["https://pypi.org", "https://test.pypi.org"])
def test_existing_version_rejected(guard, monkeypatch, index):
    from contextlib import nullcontext
    monkeypatch.setattr(guard, "urlopen", lambda url, timeout: nullcontext())
    with pytest.raises(ValueError, match="already exists"):
        guard.require_unused_version("1.0.8", index)


@pytest.mark.parametrize("status", [404, 403, 500])
def test_only_not_found_means_available(guard, monkeypatch, status):
    def response(url, timeout):
        raise guard.HTTPError(url, status, "error", {}, None)
    monkeypatch.setattr(guard, "urlopen", response)
    if status == 404:
        guard.require_unused_version("1.0.9")
    else:
        with pytest.raises(guard.HTTPError):
            guard.require_unused_version("1.0.9")


def test_network_errors_fail_closed(guard, monkeypatch):
    def response(url, timeout):
        raise TimeoutError()
    monkeypatch.setattr(guard, "urlopen", response)
    with pytest.raises(TimeoutError):
        guard.require_unused_version("1.0.9")


@pytest.mark.parametrize("runs,jobs,accepted", [("", "", False), ("123", "", False), ("123", "456", True)])
def test_requires_successful_test_upload(guard, monkeypatch, runs, jobs, accepted):
    calls = []
    sha = "a" * 40
    def output(command, text):
        calls.append(command)
        if "/workflows/" in command[3]:
            assert "head_sha=" + sha in command[3]
            assert 'select(.head_sha == "' + sha + '"' in command[5]
            assert '.actor.login == "JakubAndrysek"' in command[5]
            return runs
        assert 'select(.name == "publish-test" and .conclusion == "success")' in command[5]
        return jobs
    monkeypatch.setattr(guard.subprocess, "check_output", output)
    if accepted:
        guard.require_testpypi_run(sha)
    else:
        with pytest.raises(ValueError, match="No successful TestPyPI upload"):
            guard.require_testpypi_run(sha)
    assert all("--paginate" in call for call in calls)
