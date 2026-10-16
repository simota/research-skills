# Wire this repo into a skills directory, and keep it inside its budgets.
#
# The repo is the single source of truth: each research-* directory is symlinked
# individually into every installed CLI's skills directory (claude, codex,
# agy), so each of those directories keeps whatever else it already carries.

# The directory holding this Makefile, not the one make was started in, so
# `make -f /path/to/Makefile status` links the repo rather than the cwd.
REPO       := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
CLAUDE_DIR ?= $(HOME)/.claude/skills
CODEX_DIR  ?= $(HOME)/.codex/skills
AGY_DIR    ?= $(HOME)/.gemini/antigravity-cli/skills

# Every CLI reading a SKILL.md gets the same working tree. A host is only
# written to when it is installed here, and its own home — the parent of the
# skills directory — is what says so: judging by the skills directory itself
# would skip a host that has one but has never been given a skill.
HOST_DIRS  := $(CLAUDE_DIR) $(CODEX_DIR) $(AGY_DIR)

.DEFAULT_GOAL := help
.PHONY: help check validate test figures engines refute render hooks link unlink status

help:
	@echo "make check     validate + test + figures (what CI runs)"
	@echo "make validate  static rules over the corpus"
	@echo "make test      prove every rule and every figure check still fires"
	@echo "make figures   re-derive what the corpus claims about itself"
	@echo "make refute CLAIMS=f.json RUNNING=<engine>   put each claim to the engines that did not make it"
	@echo "make engines  ask each checker engine for one object; reports what is unreachable"
	@echo "make render    write the delivered blocks back into every SKILL.md"
	@echo "make hooks     install the pre-commit hook"
	@echo "make link      symlink the skills into claude / codex / agy"
	@echo "make unlink    remove those symlinks"
	@echo "make status    show what is linked"

check: validate test figures

validate:
	@python3 "$(REPO)/research-tools/validate.py"

test:
	@python3 "$(REPO)/research-tools/test_validate.py"
	@python3 "$(REPO)/research-tools/test_figures.py"

figures:
	@python3 "$(REPO)/research-tools/figures_check.py"

engines:
	@python3 "$(REPO)/research-tools/engine.py" --selftest

# RUNNING is stated, never defaulted: a default of claude on a codex run would
# exclude the wrong engine and let the maker refute its own claim.
refute:
	@test -n "$(CLAIMS)" && test -n "$(RUNNING)" || { \
		echo "usage: make refute CLAIMS=claims.json RUNNING=<claude|codex|agy>"; exit 2; }
	@python3 "$(REPO)/research-tools/refute.py" --running "$(RUNNING)" "$(CLAIMS)"

render:
	@python3 "$(REPO)/research-tools/render.py"

# git says where hooks live: `.git` is a file in a worktree, and core.hooksPath
# can move them anywhere.
hooks:
	@hooks=$$(cd "$(REPO)" && git rev-parse --git-path hooks) && \
		case "$$hooks" in /*) ;; *) hooks="$(REPO)/$$hooks";; esac && \
		mkdir -p "$$hooks" && \
		cp "$(REPO)/research-tools/githooks/pre-commit" "$$hooks/pre-commit" && \
		chmod +x "$$hooks/pre-commit" && \
		echo "pre-commit installed in $$hooks"

# A skill is a directory holding a SKILL.md, under skills/ where the plugin
# format expects it. The prefix alone is not the test: research-registry/ and
# research-tools/ share it and must never be installed.
SKILL_DIRS := $(patsubst $(REPO)/%/SKILL.md,%,$(wildcard $(REPO)/skills/research-*/SKILL.md))

link:
	@for dir in $(HOST_DIRS); do \
		if [ ! -d "$$(dirname "$$dir")" ]; then echo "skip $$dir (host not installed here)"; continue; fi; \
		mkdir -p "$$dir"; \
		echo "$$dir"; \
		for path in $(SKILL_DIRS); do \
			name=$$(basename "$$path"); target="$$dir/$$name"; \
			if [ -L "$$target" ] && [ "$$(readlink "$$target")" != "$(REPO)/$$path" ]; then \
				echo "  skip $$name (linked elsewhere: $$(readlink "$$target"))"; \
			elif [ -e "$$target" ] && [ ! -L "$$target" ]; then \
				echo "  skip $$name (a real path is already there)"; \
			else \
				ln -sfn "$(REPO)/$$path" "$$target"; echo "  link $$name"; \
			fi; \
		done; \
	done

# Only links this checkout made: a same-named skill linked from another
# checkout belongs to whoever put it there.
unlink:
	@for dir in $(HOST_DIRS); do \
		[ -d "$$dir" ] || continue; \
		echo "$$dir"; \
		for path in $(SKILL_DIRS); do \
			name=$$(basename "$$path"); target="$$dir/$$name"; \
			if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$(REPO)/$$path" ]; then \
				rm "$$target"; echo "  unlink $$name"; \
			elif [ -L "$$target" ]; then echo "  keep $$name (linked elsewhere)"; fi; \
		done; \
	done

status:
	@for dir in $(HOST_DIRS); do \
		echo "$$dir"; \
		for path in $(SKILL_DIRS); do \
			name=$$(basename "$$path"); target="$$dir/$$name"; \
			if [ -L "$$target" ] && [ "$$(readlink "$$target")" = "$(REPO)/$$path" ]; then \
				echo "  linked   $$name"; \
			elif [ -L "$$target" ]; then echo "  elsewhere $$name -> $$(readlink "$$target")"; \
			elif [ -e "$$target" ]; then echo "  occupied $$name (a real path)"; \
			else echo "  unlinked $$name"; fi; \
		done; \
	done
