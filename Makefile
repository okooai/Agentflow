.PHONY: shell test help requirements

# SHELL				   := /bin/bash

BASEDIR					= $(shell pwd)
-include ${BASEDIR}/.env

ENVIRONMENT			   ?= development

PROJECT					= agentflow

PROJDIR					= ${BASEDIR}/src/agentflow
TESTDIR					= ${BASEDIR}/tests
DOCSDIR					= ${BASEDIR}/docs

NOTEBOOKSDIR		   ?= ${DOCSDIR}/source/notebooks


PYTHONPATH		 	   ?= python

VIRTUAL_ENV			   ?= ${BASEDIR}/.venv
VENVBIN				   ?= ${VIRTUAL_ENV}/bin/

PYTHON				   ?= ${VENVBIN}python
IPYTHON					= ${VENVBIN}ipython
PIP					   ?= ${VENVBIN}pip
PYTEST				   ?= ${VENVBIN}pytest
TOX						= ${VENVBIN}tox
COVERALLS			   ?= ${VENVBIN}coveralls
DOCSTR_COVERAGE		   ?= ${VENVBIN}docstr-coverage
IPYTHON					= ${VENVBIN}ipython
PYLINT					= ${VENVBIN}pylint

JUPYTER					= ${VENVBIN}jupyter

DOCKER_COMPOSE			= ${VENVBIN}docker-compose
SAFETY					= ${VENVBIN}safety
PRECOMMIT				= ${VENVBIN}pre-commit
SPHINXBUILD				= ${VENVBIN}sphinx-build
SPHINXAUTOBUILD			= ${VENVBIN}sphinx-autobuild
TWINE					= ${VENVBIN}twine

DOCKER_TAG			   ?= latest

DOCKER_IMAGE		   ?= ${DOCKER_REGISTRY}/${DOCKER_USERNAME}/${PROJECT}
DOCKER_BUILDKIT		   ?= 1


SQLITE				   ?= sqlite


JOBS				   ?= $(shell $(PYTHON) -c "import multiprocessing as mp; print(mp.cpu_count())")
PYTHON_ENVIRONMENT      = $(shell $(PYTHON) -c "import sys;v=sys.version_info;print('py%s%s'%(v.major,v.minor))")

NULL					= /dev/null

define log
	$(eval CLEAR     = \033[0m)
	$(eval BOLD		 = \033[0;1m)
	$(eval INFO	     = \033[0;36m)
	$(eval SUCCESS   = \033[0;32m)

	$(eval BULLET 	 = "→")
	$(eval TIMESTAMP = $(shell date +%H:%M:%S))

	@printf "${BULLET} ${$1}[${TIMESTAMP}]${CLEAR} ${BOLD}$2${CLEAR}\n"
endef

define browse
	$(PYTHON) -c "import webbrowser as wb; wb.open('${$1}')"
endef

ifndef VERBOSE
.SILENT:
endif

.DEFAULT_GOAL 		   := help 

env: ## Create a Virtual Environment
ifneq (${VERBOSE},true)
	$(eval OUT = > /dev/null)
endif

	$(call log,INFO,Creating a Virtual Environment ${VIRTUAL_ENV} with Python - ${PYTHONPATH})
	@virtualenv $(VIRTUAL_ENV) -p $(PYTHONPATH) $(OUT)

info: ## Display Information
	@echo "Python Environment: ${PYTHON_ENVIRONMENT}"

upgrade-tools: # Upgrade pip, setuptools, wheel to latest
ifneq (${VERBOSE},true)
	$(eval OUT = > /dev/null)
endif
	$(PIP) install --upgrade pip setuptools wheel $(OUT)

requirements: ## Build Requirements
	$(call log,INFO,Building Requirements)
	@find $(BASEDIR)/requirements -maxdepth 1 -type f | grep -v 'jobs' | xargs awk '{print}' > $(BASEDIR)/requirements-dev.txt
	@find $(BASEDIR)/requirements -maxdepth 1 -type f | xargs awk '{print}' > $(BASEDIR)/requirements-jobs.txt
	@cat $(BASEDIR)/requirements/production.txt  > $(BASEDIR)/requirements.txt

install: clean info upgrade-tools requirements ## Install dependencies and module.
ifneq (${VERBOSE},true)
	$(eval OUT = > /dev/null)
endif

ifneq (${PIPCACHEDIR},)
	$(eval PIPCACHEDIR := --cache-dir $(PIPCACHEDIR))
endif

	$(call log,INFO,Installing Requirements)
ifeq (${ENVIRONMENT},test)
	$(PIP) install -r $(BASEDIR)/requirements-test.txt $(PIP_ARGS) $(OUT)
else
	$(PIP) install -r $(BASEDIR)/requirements-dev.txt  $(PIP_ARGS) $(OUT)
endif

# https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html#summary
# setup.py install is deprecated.
	$(call log,INFO,Installing ${PROJECT} (${ENVIRONMENT}))
ifeq (${ENVIRONMENT},development)

	$(PIP) install -e $(BASEDIR) $(OUT)
else
	$(PIP) install $(BASEDIR) $(OUT)
endif

	$(call log,SUCCESS,Installation Successful)

clean: ## Clean cache, build and other auto-generated files.
ifneq (${ENVIRONMENT},test)
	@clear

	$(call log,INFO,Cleaning Python Cache)
	@find $(BASEDIR) | grep -E "__pycache__|\.pyc|\.egg-info" | xargs rm -rf

	@rm -rf \
		$(BASEDIR)/*.egg-info \
		$(BASEDIR)/.pytest_cache \
		$(BASEDIR)/.tox \
		$(BASEDIR)/*.coverage \
		$(BASEDIR)/*.coverage.* \
		$(BASEDIR)/.coverage.* \
		$(BASEDIR)/htmlcov \
		$(BASEDIR)/dist \
		$(BASEDIR)/build \
		$(BASEDIR)/*.log \
		~/.config/$(PROJECT)

	$(call log,SUCCESS,Cleaning Successful)
else
	$(call log,SUCCESS,Nothing to clean)
endif

test: install ## Run tests.
	$(call log,INFO,Running Python Tests using $(JOBS) jobs.)
	$(TOX) $(ARGS)

coverage: install ## Run tests and display coverage.
ifeq (${ENVIRONMENT},development)
	$(eval IARGS := --cov-report html)
endif

	$(PYTEST) -s -n $(JOBS) --cov $(PROJDIR) $(IARGS) -vv $(ARGS)

ifeq (${ENVIRONMENT},development)
	$(call browse,file:///${BASEDIR}/htmlcov/index.html)
endif

doc-coverage: install ## Display documentation coverage.
	$(DOCSTR_COVERAGE) $(PROJDIR)

ifeq (${ENVIRONMENT},development)
	$(call browse,file:///${BASEDIR}/htmlcov/index.html)
endif

ifeq (${ENVIRONMENT},test)
	$(COVERALLS)
endif

shell: install ## Launch an IPython shell.
	clear
	
	$(call log,INFO,Launching Python Shell)
	$(IPYTHON) \
		--no-banner


dbshell:
	$(call log,INFO,Launching SQLite Shell)
	$(SQLITE) ~/.config/${PROJECT}/db.db


build: clean ## Build the Distribution.
	$(PYTHON) setup.py sdist bdist_wheel

pre-commit: ## Perform Pre-Commit Tasks.
	$(PRECOMMIT) run

docs: install ## Build Documentation
ifneq (${VERBOSE},true)
	$(eval OUT = > /dev/null)
endif

	
	$(call log,INFO,Building Notebooks)
	@find $(DOCSDIR)/source/notebooks -type f -name '*.ipynb' -not -path "*/.ipynb_checkpoints/*" | \
		xargs $(JUPYTER) nbconvert \
			--to notebook 		\
			--inplace 			\
			--execute 			\
			--ExecutePreprocessor.timeout=300
	

	$(call log,INFO,Building Documentation)
	$(SPHINXBUILD) $(DOCSDIR)/source $(DOCSDIR)/build $(OUT)

	$(call log,SUCCESS,Building Documentation Successful)

ifeq (${launch},true)
	$(call browse,file:///${DOCSDIR}/build/index.html)
endif

docs-serve: install ## Serve Documentation
	$(call log,INFO,Serving Documentation)
	$(SPHINXAUTOBUILD) $(DOCSDIR)/source $(DOCSDIR)/build

docker-pull: ## Pull Latest Docker Images
	$(call log,INFO,Pulling latest Docker Image)

	if [[ -d "${BASEDIR}/docker/files" ]]; then \
		for folder in `ls ${BASEDIR}/docker/files`; do \
			docker pull $(DOCKER_IMAGE):$$folder || true; \
		done; \
	fi

	@docker pull $(DOCKER_IMAGE):latest || true

docker-build: clean docker-pull requirements ## Build the Docker Image.
	$(call log,INFO,Building Docker Image)

	if [[ -f "${BASEDIR}/docker-compose.yml" ]]; then \
		$(DOCKER_COMPOSE) build; \
	fi

	if [[ -d "${BASEDIR}/docker/files" ]]; then \
		for folder in `ls ${BASEDIR}/docker/files`; do \
			docker build ${BASEDIR}/docker/files/$$folder --tag $(DOCKER_IMAGE):$$folder $(DOCKER_BUILD_ARGS) ; \
		done \
	fi

	@[[ -f "${BASEDIR}/Dockerfile" ]] && docker build $(BASEDIR) --tag $(DOCKER_IMAGE):$(DOCKER_TAG) $(DOCKER_BUILD_ARGS)

docker-test: clean ## Testing within Docker Image.
	$(call log,INFO,Building Docker Image)
	
	@docker run --rm -it $(DOCKER_IMAGE):$(DOCKER_TAG) "tox"

docker-push: ## Push Docker Image to Registry.
	@docker push $(DOCKER_IMAGE) --all-tags

docker-tox: clean ## Test using Docker Tox Image.
	$(call log,INFO,Running Tests using Docker Tox)
	$(eval TMPDIR := /tmp/$(PROJECT)-$(shell date +"%Y_%m_%d_%H_%M_%S"))

	@mkdir   $(TMPDIR)
	@cp -R . $(TMPDIR)

	@docker run --rm -v $(TMPDIR):/app themattrix/tox

	@rm -rf  $(TMPDIR)

bump: test ## Bump Version
	$(BUMPVERSION) \
		--current-version $(shell cat $(PROJDIR)/VERSION) \
		$(TYPE) \
		$(PROJDIR)/VERSION 

release: ## Create a Release
	$(PYTHON) setup.py sdist bdist_wheel

ifeq (${ENVIRONMENT},development)
	$(call log,WARN,Ensure your environment is in production mode.)
	$(TWINE) upload --repository-url https://test.pypi.org/legacy/   $(BASEDIR)/dist/* 
else
	$(TWINE) upload --repository-url https://upload.pypi.org/legacy/ $(BASEDIR)/dist/* 
endif

start: ## Start app.
	$(PYTHON) -m flask run


notebooks: ## Launch Notebooks
	$(JUPYTER) notebook --notebook-dir $(NOTEBOOKSDIR) $(ARGS)


lint: ## Perform Lint
	$(PYLINT) $(PROJDIR) --output-format=colorized

loc: ## Count Lines of Code
	$(call log,INFO,Counting Lines of Code)
	@find $(PROJDIR) -type f -name "*.py" | xargs wc -l | sort -n

help: ## Show help and exit.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)