#!/usr/bin/env python3
"""Offline tests for repo-forge."""

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

import forge


class TestForge(unittest.TestCase):
    """Test each supported scaffold and the command-line entry point."""

    def setUp(self):
        self.root = Path.cwd() / ".test-work" / self._testMethodName
        shutil.rmtree(self.root, ignore_errors=True)
        self.root.mkdir(parents=True)
        self.addCleanup(lambda: shutil.rmtree(self.root, ignore_errors=True))

    def assert_common_files(self, dest, language):
        self.assertTrue((dest / "README.md").exists())
        self.assertTrue((dest / ".gitignore").exists())
        self.assertTrue((dest / "LICENSE").exists())
        workflow = dest / ".github" / "workflows" / "ci.yml"
        self.assertTrue(workflow.exists())
        commands = {
            "python": "python -m unittest discover -s tests",
            "node": "npm test",
            "rust": "cargo test",
        }
        self.assertIn(commands[language], workflow.read_text(encoding="utf-8"))
        self.assertIn("MIT License", (dest / "LICENSE").read_text(encoding="utf-8"))
        self.assertNotIn("OR OTHERWISE OR OTHERWISE", (dest / "LICENSE").read_text(encoding="utf-8"))

    def test_generate_python_project(self):
        dest = self.root / "test-python"
        forge.generate_python_project("test-python", dest)

        self.assertTrue((dest / "test_python" / "__init__.py").exists())
        self.assertTrue((dest / "test_python" / "main.py").exists())
        self.assertTrue((dest / "test_python" / "__main__.py").exists())
        self.assertTrue((dest / "tests" / "test_main.py").exists())
        self.assertIn('packages = ["test_python"]', (dest / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertNotIn("name.replace", (dest / "pyproject.toml").read_text(encoding="utf-8"))
        self.assert_common_files(dest, "python")

        result = subprocess.run(
            [sys.executable, "-m", "test_python"],
            cwd=dest,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Hello from test-python", result.stdout)

    def test_generate_node_project(self):
        dest = self.root / "test-node"
        forge.generate_node_project("test-node", dest)

        self.assertTrue((dest / "src" / "index.js").exists())
        self.assertTrue((dest / "test" / "index.test.js").exists())
        package = json.loads((dest / "package.json").read_text(encoding="utf-8"))
        self.assertEqual(package["scripts"]["test"], "jest")
        self.assertIn("const { main }", (dest / "test" / "index.test.js").read_text(encoding="utf-8"))
        self.assert_common_files(dest, "node")

    def test_generate_rust_project(self):
        dest = self.root / "test-rust"
        forge.generate_rust_project("test-rust", dest)

        self.assertTrue((dest / "Cargo.toml").exists())
        self.assertTrue((dest / "src" / "main.rs").exists())
        self.assertIn("cargo test", (dest / "README.md").read_text(encoding="utf-8"))
        self.assert_common_files(dest, "rust")

    def test_cli_creates_named_project_under_destination(self):
        result = subprocess.run(
            [sys.executable, str(Path(forge.__file__).resolve()), "cli-project", "--dest", str(self.root)],
            capture_output=True,
            text=True,
            check=True,
        )

        project = self.root / "cli-project"
        self.assertTrue((project / "README.md").exists())
        self.assertIn(str(project.resolve()), result.stdout)
        self.assertFalse((self.root / "README.md").exists())

    def test_invalid_project_name_is_rejected(self):
        with self.assertRaises(ValueError):
            forge.generate_python_project("../outside", self.root / "project")

    def test_existing_license_is_preserved(self):
        dest = self.root / "preserve-license"
        dest.mkdir()
        license_text = "existing license\n"
        (dest / "LICENSE").write_text(license_text, encoding="utf-8")

        forge.generate_node_project("preserve-license", dest)

        self.assertEqual((dest / "LICENSE").read_text(encoding="utf-8"), license_text)

    def test_readmes_include_testing_and_ci(self):
        for language, generator in (
            ("python", forge.generate_python_project),
            ("node", forge.generate_node_project),
            ("rust", forge.generate_rust_project),
        ):
            with self.subTest(language=language):
                dest = self.root / language
                generator(f"sample-{language}", dest)
                readme = (dest / "README.md").read_text(encoding="utf-8")
                self.assertIn("## Testing", readme)
                self.assertIn("GitHub Actions", readme)


if __name__ == "__main__":
    unittest.main()
