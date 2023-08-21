SHELL := /bin/bash
CURRENT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

version = 3

# We like colors
# From: https://coderwall.com/p/izxssa/colored-makefile-for-golang-projects
RED=`tput setaf 1`
GREEN=`tput setaf 2`
RESET=`tput sgr0`
YELLOW=`tput setaf 3`

ADDONBASE=./
ADDONFOLDER=${ADDONBASE}src/
VENV_FOLDER=./venv
PYBIN=${VENV_FOLDER}/bin/

# See https://github.com/plone/code-quality
# Our configuration is in pyproject.toml.
CODE_QUALITY_VERSION=2.0.0
CURRENT_USER=$$(whoami)
USER_INFO=$$(id -u ${CURRENT_USER}):$$(id -g ${CURRENT_USER})
LINT=docker run --user="${USER_INFO}" --rm -v "$(PWD)":/github/workspace plone/code-quality:${CODE_QUALITY_VERSION} check
FORMAT=docker run --user="$(id -u $(whoami)):$(getent group $(whoami)|cut -d: -f3)" --rm -v "$(PWD)":/github/workspace plone/code-quality:${CODE_QUALITY_VERSION} format


all: build

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z0-9._-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

venv:
	python$(version) -m venv venv
	venv/bin/python -m pip install pip==23.0.1
	venv/bin/pip install -U pip wheel mxdev

requirements-mxdev.txt: venv # pip
	venv/bin/mxdev -c mx.ini
	venv/bin/pip install -r requirements-mxdev.txt

.PHONY: build
build: requirements-mxdev.txt ## Build Plone
	venv/bin/cookiecutter -f --no-input --config-file instance.yml https://github.com/plone/cookiecutter-zope-instance

.PHONY: pip
pip: ## Update Python venv
	venv/bin/mxdev -c mx.ini
	venv/bin/pip install -r requirements-mxdev.txt

.PHONY: Test
test:  ## Test
	venv/bin/pytest

.PHONY: test_quiet
test_quiet: ## Run tests removing deprecation warnings
	venv/bin/pytest --disable-warnings

.PHONY: lint
lint:  ## validate with isort, black, flake8, pyroma, zpretty
	@echo USER_INFO: $(USER_INFO)
	$(LINT)

.PHONY: format
format:  ## Format the codebase according to our standards
	@echo USER_INFO: $(USER_INFO)
	$(FORMAT)
