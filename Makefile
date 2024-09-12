.PHONY: package install install-dev release release-test clean reviewCode docs-serve docs-build fixRelativeLinkDocs

# Packaging
package:
	rm -f dist/*
	python3 -m build --wheel  # Updated to use python3 build tool for wheel
	python3 setup.py sdist

install: package
	python3 -m pip install --no-deps --force dist/*.whl

install-dev: package
	python3 -m pip install --force --editable .

# Releasing
release: package
	twine upload --repository pypi dist/*

release-test: package
	twine upload --repository testpypi dist/*

# Clean build directories
clean:
	rm -rf dist build *.egg-info

# Fix relative links in documentation
fixRelativeLinkDocs:
	# change ./docs/ to ./
	sed  's/\.\/docs\//\.\//g' README.md > docs/README.md
	cp RelativeLink.md docs/RelativeLink.md

# Code review
reviewCode:
	sourcery review mkdoxy --in-place

# Documentation
docs-serve: fixRelativeLinkDocs
	mkdocs serve

docs-build: fixRelativeLinkDocs
	mkdocs build
