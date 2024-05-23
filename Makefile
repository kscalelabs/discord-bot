# Makefile

# ------------------------ #
#          Serve           #
# ------------------------ #

serve-local:
	@python -m stompy.main

# ------------------------ #
#       Static Checks      #
# ------------------------ #

format:
	@black stompy tests
	@ruff check --fix stompy tests
.PHONY: format

static-checks:
	@black --diff --check stompy tests
	@ruff check stompy tests
	# @mypy --install-types --non-interactive stompy tests
.PHONY: lint

# ------------------------ #
#        Unit tests        #
# ------------------------ #

test:
	python -m pytest
.PHONY: test
