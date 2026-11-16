import email
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]


def test_sdist_rebuild_and_pip_install(tmp_path):
    dist = tmp_path / "dist"
    subprocess.run(
        [sys.executable, "-m", "build", "--outdir", str(dist), str(ROOT)],
        check=True,
    )  # The default build makes a wheel from the sdist, not the checkout.
    sdist, = dist.glob("*.tar.gz")
    with tarfile.open(sdist) as archive:
        names = archive.getnames()
        for suffix in ["pyproject.toml", "README.md", "LICENSE", "open_in_new_tab/plugin.py",
                       "open_in_new_tab/js/open_in_new_tab.js", "open_in_new_tab/css/open_in_new_tab.css"]:
            assert any(name.endswith("/" + suffix) for name in names)
    wheel, = dist.glob("*.whl")
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        for asset in ["js/open_in_new_tab.js", "css/open_in_new_tab.css"]:
            assert archive.read("open_in_new_tab/" + asset) == (ROOT / "open_in_new_tab" / asset).read_bytes()
        assert not any(name.startswith(("tests/", "docs/", ".github/")) for name in names)
        metadata = email.message_from_bytes(archive.read(next(n for n in names if n.endswith("/METADATA"))))
        assert metadata["Name"] == "mkdocs-open-in-new-tab"
        assert metadata["Requires-Python"] == ">=3.8"
        assert "mkdocs>=1.4" in metadata.get_all("Requires-Dist")
        assert any(n.endswith("/licenses/LICENSE") for n in names)
    installed = tmp_path / "installed"
    # pip belongs to the temporary tooling environment; install into an isolated target.
    subprocess.run([sys.executable, "-m", "pip", "install", "--no-deps", "--target", str(installed), str(wheel)], check=True)
    env = dict(os.environ, PYTHONPATH=str(installed))
    subprocess.run([sys.executable, "-c", """
from importlib.metadata import distribution
from pathlib import Path
import open_in_new_tab
root = Path(open_in_new_tab.__file__).parent
assert root.parent.name == 'installed'
entry, = [e for e in distribution('mkdocs-open-in-new-tab').entry_points if e.group == 'mkdocs.plugins']
assert entry.name == 'open-in-new-tab'
assert entry.load().__name__ == 'OpenInNewTabPlugin'
for asset in ['js/open_in_new_tab.js', 'css/open_in_new_tab.css']:
    assert (root / asset).is_file()
"""], cwd=tmp_path, env=env, check=True)
