"""Tests for install.sh.

Runs the installer against temporary directories and verifies behavior.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALL_SCRIPT = REPO_ROOT / "install.sh"


def run_installer(target_dir: Path, *args: str) -> subprocess.CompletedProcess:
    bash = shutil.which("bash")
    if bash is None:
        pytest.skip("bash not available on PATH")
    return subprocess.run(
        [bash, str(INSTALL_SCRIPT), *args],
        cwd=str(target_dir),
        capture_output=True,
        text=True,
    )


def test_install_script_exists() -> None:
    assert INSTALL_SCRIPT.exists(), f"Missing: {INSTALL_SCRIPT}"


def test_install_to_empty_directory(tmp_path: Path) -> None:
    """Installer copies template content to an empty target."""
    result = run_installer(tmp_path)
    assert result.returncode == 0, (
        f"Install should succeed.\nStdout:\n{result.stdout}\nStderr:\n{result.stderr}"
    )
    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / ".claude" / "memory" / "MEMORY.md").exists()
    assert (tmp_path / ".claude" / "memory" / "_examples" / "decision_example.md").exists()
    assert (tmp_path / ".claude" / "memory" / "decisions" / ".gitkeep").exists()


def test_install_refuses_overwrite_without_force(tmp_path: Path) -> None:
    """Installer refuses if CLAUDE.md already exists."""
    (tmp_path / "CLAUDE.md").write_text("pre-existing", encoding="utf-8")
    result = run_installer(tmp_path)
    assert result.returncode != 0
    assert "refusing to overwrite" in result.stderr.lower()
    assert (tmp_path / "CLAUDE.md").read_text(encoding="utf-8") == "pre-existing"


def test_install_force_overwrites_claude_md(tmp_path: Path) -> None:
    """--force overwrites an existing CLAUDE.md."""
    (tmp_path / "CLAUDE.md").write_text("pre-existing", encoding="utf-8")
    result = run_installer(tmp_path, "--force")
    assert result.returncode == 0, f"stderr:\n{result.stderr}"
    assert (tmp_path / "CLAUDE.md").read_text(encoding="utf-8").startswith("# <PROJECT_NAME>")


def test_install_force_overwrites_claude_dir(tmp_path: Path) -> None:
    """--force replaces an existing .claude/ directory entirely."""
    stale = tmp_path / ".claude" / "stale-file"
    stale.parent.mkdir(parents=True)
    stale.write_text("stale", encoding="utf-8")
    result = run_installer(tmp_path, "--force")
    assert result.returncode == 0, f"stderr:\n{result.stderr}"
    assert not stale.exists(), "stale file should be wiped by --force"
    assert (tmp_path / ".claude" / "memory" / "MEMORY.md").exists()


def test_install_warns_when_not_git_repo(tmp_path: Path) -> None:
    """Warning issued when target is not a git repo, but install proceeds."""
    result = run_installer(tmp_path)
    assert result.returncode == 0
    assert "does not look like a git repo" in result.stderr.lower()


def test_install_help() -> None:
    """--help exits 0 and prints usage."""
    result = subprocess.run(
        [shutil.which("bash") or "bash", str(INSTALL_SCRIPT), "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Usage:" in result.stdout


def test_install_rejects_unknown_arg(tmp_path: Path) -> None:
    """Unknown flag exits non-zero with an error message."""
    result = run_installer(tmp_path, "--bogus")
    assert result.returncode != 0
    assert "unknown argument" in result.stderr.lower()
