# Author: Jakub Andrýsek
# Email: email@kubaandrysek.cz
# Website: https://kubaandrysek.cz
# License: MIT
# GitHub: https://github.com/JakubAndrysek/mkdocs-open-in-new-tab
# PyPI: https://pypi.org/project/mkdocs-open-in-new-tab/
# Inspired by: https://github.com/timvink/mkdocs-charts-plugin/tree/main

import json
from pathlib import Path
from mkdocs.config.base import Config
from mkdocs.config.config_options import ListOfItems, Type
from mkdocs.plugins import BasePlugin
from mkdocs.utils import copy_file


class OpenInNewTabPluginConfig(Config):
    add_icon = Type(bool, default=False)
    exclude_hosts = ListOfItems(Type(str), default=[])


class OpenInNewTabPlugin(BasePlugin[OpenInNewTabPluginConfig]):
    def on_config(self, config, **kwargs):
        """
        Event trigger on config.
        See https://www.mkdocs.org/user-guide/plugins/#on_config.
        """
        # Add pointer to open_in_new_tab.js file to extra_javascript
        config["extra_javascript"].append("js/open_in_new_tab.js")

        # If add_icon is True, add extra CSS to extra_css
        if self.config.add_icon:
            config["extra_css"].append("css/open_in_new_tab.css")

    def on_post_build(self, config):
        """
        Event trigger on post build.
        See https://www.mkdocs.org/user-guide/plugins/#on_post_build.
        """
        site_dir = Path(config["site_dir"])
        js_asset_path = "js/open_in_new_tab.js"
        self.copy_asset(js_asset_path, site_dir)
        if self.config.exclude_hosts:
            dest_path = site_dir / js_asset_path
            exclude_hosts_str = json.dumps(self.config.exclude_hosts)
            dest_path.write_text(
                dest_path.read_text(encoding="utf-8").replace(
                    "const exclude_hosts = [];",
                    f"const exclude_hosts = {exclude_hosts_str};",
                ),
                encoding="utf-8",
            )

        if self.config.add_icon:
            self.copy_asset("css/open_in_new_tab.css", site_dir)

    def copy_asset(self, asset_path: str, site_dir: Path):
        """
        Copy an asset file to the output directory.
        """
        source_path = Path(__file__).parent / asset_path
        dest_path = site_dir / asset_path
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        copy_file(source_path, dest_path)
