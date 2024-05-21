# Makefile

# ------------------------ #
#          Serve           #
# ------------------------ #

serve-local:
	@python -m stompy.main

# ------------------------ #
#          Build           #
# ------------------------ #

install:
	@pip install --verbose -e .
.PHONY: install

install-dev:
	@pip install --verbose -e '.[dev]'
.PHONY: install

build-ext:
	@python setup.py build_ext --inplace
.PHONY: build-ext

clean:
	rm -rf build dist *.so **/*.so **/*.pyi **/*.pyc **/*.pyd **/*.pyo **/__pycache__ *.egg-info .eggs/ .ruff_cache/
.PHONY: clean

# ------------------------ #
#       Static Checks      #
# ------------------------ #

py-files := $(shell find . -name '*.py')

format:
	@black $(py-files)
	@ruff format $(py-files)
.PHONY: format

static-checks:
	@black --diff --check $(py-files)
	@ruff check $(py-files)
	@mypy --install-types --non-interactive $(py-files)
.PHONY: lint

# ------------------------ #
#        Unit tests        #
# ------------------------ #

test:
	python -m pytest
.PHONY: test
