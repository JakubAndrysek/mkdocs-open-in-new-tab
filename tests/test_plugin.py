from pathlib import Path

import pytest
from mkdocs.commands.build import build
from mkdocs.config import load_config


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
