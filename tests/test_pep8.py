import ast
import glob
import os
import pytest

# Find all python files under src/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
PYTHON_FILES = sorted(glob.glob(f"{SRC_DIR}/**/*.py", recursive=True))


def test_python_files_found():
    """Ensure there are python files found to test."""
    assert len(PYTHON_FILES) > 0, "No python files found under src/"


@pytest.mark.parametrize("path", PYTHON_FILES)
def test_no_syntax_errors(path):
    """All files must parse without SyntaxError."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        ast.parse(content, filename=path)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {path}:{e.lineno}: {e.msg}")


@pytest.mark.parametrize("path", PYTHON_FILES)
def test_no_blank_line_at_file_start(path):
    """PEP8: Non-empty files should not start with an extraneous blank line."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        return  # Allow completely empty __init__.py files

    first_line = content.splitlines()[0]
    assert first_line.strip() != "", f"{path}: File starts with an extraneous blank line"


@pytest.mark.parametrize("path", PYTHON_FILES)
def test_single_trailing_newline_at_eof(path):
    """PEP8 (W292 / W391): Non-empty files must end with exactly one trailing newline."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content:
        return

    assert content.endswith("\n"), f"{path}: Missing trailing newline at EOF (W292)"
    assert not content.endswith("\n\n"), f"{path}: Extraneous blank line(s) at EOF (W391)"


@pytest.mark.parametrize("path", PYTHON_FILES)
def test_no_trailing_whitespace(path):
    """PEP8 (W291 / W293): No trailing whitespace on any line."""
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            stripped = line.rstrip("\r\n")
            assert stripped == stripped.rstrip(), (
                f"{path}:{line_num}: Trailing whitespace detected"
            )


@pytest.mark.parametrize("path", PYTHON_FILES)
def test_top_level_function_blank_lines(path):
    """PEP8 (E302 / E303): Top-level functions must be preceded by exactly 2 blank lines."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        return

    try:
        tree = ast.parse(content, filename=path)
    except SyntaxError:
        return

    lines = content.splitlines()

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            lineno = node.lineno  # 1-indexed

            if lineno <= 2:
                continue

            blank_count = 0
            idx = lineno - 2
            while idx >= 0 and lines[idx].strip() == "":
                blank_count += 1
                idx -= 1

            assert blank_count >= 2, (
                f"{path}:{lineno} (E302): expected 2 blank lines before "
                f"'{node.name}', found {blank_count}"
            )
            assert blank_count <= 2, (
                f"{path}:{lineno} (E303): too many blank lines ({blank_count}) "
                f"before '{node.name}', expected 2"
            )
