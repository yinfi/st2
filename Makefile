OS := $(shell uname)

# We separate the OSX X and Linux virtualenvs so we can run in a Docker
# container (st2devbox) while doing things on our host Mac machine
ifeq ($(OS),Darwin)
	VIRTUALENV_DIR ?= virtualenv-osx
else
	VIRTUALENV_DIR ?= virtualenv
endif

PYTHON_VERSION ?= python2.7


# Target for debugging Makefile variable assembly
.PHONY: play
play:
	@echo COVERAGE_GLOBS=$(COVERAGE_GLOBS_QUOTED)
	@echo
	@echo COMPONENTS=$(COMPONENTS)
	@echo
	@echo COMPONENTS_WITH_RUNNERS=$(COMPONENTS_WITH_RUNNERS)
	@echo
	@echo COMPONENTS_WITH_RUNNERS_WITHOUT_MISTRAL_RUNNER=$(COMPONENTS_WITH_RUNNERS_WITHOUT_MISTRAL_RUNNER)
	@echo
	@echo COMPONENTS_TEST=$(COMPONENTS_TEST)
	@echo
	@echo COMPONENTS_TEST_COMMA=$(COMPONENTS_TEST_COMMA)
	@echo
	@echo COMPONENTS_TEST_DIRS=$(COMPONENTS_TEST_DIRS)
	@echo
	@echo COMPONENTS_TEST_MODULES=$(COMPONENTS_TEST_MODULES)
	@echo
	@echo COMPONENTS_TEST_MODULES_COMMA=$(COMPONENTS_TEST_MODULES_COMMA)
	@echo
	@echo COMPONENTS_TEST_WITHOUT_MISTRAL_RUNNER=$(COMPONENTS_TEST_WITHOUT_MISTRAL_RUNNER)
	@echo
	@echo COMPONENT_PYTHONPATH=$(COMPONENT_PYTHONPATH)
	@echo
	@echo TRAVIS_PULL_REQUEST=$(TRAVIS_PULL_REQUEST)
	@echo
	@echo TRAVIS_EVENT_TYPE=$(TRAVIS_EVENT_TYPE)
	@echo
	@echo NOSE_OPTS=$(NOSE_OPTS)
	@echo
	@echo ENABLE_COVERAGE=$(ENABLE_COVERAGE)
	@echo
	@echo NOSE_COVERAGE_FLAGS=$(NOSE_COVERAGE_FLAGS)
	@echo
	@echo NOSE_COVERAGE_PACKAGES=$(NOSE_COVERAGE_PACKAGES)
	@echo
	@echo INCLUDE_TESTS_IN_COVERAGE=$(INCLUDE_TESTS_IN_COVERAGE)
	@echo

.PHONY: clean
clean:
	invoke clean

.PHONY: distclean
distclean: clean
	@echo
	@echo "==================== distclean ===================="
	@echo
	rm -rf $(VIRTUALENV_DIR)

# Optional virtualenv wrapper
ifneq ($(VIRTUALENV_DIR),virtualenv)
virtualenv: $(VIRTUALENV_DIR)
endif

$(VIRTUALENV_DIR):
	# Note: We pass --no-download flag to make sure version of pip which we install (9.0.1) is used
	# instead of latest version being downloaded from PyPi
	virtualenv --python=$(PYTHON_VERSION) --no-site-packages $(VIRTUALENV_DIR) --no-download

	@echo
	@echo "==================== requirements ===================="
	@echo
	# Make sure we use latest version of pip which is 19
	$(VIRTUALENV_DIR)/bin/pip --version
	$(VIRTUALENV_DIR)/bin/pip install --upgrade "pip>=19.0,<20.0"
	$(VIRTUALENV_DIR)/bin/pip install --upgrade "virtualenv==16.6.0" # Required for packs.install in dev envs

virtualenv-components:
	virtualenv --python=$(PYTHON_VERSION) --no-site-packages $@ --no-download

virtualenv-st2client:
	virtualenv --python=$(PYTHON_VERSION) --no-site-packages $@ --no-download

$(VIRTUALENV_DIR)/bin/invoke: virtualenv
	$(VIRTUALENV_DIR)/bin/pip install invoke

invoke: $(VIRTUALENV_DIR)/bin/invoke

# https://stackoverflow.com/a/33018558
# Workaround to support all previous make targets
# This default target simply passes all targets on to invoke
.DEFAULT: invoke
	@. $(VIRTUALENV_DIR)/bin/activate; invoke $@
