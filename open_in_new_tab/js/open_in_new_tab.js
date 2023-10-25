// Icon SVG
// const newTabIcon = `<svg style="vertical-align: middle; margin-left: 4px; fill: currentColor;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z"></path></svg>`;
const newTabIcon = `<svg style="vertical-align: middle; margin-left: 4px; fill: currentColor; width: 1em; height: 1em;" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M3.75 2h3.5a.75.75 0 0 1 0 1.5h-3.5a.25.25 0 0 0-.25.25v8.5c0 .138.112.25.25.25h8.5a.25.25 0 0 0 .25-.25v-3.5a.75.75 0 0 1 1.5 0v3.5A1.75 1.75 0 0 1 12.25 14h-8.5A1.75 1.75 0 0 1 2 12.25v-8.5C2 2.784 2.784 2 3.75 2Zm6.854-1h4.146a.25.25 0 0 1 .25.25v4.146a.25.25 0 0 1-.427.177L13.03 4.03 9.28 7.78a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042l3.75-3.75-1.543-1.543A.25.25 0 0 1 10.604 1Z"></path></svg>`;


// Append the SVG icon after a link
function appendIcon(linkElement) {
    // Check if the icon already exists next to the link, if not, append it
    if (!linkElement.nextElementSibling || linkElement.nextElementSibling.innerHTML !== newTabIcon) {
        linkElement.insertAdjacentHTML('afterend', newTabIcon);
    }
}

// Open external links in a new tab
function external_new_window() {
    for (let c = document.getElementsByTagName("a"), a = 0; a < c.length; a++) {
        let b = c[a];
        if (b.getAttribute("href") && b.hostname !== location.hostname) {
            b.target = "_blank";
            b.rel = "noopener";
            appendIcon(b);
        }
    }
}

// Open PDF links in a new tab
function pdf_new_window() {
    let links = document.getElementsByTagName("a");
    for (let eleLink = 0; eleLink < links.length; eleLink++) {
        if (links[eleLink].href.endsWith('.pdf') || links[eleLink].href.endsWith('.doc') || links[eleLink].href.endsWith('.docx')) {
            links[eleLink].onclick = function () {
                window.open(this.href);
                return false;
            }
            appendIcon(links[eleLink]);
        }
    }
}

function apply_rules() {
    external_new_window();
    pdf_new_window();
}

if (typeof document$ !== "undefined") {
    document$.subscribe(function () {
        apply_rules();
    })
}
