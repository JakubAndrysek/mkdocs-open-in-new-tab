import json
from pathlib import Path

import pytest
from mkdocs.commands.build import build
from mkdocs.config import load_config

from open_in_new_tab.plugin import OpenInNewTabPlugin


@pytest.mark.parametrize("add_icon", [False, True])
def test_build_assets_and_nested_urls(tmp_path, add_icon):
    docs = tmp_path / "docs"
    (docs / "nested").mkdir(parents=True)
    (docs / "index.md").write_text("# Home\n[Page](nested/page.md)\n", encoding="utf-8")
    (docs / "nested/page.md").write_text("# Page\n[External](https://example.com)\n", encoding="utf-8")
    config_file = tmp_path / "mkdocs.yml"
    config_file.write_text(
        "site_name: Test\nsite_url: https://example.org/project/\n"
        "plugins:\n  - open-in-new-tab:\n"
        "      add_icon: " + str(add_icon).lower() + "\n",
        encoding="utf-8",
    )
    config = load_config(config_file=str(config_file), strict=True)
    build(config)
    site = Path(config.site_dir)
    package = Path(__file__).resolve().parents[1] / "open_in_new_tab"
    assert (site / "js/open_in_new_tab.js").read_bytes() == (package / "js/open_in_new_tab.js").read_bytes()
    assert (site / "css/open_in_new_tab.css").exists() is add_icon
    if add_icon:
        assert (site / "css/open_in_new_tab.css").read_bytes() == (package / "css/open_in_new_tab.css").read_bytes()
    for page, prefix in [("index.html", ""), ("nested/page/index.html", "../../")]:
        html = (site / page).read_text(encoding="utf-8")
        assert 'src="' + prefix + 'js/open_in_new_tab.js"' in html
        assert (prefix + "css/open_in_new_tab.css" in html) is add_icon


@pytest.mark.parametrize("hosts", [[], ["example.com", "localhost:8001"], ['quote"host', 'back\\slash', '\u017elu\u0165ou\u010dk\u00fd', '\u2028', '"];throw Error("injected");//']])
def test_exclude_hosts_build_and_rebuild(tmp_path, hosts):
    plugin = OpenInNewTabPlugin()
    errors, warnings = plugin.load_config({"exclude_hosts": hosts})
    assert not errors
    assert not warnings
    plugin.on_post_build({"site_dir": str(tmp_path)})
    script_path = tmp_path / "js/open_in_new_tab.js"
    script = script_path.read_text(encoding="utf-8")
    literal = script.split("const exclude_hosts = ", 1)[1].split(";\n", 1)[0]
    assert json.loads(literal) == hosts
    # A rebuild must overwrite old configuration, including when reset to empty.
    plugin.load_config({"exclude_hosts": []})
    plugin.on_post_build({"site_dir": str(tmp_path)})
    assert "const exclude_hosts = [];" in script_path.read_text(encoding="utf-8")
    assert (tmp_path / "css/open_in_new_tab.css").exists() is False


@pytest.mark.parametrize("value", ["example.com", 42, [42], [True], [None], [{}]])
def test_exclude_hosts_rejects_non_string_lists(value):
    plugin = OpenInNewTabPlugin()
    errors, _ = plugin.load_config({"exclude_hosts": value})
    assert errors
    assert any(key == "exclude_hosts" for key, _ in errors)
