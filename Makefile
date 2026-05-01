.PHONY: install install-all check check-all help

# Defaults
SKILL ?=

help:
	@echo "Targets:"
	@echo "  make install SKILL=<name>   Sync skills/<name> and agents/<name>.md to ~/.claude/"
	@echo "  make install-all            Sync every skill and every agent to ~/.claude/"
	@echo "  make check SKILL=<name>     Diff-only; exits non-zero if ~/.claude is out of sync"
	@echo "  make check-all              Diff every skill and agent against ~/.claude (CI-friendly)"

install:
	@if [ -z "$(SKILL)" ]; then echo "usage: make install SKILL=<name>"; exit 2; fi
	@./scripts/install_to_claude.sh "$(SKILL)"

install-all:
	@./scripts/install_to_claude.sh --all

check:
	@if [ -z "$(SKILL)" ]; then echo "usage: make check SKILL=<name>"; exit 2; fi
	@./scripts/install_to_claude.sh --check "$(SKILL)"

check-all:
	@./scripts/install_to_claude.sh --check --all
