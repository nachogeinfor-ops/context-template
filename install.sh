#!/usr/bin/env bash
# install.sh — Apply the context-template to the current directory.
#
# Usage: bash <CONTEXT_TEMPLATE_PATH>/install.sh [--force]
#
# Copies template/CLAUDE.md and template/.claude/ from this repo to the
# current working directory. Without --force, refuses if either destination
# already exists. Warns (does not fail) if the target is not a git repo.

set -euo pipefail

if [ "${BASH_VERSINFO[0]:-0}" -lt 4 ]; then
  echo "ERROR: install.sh requires bash 4 or later." >&2
  echo "On macOS the default /bin/bash is 3.2 — install bash 4+ via Homebrew: brew install bash" >&2
  exit 2
fi

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
TEMPLATE_DIR="$SCRIPT_DIR/template"

if [ ! -d "$TEMPLATE_DIR" ]; then
  echo "ERROR: template/ directory not found at $TEMPLATE_DIR" >&2
  echo "This script must be run from inside the context-template repo." >&2
  exit 1
fi

FORCE=0
for arg in "$@"; do
  case "$arg" in
    -f|--force)
      FORCE=1
      ;;
    -h|--help)
      cat <<USAGE
Usage: bash install.sh [--force]

Apply the context-template to the current directory.
Copies template/CLAUDE.md and template/.claude/ to where you run this script.

Options:
  -f, --force    Overwrite existing CLAUDE.md / .claude/ if present.
  -h, --help     Show this help.
USAGE
      exit 0
      ;;
    *)
      echo "ERROR: unknown argument: $arg" >&2
      echo "Run 'bash install.sh --help' for usage." >&2
      exit 1
      ;;
  esac
done

TARGET=$(pwd)

if [ ! -d "$TARGET/.git" ]; then
  echo "WARNING: $TARGET does not look like a git repo." >&2
  echo "(Run 'git init' first if you intend to version-control the template.)" >&2
fi

CONFLICTS=()
[ -e "$TARGET/CLAUDE.md" ] && CONFLICTS+=("CLAUDE.md")
[ -e "$TARGET/.claude" ] && CONFLICTS+=(".claude/")

if [ "${#CONFLICTS[@]}" -gt 0 ] && [ "$FORCE" -eq 0 ]; then
  echo "ERROR: refusing to overwrite existing entries in $TARGET:" >&2
  for c in "${CONFLICTS[@]}"; do
    echo "  - $c" >&2
  done
  echo "" >&2
  echo "Re-run with --force to overwrite, or move/remove the conflicts manually." >&2
  exit 1
fi

cp "$TEMPLATE_DIR/CLAUDE.md" "$TARGET/CLAUDE.md"
if [ -d "$TARGET/.claude" ] && [ "$FORCE" -eq 1 ]; then
  rm -rf "$TARGET/.claude"
fi
cp -R "$TEMPLATE_DIR/.claude" "$TARGET/.claude"

cat <<NEXT
✓ Template applied to $TARGET

Next steps:
  1. Edit CLAUDE.md and replace every <YOUR_*> / <PROJECT_NAME> placeholder.
  2. Decide what goes in .claude/memory/ (see _examples/ for the format).
  3. Run the lint script to catch unfilled placeholders:
       bash $SCRIPT_DIR/scripts/lint-template.sh .
  4. Commit it. .claude/memory/ is meant to be version-controlled.
NEXT
