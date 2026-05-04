#!/usr/bin/env bash
# lint-template.sh — Verify that a repo applied the context-template correctly.
#
# Usage: lint-template.sh [DIRECTORY]
#
# Exit codes:
#   0  All checks pass.
#   1  One or more issues found.
#
# Checks (all run; the script reports every issue before exiting):
#   1. CLAUDE.md exists in the target.
#   2. CLAUDE.md has no unfilled placeholders (e.g. <PROJECT_NAME>, <YOUR_*>, <TBD>).
#   3. .claude/memory/MEMORY.md exists.
#   4. Every .md under .claude/memory/ (except _examples/ and MEMORY.md itself)
#      starts with YAML frontmatter (first line is '---').
#   5. Files referenced by MEMORY.md exist on disk.
#   6. (Warning, not error) MEMORY.md is < 200 lines.

set -euo pipefail

if [ "${BASH_VERSINFO[0]:-0}" -lt 4 ]; then
  echo "ERROR: lint-template.sh requires bash 4 or later." >&2
  echo "On macOS the default /bin/bash is 3.2 — install bash 4+ via Homebrew: brew install bash" >&2
  exit 2
fi

TARGET="${1:-.}"
ERRORS=0

err() {
  echo "ERROR: $*" >&2
  ERRORS=$((ERRORS + 1))
}

CLAUDE_MD="$TARGET/CLAUDE.md"
MEM_DIR="$TARGET/.claude/memory"
MEMORY_INDEX="$MEM_DIR/MEMORY.md"

# 1. CLAUDE.md must exist.
if [ ! -f "$CLAUDE_MD" ]; then
  err "$CLAUDE_MD not found"
fi

# 2. No unfilled placeholders in CLAUDE.md.
PLACEHOLDER_PATTERN='<(PROJECT_NAME|YOUR_[A-Z_]+|TBD|TODO|FILL_IN|REPLACE_ME)>'
if [ -f "$CLAUDE_MD" ]; then
  if grep -qE "$PLACEHOLDER_PATTERN" "$CLAUDE_MD"; then
    err "$CLAUDE_MD has unfilled placeholders:"
    grep -nE "$PLACEHOLDER_PATTERN" "$CLAUDE_MD" | sed 's/^/  /' >&2
  fi
fi

# 3. MEMORY.md must exist.
if [ ! -f "$MEMORY_INDEX" ]; then
  err "$MEMORY_INDEX not found"
fi

# 4. Frontmatter check on memory files (skip _examples/ and MEMORY.md).
if [ -d "$MEM_DIR" ]; then
  while IFS= read -r -d '' f; do
    case "$f" in
      */_examples/*) continue ;;
    esac
    if [ "$(realpath "$f" 2>/dev/null || readlink -f "$f" 2>/dev/null || echo "$f")" = \
         "$(realpath "$MEMORY_INDEX" 2>/dev/null || readlink -f "$MEMORY_INDEX" 2>/dev/null || echo "$MEMORY_INDEX")" ]; then
      continue
    fi
    first_line=$(head -n 1 "$f" 2>/dev/null || true)
    if [ "$first_line" != "---" ]; then
      err "$f: missing frontmatter (first line should be '---', got '$first_line')"
    fi
  done < <(find "$MEM_DIR" -type f -name '*.md' -print0)
fi

# 5. Cross-check MEMORY.md links against actual files on disk.
#    Strip backtick code spans first (so format examples inside `...` are ignored).
if [ -f "$MEMORY_INDEX" ]; then
  # Extract markdown links: [text](path.md), excluding those inside `code spans`.
  stripped=$(sed 's/`[^`]*`//g' "$MEMORY_INDEX")
  mapfile -t refs < <(echo "$stripped" | grep -oE '\]\([^)]+\.md\)' | sed 's/^\](//; s/)$//')
  for ref in "${refs[@]:-}"; do
    [ -z "$ref" ] && continue
    if [ ! -f "$MEM_DIR/$ref" ]; then
      err "$MEMORY_INDEX references file that does not exist: $ref"
    fi
  done
fi

# 6. Soft warning on MEMORY.md size.
if [ -f "$MEMORY_INDEX" ]; then
  lines=$(wc -l < "$MEMORY_INDEX")
  if [ "$lines" -gt 200 ]; then
    echo "WARNING: $MEMORY_INDEX has $lines lines (recommended < 200)" >&2
  fi
fi

if [ "$ERRORS" -gt 0 ]; then
  echo "" >&2
  echo "Found $ERRORS issue(s)" >&2
  exit 1
fi

echo "✓ Template lint passed for $TARGET"
exit 0
