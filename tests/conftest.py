"""Shared pytest fixtures and helpers."""
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def protocol_doc(repo_root: Path) -> Path:
    return repo_root / "docs" / "tool-protocol.md"


@pytest.fixture(scope="session")
def claude_template(repo_root: Path) -> Path:
    return repo_root / "template" / "CLAUDE.md"
