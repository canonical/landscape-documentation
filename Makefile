# The documentation lives in the docs/ directory and is built with the
# Canonical Sphinx Stack. This top-level Makefile forwards every target to
# docs/, so that `make <target>` can be run from the repository root.
# Running the same commands from within docs/ is equivalent.

# Put it first so that "make" without argument is like "make help".
help:
	@$(MAKE) -C docs help

%:
	@$(MAKE) -C docs $@
