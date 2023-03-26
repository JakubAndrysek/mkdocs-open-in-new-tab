.PHONY: package release release-test clean reviewCode docs-serve docs-build

# Packaging
package:
	rm -f dist/*
	python3 setup.py sdist bdist_wheel

install: package
	python3 -m pip install --no-deps --force dist/*.whl

install-dev: package
	python3 -m pip install --force --editable .

release: package
	twine upload --repository pypi dist/*

release-test: package
	twine upload --repository testpypi dist/*

clean:
	rm -rf dist build


fixRelativeLinkDocs:
	# change ./docs/ to ./
	sed  's/\.\/docs\//\.\//g' README.md > docs/README.md
	cp RelativeLink.md docs/RelativeLink.md



# Testing
reviewCode:
	sourcery review mkdoxy --in-place

install-dev:
	python3 -m pip install --force --editable .

# Documentation
docs-serve: fixRelativeLinkDocs
	mkdocs serve

docs-build: fixRelativeLinkDocs
	mkdocs build