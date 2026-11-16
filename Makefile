.PHONY: package release release-test clean test docs-serve docs-build fixRelativeLinkDocs

package:
	rm -rf dist
	uv build
	uv run --locked --extra dev twine check dist/*

# Publishing remains manual until a separate release workflow is approved.
release: package
	uv run --locked --extra dev twine upload --repository pypi dist/*

release-test: package
	uv run --locked --extra dev twine upload --repository testpypi dist/*

clean:
	rm -rf dist build *.egg-info

test:
	uv run --locked --extra dev pytest -q
	node --test tests/test_links.cjs

fixRelativeLinkDocs:
	sed 's/\.\/docs\//\.\//g' README.md > docs/README.md
	cp RelativeLink.md docs/RelativeLink.md

docs-serve: fixRelativeLinkDocs
	uv run --locked --extra dev mkdocs serve

docs-build: fixRelativeLinkDocs
	uv run --locked --extra dev mkdocs build --clean --strict
