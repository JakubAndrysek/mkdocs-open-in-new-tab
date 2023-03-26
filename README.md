# MkDocs - Open in a new tab plugin

<p align="center">
<a href="https://hits.seeyoufarm.com"><img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FJakubAndrysek%2Fmkdocs-open-in-new-tab&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=true"/></a>
<img src="https://img.shields.io/github/license/JakubAndrysek/mkdocs-open-in-new-tab?style=flat-square">
<img src="https://img.shields.io/github/v/release/JakubAndrysek/mkdocs-open-in-new-tab?style=flat-square">
<img src="https://img.shields.io/github/stars/JakubAndrysek/mkdocs-open-in-new-tab?style=flat-square">
<img src="https://img.shields.io/github/forks/JakubAndrysek/mkdocs-open-in-new-tab?style=flat-square">
<img src="https://img.shields.io/github/issues/JakubAndrysek/mkdocs-open-in-new-tab?style=flat-square">
<img src="https://static.pepy.tech/personalized-badge/mkdocs-open-in-new-tab?period=month&units=international_system&left_color=black&right_color=orange&left_text=Downloads">


</p>

This plugin adds js to open outgoing links and PDFs in a new tab.

Look at the [demo](https://newtab.kubaandrysek.cz/).

## Installation

Install the plugin using pip from [PyPI](https://pypi.org/project/mkdocs-open-in-new-tab/):

```bash
pip3 install mkdocs-open-in-new-tab
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

Relative link to [Relative link](./docs/RelativeLink.md) should open in the same tab.

Sample PDF link to [PDF](./docs/assets/sample.pdf) should open in a new tab (pdf from [here](https://www.africau.edu/images/default/sample.pdf)).

## License

This project is licensed under the terms of the MIT license.