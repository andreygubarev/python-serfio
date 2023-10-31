MAKEFILE_DIR := $(realpath $(dir $(firstword $(MAKEFILE_LIST))))

.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: lint
lint: ## Lint Python Package
	python -m pycodestyle --max-line-length=120 serfio

.PHONY: build
build: ## Build Python Package
	python -m build --sdist --wheel

.PHONY: install
install: ## Install Python Package
	python -m pip install -e .

.PHONY: clean
clean: ## Clean Python Package
	rm -rf build dist *.egg-info
