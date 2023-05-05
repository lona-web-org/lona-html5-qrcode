SHELL=/bin/bash
PYTHON=python3

DIST_ROOT=lona_html5_qrcode/static/lona-html5-qrcode/dist

PYTHON_ENV_ROOT=envs
PYTHON_DEV_ENV=$(PYTHON_ENV_ROOT)/$(PYTHON)-dev
PYTHON_PACKAGING_ENV=$(PYTHON_ENV_ROOT)/$(PYTHON)-packaging


.PHONY: all clean npm-dependencies shell python-shell test-script dist _release

all: | test-script

clean:
	rm -rf node_modules
	rm -rf $(PYTHON_ENV_ROOT)

# npm #########################################################################
node_modules: package.json
	npm install

npm-dependencies: | node_modules
	rm -rf $(DIST_ROOT)
	mkdir -p $(DIST_ROOT)

	cp node_modules/html5-qrcode/html5-qrcode.min.js $(DIST_ROOT)
	cp node_modules/html5-qrcode/LICENSE $(DIST_ROOT)

# python ######################################################################
$(PYTHON_DEV_ENV): pyproject.toml
	rm -rf $(PYTHON_DEV_ENV) && \
	$(PYTHON) -m venv $(PYTHON_DEV_ENV) && \
	. $(PYTHON_DEV_ENV)/bin/activate && \
	pip install pip --upgrade && \
	pip install -e .[dev]

$(PYTHON_PACKAGING_ENV): pyproject.toml
	rm -rf $(PYTHON_PACKAGING_ENV) && \
	$(PYTHON) -m venv $(PYTHON_PACKAGING_ENV) && \
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	pip install --upgrade pip && \
	pip install .[packaging]

# helper
shell: $(PYTHON_DEV_ENV)
	. $(PYTHON_DEV_ENV)/bin/activate && \
	/bin/bash

python-shell: $(PYTHON_DEV_ENV)
	. $(PYTHON_DEV_ENV)/bin/activate && \
	rlpython

# tests
test-script: $(PYTHON_DEV_ENV)
	. $(PYTHON_DEV_ENV)/bin/activate && \
	$(PYTHON) test-script/test_script.py $(args)

# packaging
dist: $(PYTHON_PACKAGING_ENV)
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	rm -rf dist *.egg-info && \
	python -m build

_release: dist
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	twine upload --config-file ~/.pypirc.fscherf dist/*
