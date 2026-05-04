"""Verify that docs/tool-protocol.md and template/CLAUDE.md §8 describe the same contract.

The two files use different formats (table vs bullet list) but must agree on:
- The set of tool names.
- The ordered list of parameter names per tool.
- The optional/required marker (?) per parameter.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

# This set is the authoritative declaration of "the contract" — both files
# (tool-protocol.md and CLAUDE.md §8) must declare exactly these tools.
EXPECTED_TOOLS = {"search_repo", "recent_changes", "get_summary"}


def _parse_params(s: str) -> list[tuple[str, bool]]:
    """Parse a parameter string. Accepts both forms:
        'query: str, top_k?: int = 5, scope?: str'   (typed, from tool-protocol.md)
        'query, top_k?, scope?'                       (untyped, from CLAUDE.md §8)
    Returns a list of (name, is_optional).

    Limitation: splits on top-level commas only. A type annotation containing
    a comma (e.g. `dict[str, int]`) would produce spurious entries. None of
    the current tools use such types; if added, fix the splitter first.
    """
    s = s.strip()
    if not s:
        return []
    out: list[tuple[str, bool]] = []
    for part in s.split(","):
        part = part.strip()
        # Strip type annotation if present.
        head = part.split(":", 1)[0].strip()
        # Strip default value if present (untyped form).
        head = head.split("=", 1)[0].strip()
        is_optional = head.endswith("?")
        name = head.rstrip("?").strip()
        if name:
            out.append((name, is_optional))
    return out


def parse_protocol_doc(path: Path) -> dict[str, list[tuple[str, bool]]]:
    """Parse tool-protocol.md table rows: | `tool_name` | `(params)` | `Return` |"""
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"\|\s*`(\w+)`\s*\|\s*`\(([^)]*)\)`\s*\|")
    return {m.group(1): _parse_params(m.group(2)) for m in pattern.finditer(text)}


def parse_claude_template(path: Path) -> dict[str, list[tuple[str, bool]]]:
    """Parse CLAUDE.md §8 bullets: - **`tool_name(params)`** — ..."""
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(r"\*\*`(\w+)\(([^)]*)\)`\*\*")
    return {m.group(1): _parse_params(m.group(2)) for m in pattern.finditer(text)}


def test_protocol_doc_exists(protocol_doc: Path) -> None:
    assert protocol_doc.exists(), f"Missing: {protocol_doc}"


def test_claude_template_exists(claude_template: Path) -> None:
    assert claude_template.exists(), f"Missing: {claude_template}"


def test_protocol_doc_has_expected_tools(protocol_doc: Path) -> None:
    tools = parse_protocol_doc(protocol_doc)
    assert set(tools.keys()) == EXPECTED_TOOLS, (
        f"Protocol doc declares {set(tools.keys())}, expected {EXPECTED_TOOLS}"
    )


def test_claude_template_has_expected_tools(claude_template: Path) -> None:
    tools = parse_claude_template(claude_template)
    assert set(tools.keys()) == EXPECTED_TOOLS, (
        f"CLAUDE.md §8 declares {set(tools.keys())}, expected {EXPECTED_TOOLS}"
    )


@pytest.mark.parametrize("tool", sorted(EXPECTED_TOOLS))
def test_param_names_match(tool: str, protocol_doc: Path, claude_template: Path) -> None:
    p_tools = parse_protocol_doc(protocol_doc)
    t_tools = parse_claude_template(claude_template)
    assert tool in p_tools, f"Tool {tool!r} missing from {protocol_doc.name}"
    assert tool in t_tools, f"Tool {tool!r} missing from {claude_template.name}"
    p_names = [n for n, _ in p_tools[tool]]
    t_names = [n for n, _ in t_tools[tool]]
    assert p_names == t_names, (
        f"Tool {tool}: protocol params {p_names}, template params {t_names}"
    )


@pytest.mark.parametrize("tool", sorted(EXPECTED_TOOLS))
def test_optional_markers_match(tool: str, protocol_doc: Path, claude_template: Path) -> None:
    p_tools = parse_protocol_doc(protocol_doc)
    t_tools = parse_claude_template(claude_template)
    assert tool in p_tools, f"Tool {tool!r} missing from {protocol_doc.name}"
    assert tool in t_tools, f"Tool {tool!r} missing from {claude_template.name}"
    p_opt = [o for _, o in p_tools[tool]]
    t_opt = [o for _, o in t_tools[tool]]
    assert p_opt == t_opt, (
        f"Tool {tool}: protocol optionals {p_opt}, template optionals {t_opt}"
    )
