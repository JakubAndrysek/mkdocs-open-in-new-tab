# MkDocs - Open in a new tab plugin

This plugin adds js to open outgoing links and PDFs in a new tab.

## Installation

Install the plugin using pip from [PyPI](https://pypi.org/project/mkdocs-open-in-new-tab-plugin/):

```bash
pip3 install mkdocs-open-in-new-tab-plugin
```

## Usage

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - open-in-new-tab
```


## Testing
Link to [Google](https://google.com) and [GitHub](https://github.com).
Both should links should open in a new tab.

Relative link to [Relative link](./RelativeLink.md) should open in the same tab.

Sample PDF link to [PDF](./assets/sample.pdf) should open in a new tab (pdf from [here](https://www.africau.edu/images/default/sample.pdf)).

## License

This project is licensed under the terms of the MIT license.