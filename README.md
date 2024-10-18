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

This plugin adds JS code to open outgoing links and PDFs in a new tab.

The automatic opening of links in a new tab is a common feature of modern websites. It is also a good practice for accessibility. However, it is not a default behavior of Markdown. This plugin adds a JavaScript code to your website that opens external links and PDFs in a new tab.

Look at the [demo](https://newtab.kubaandrysek.cz/).

## Installation

Install the plugin using pip from [PyPI](https://pypi.org/project/mkdocs-open-in-new-tab/):

```bash
pip install mkdocs-open-in-new-tab
```

## Usage

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - search
  - open-in-new-tab
```

## Configuration

The plugin supports the following configuration option:

- `add_icon:` (default: false)
    - If set to true, the plugin will add an icon next to external links.


## Testing
Link to [Google](https://google.com) and [GitHub](https://github.com).
Both should links should open in a new tab.

Relative link to [Relative link](./docs/RelativeLink.md) should open in the same tab.

Sample PDF link to [PDF](./docs/assets/sample.pdf) should open in a new tab (pdf from [here](https://www.africau.edu/images/default/sample.pdf)).


# How does it work?
The plugin adds a JavaScript code to your website that opens external links and PDFs in a new tab. Injection of the code is done using the `on_page_context` hook. The code is injected into the `<head>` section of the page as a `<script>` dependency of the `open_in_new_tab.js` file. The code is automatically added to all pages of your website.


The function `external_new_window` checks if the link is external using the `hostname` property of the `a` element. If the link is external, the `target` attribute is set to `_blank` and the `rel` attribute is set to `noopener`. The `noopener` attribute is used to prevent the new tab from accessing the `window.opener` property and ensures that the original page will not be able to access the new tab.

The same way is used to open PDF links in a new tab.



<details><summary>Show source code</summary>
<p>

Look at this source <a href="https://github.com/JakubAndrysek/mkdocs-open-in-new-tab/blob/main/open_in_new_tab/js/open_in_new_tab.js">open_in_new_tab.js</a>:

```js
// Description: Open external links in a new tab and PDF links in a new tab
// Based on: https://jekyllcodex.org/without-plugin/new-window-fix/

// Open external links in a new window
function external_new_window() {
    for(let c = document.getElementsByTagName("a"), a = 0; a < c.length; a++) {
        let b = c[a];
        if(b.getAttribute("href") && b.host !== location.host) {
            b.target = "_blank";
            b.rel = "noopener";
        }
    }
}

// Open PDF links in a new window
function pdf_new_window() {
    if (!document.getElementsByTagName) {
        return false;
    }

    const extensions = ['.pdf', '.doc', '.docx', '.json', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar', '.tar', '.gz', '.7z', '.bz2', '.xz', '.tgz', '.tar.gz'];
    let links = document.getElementsByTagName("a");

    for (let eleLink = 0; eleLink < links.length; eleLink++) {
        let href = links[eleLink].href.toLowerCase(); // Convert href to lowercase for case-insensitive matching

        if (extensions.some(ext => href.endsWith(ext))) {
            links[eleLink].onclick = function() {
                window.open(this.href);
                return false;
            }
        }
    }
}

function apply_rules() {
    external_new_window();
    pdf_new_window();
}

if (typeof document$ !== "undefined") {
    // Compatibility with mkdocs-material's instant loading feature
    document$.subscribe(function() {
        apply_rules();
    });
} else {
    // For browsers without mkdocs-material's instant loading feature
    document.addEventListener("DOMContentLoaded", function() {
        apply_rules();
    });
}

```

`open_in_new_tab.css` (added when add_icon: true)

```css
/*
 * Materialize links that open in a new window with a right-up arrow icon
 * Author: @ebouchut (https://github.com/ebouchut)
 * https://github.com/JakubAndrysek/mkdocs-open-in-new-tab/issues/4
 */
 a[target="_blank"]::after {
    content: "↗";
    display: inline-block;
    margin-left: 0.2em;
    width: 1em;
    height: 1em;
}
```

</p>
</details>


## License

This project is licensed under the terms of the MIT license.
