# The documentation lives in the docs/ directory and is built with the
# Canonical Sphinx Stack. This top-level Makefile forwards every target to
# docs/, so that `make <target>` can be run from the repository root.
# Running the same commands from within docs/ is equivalent.

# The Sphinx virtualenv the Canonical Sphinx Stack creates in docs/.
DOCS_VENVDIR ?= docs/.venv

# Put it first so that "make" without argument is like "make help".
help:
	@$(MAKE) -C docs help

# `html` and `run` must also apply docs/_static/openapi-overlay.yaml to the
# generated Debarchive API spec, so local builds render the same
# examples-enriched spec Read the Docs publishes (see .readthedocs.yaml's
# `pre_build` job). This can't be forwarded to docs/Makefile like other
# targets: oas-patch (pinned in docs/requirements.txt) is only installed into
# $(DOCS_VENVDIR) after `install` runs, so `install` runs first here to
# guarantee it's available.
html run:
	@$(MAKE) -C docs install
	$(DOCS_VENVDIR)/bin/python docs/scripts/apply_overlay.py
	@$(MAKE) -C docs $@

%:
	@$(MAKE) -C docs $@
