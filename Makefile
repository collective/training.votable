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

all: build-plone-6.0

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
.PHONY: help
help: ## This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


venv:
	python$(version) -m venv venv
	venv/bin/python -m pip install pip==23.0.1
	venv/bin/pip install -U pip wheel mxdev


requirements-mxdev.txt: venv  ## pip
	venv/bin/mxdev -c mx.ini
	venv/bin/pip install -r requirements-mxdev.txt


.PHONY: Build Plone 6.0
build-plone-6.0: requirements-mxdev.txt  ## Build Plone 6.0
	venv/bin/cookiecutter -f --no-input --config-file instance.yml https://github.com/plone/cookiecutter-zope-instance


.PHONY: Test
test:  ## Test
	@${PYBIN}zope-testrunner --auto-color --auto-progress --test-path=${ADDONFOLDER}
