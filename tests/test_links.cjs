const assert = require('node:assert/strict');
const {test} = require('node:test');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../open_in_new_tab/js/open_in_new_tab.js'), 'utf8');

for (const mode of ['dom', 'material', 'instant', 'both']) {
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
    if (mode === 'instant' || mode === 'both') {
      context.InstantClick = {on: (event, cb) => {
        assert.equal(event, 'change');
        assert.equal(mode, 'instant', 'Material takes precedence when both hooks exist');
        callback = cb;
      }};
    }
    if (mode === 'material' || mode === 'both') {
      context.document$ = {subscribe: cb => {callback = cb;}};
    }
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

test('host exclusions match exactly and preserve the separate document rule', () => {
  const hosts = ['excluded.example', 'localhost:8001', 'quote"host', 'back\\slash', '\u2028'];
  const script = source.replace('const exclude_hosts = [];',
    `const exclude_hosts = ${JSON.stringify(hosts)};`);
  function link(href) {
    const url = new URL(href);
    return {href: url.href, host: url.host, getAttribute: () => href};
  }
  const links = [link('https://excluded.example/'), link('http://localhost:8001/'),
    link('http://localhost:8002/'), link('https://sub.excluded.example/'),
    link('https://excluded.example/FILE.PDF'), link('https://normal.example/')];
  links[0].target = '_self';
  links[0].rel = 'nofollow';
  let callback;
  const opened = [];
  vm.runInNewContext(script, {
    document: {getElementsByTagName: () => links,
      addEventListener: (_, cb) => {callback = cb;}},
    location: {host: 'docs.example'}, window: {open: href => opened.push(href)}
  });
  callback();
  assert.equal(links[0].target, '_self');
  assert.equal(links[0].rel, 'nofollow');
  assert.equal(links[1].target, undefined);
  for (const index of [2, 3, 5]) assert.equal(links[index].target, '_blank');
  assert.equal(links[4].target, undefined);
  assert.equal(links[4].onclick(), false);
  assert.deepEqual(opened, [links[4].href]);
});
