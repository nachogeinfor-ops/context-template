"""Tests for scripts/lint-template.sh.

Runs the script against fixtures and asserts exit codes.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
LINT_SCRIPT = REPO_ROOT / "scripts" / "lint-template.sh"
FIXTURES = REPO_ROOT / "tests" / "fixtures"


def run_lint(target: Path) -> subprocess.CompletedProcess:
    """Invoke the lint script via bash. Use bash explicitly so this works on Windows."""
    bash = shutil.which("bash")
    if bash is None:
        pytest.skip("bash not available on PATH")
    return subprocess.run(
        [bash, str(LINT_SCRIPT), str(target)],
        capture_output=True,
        text=True,
    )


def test_lint_script_exists() -> None:
    assert LINT_SCRIPT.exists(), f"Missing: {LINT_SCRIPT}"


def test_lint_passes_on_template_skeleton() -> None:
    """The skeleton itself contains placeholders by design — lint should FAIL.

    This documents the contract that the skeleton is NOT a valid filled-in
    template. Users must fill it in.
    """
    result = run_lint(REPO_ROOT / "template")
    assert result.returncode != 0, (
        f"Lint should fail on skeleton (placeholders present), got: {result.stdout}"
    )


@pytest.mark.parametrize(
    "case",
    ["missing-claude", "unfilled-placeholder", "broken-frontmatter", "index-mismatch"],
)
def test_lint_fails_on_bad_fixture(case: str) -> None:
    target = FIXTURES / "lint-bad" / case
    result = run_lint(target)
    assert result.returncode != 0, (
        f"Lint should fail on '{case}', got exit 0. Stdout:\n{result.stdout}\nStderr:\n{result.stderr}"
    )


@pytest.mark.parametrize(
    "fixture",
    ["sample-node-repo", "sample-python-repo"],
)
def test_lint_passes_on_sample_fixture(fixture: str) -> None:
    """The two filled-in sample fixtures must lint cleanly.

    They serve as proof that a fully-filled CLAUDE.md + .claude/memory/
    passes the lint script.
    """
    target = FIXTURES / fixture
    result = run_lint(target)
    assert result.returncode == 0, (
        f"Lint should pass on '{fixture}', got exit {result.returncode}.\n"
        f"Stdout:\n{result.stdout}\nStderr:\n{result.stderr}"
    )
