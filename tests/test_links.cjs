const assert = require('node:assert/strict');
const {test} = require('node:test');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../open_in_new_tab/js/open_in_new_tab.js'), 'utf8');

for (const mode of ['dom', 'material']) {
  test(`${mode}: external hosts, ports, documents and repeated navigation`, () => {
    function link(href) {
      const url = new URL(href, 'https://docs.example:8000/');
      return {href: url.href, host: url.host, getAttribute: () => href};
    }
    let links = [link('/internal'), link('https://other.example/'),
      link('https://docs.example:9000/'), link('/FILE.PDF'), link('/archive.zip')];
    let callback;
    const opened = [];
    const context = {
      document: {getElementsByTagName: () => links, addEventListener: (name, cb) => {
        assert.equal(name, 'DOMContentLoaded'); callback = cb;
      }},
      location: {host: 'docs.example:8000'}, window: {open: href => opened.push(href)}
    };
    if (mode === 'material') context.document$ = {subscribe: cb => {callback = cb;}};
    vm.runInNewContext(source, context);
    callback();
    assert.equal(links[0].target, undefined);
    for (const external of links.slice(1, 3)) {
      assert.equal(external.target, '_blank');
      assert.equal(external.rel, 'noopener');
    }
    for (const document of links.slice(3)) assert.equal(document.onclick(), false);
    assert.deepEqual(opened, links.slice(3).map(link => link.href));
    links = [link('https://new.example/')];
    callback();
    assert.equal(links[0].target, '_blank');
  });
}
