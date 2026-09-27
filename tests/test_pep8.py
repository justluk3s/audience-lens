import ast
import glob
import os
import unittest


class TestPEP8Compliance(unittest.TestCase):
    """Automated PEP8 hygiene and style verification for audience-lens."""

    @classmethod
    def setUpClass(cls):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        src_dir = os.path.join(project_root, "src")
        cls.python_files = sorted(glob.glob(f"{src_dir}/**/*.py", recursive=True))

    def test_python_files_found(self):
        """Ensure there are python files found to test."""
        self.assertGreater(len(self.python_files), 0, "No python files found under src/")

    def test_no_syntax_errors(self):
        """All files must parse without SyntaxError."""
        for path in self.python_files:
            with self.subTest(file=path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                try:
                    ast.parse(content, filename=path)
                except SyntaxError as e:
                    self.fail(f"Syntax error in {path}:{e.lineno}: {e.msg}")

    def test_no_blank_line_at_file_start(self):
        """PEP8: Non-empty files should not start with an extraneous blank line."""
        for path in self.python_files:
            with self.subTest(file=path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                if not content.strip():
                    continue
                first_line = content.splitlines()[0]
                self.assertNotEqual(
                    first_line.strip(),
                    "",
                    f"{path}: File starts with an extraneous blank line",
                )

    def test_single_trailing_newline_at_eof(self):
        """PEP8 (W292 / W391): Non-empty files must end with exactly one trailing newline."""
        for path in self.python_files:
            with self.subTest(file=path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                if not content:
                    continue
                self.assertTrue(
                    content.endswith("\n"),
                    f"{path}: Missing trailing newline at EOF (W292)",
                )
                self.assertFalse(
                    content.endswith("\n\n"),
                    f"{path}: Extraneous blank line(s) at EOF (W391)",
                )

    def test_no_trailing_whitespace(self):
        """PEP8 (W291 / W293): No trailing whitespace on any line."""
        for path in self.python_files:
            with self.subTest(file=path):
                with open(path, "r", encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        stripped = line.rstrip("\r\n")
                        self.assertEqual(
                            stripped,
                            stripped.rstrip(),
                            f"{path}:{line_num}: Trailing whitespace detected",
                        )

    def test_top_level_function_blank_lines(self):
        """PEP8 (E302 / E303): Top-level functions must be preceded by exactly 2 blank lines."""
        for path in self.python_files:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if not content.strip():
                continue

            try:
                tree = ast.parse(content, filename=path)
            except SyntaxError:
                continue

            lines = content.splitlines()

            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    lineno = node.lineno  # 1-indexed

                    # If it's the very first line of the file, E302 does not apply
                    if lineno <= 2:
                        continue

                    # Count how many preceding lines are completely blank
                    blank_count = 0
                    idx = lineno - 2  # 0-indexed line immediately before
                    while idx >= 0 and lines[idx].strip() == "":
                        blank_count += 1
                        idx -= 1

                    with self.subTest(file=path, function=node.name, line=lineno):
                        if blank_count < 2:
                            self.fail(
                                f"{path}:{lineno} (E302): expected 2 blank lines before "
                                f"'{node.name}', found {blank_count}"
                            )
                        elif blank_count > 2:
                            self.fail(
                                f"{path}:{lineno} (E303): too many blank lines ({blank_count}) "
                                f"before '{node.name}', expected 2"
                            )


if __name__ == "__main__":
    unittest.main()
