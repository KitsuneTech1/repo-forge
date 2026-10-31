#!/usr/bin/env python3
"""Tests for repo-forge."""

import unittest
import tempfile
from pathlib import Path
import forge


class TestForge(unittest.TestCase):
    """Test forge functionality."""

    def setUp(self):
        """Create temporary directory for tests."""
        self.temp_dir = tempfile.mkdtemp()

    def test_generate_python_project(self):
        """Test generating a Python project."""
        dest = Path(self.temp_dir) / 'test-python'
        forge.generate_python_project('test-python', dest)

        # Check key files exist
        self.assertTrue((dest / 'test_python' / '__init__.py').exists())
        self.assertTrue((dest / 'test_python' / 'main.py').exists())
        self.assertTrue((dest / 'tests' / 'test_main.py').exists())
        self.assertTrue((dest / 'pyproject.toml').exists())
        self.assertTrue((dest / 'README.md').exists())
        self.assertTrue((dest / '.gitignore').exists())

    def test_generate_node_project(self):
        """Test generating a Node.js project."""
        dest = Path(self.temp_dir) / 'test-node'
        forge.generate_node_project('test-node', dest)

        # Check key files exist
        self.assertTrue((dest / 'src' / 'index.js').exists())
        self.assertTrue((dest / 'test' / 'index.test.js').exists())
        self.assertTrue((dest / 'package.json').exists())
        self.assertTrue((dest / 'README.md').exists())
        self.assertTrue((dest / '.gitignore').exists())

    def test_generate_rust_project(self):
        """Test generating a Rust project."""
        dest = Path(self.temp_dir) / 'test-rust'
        forge.generate_rust_project('test-rust', dest)

        # Check key files exist
        self.assertTrue((dest / 'Cargo.toml').exists())
        self.assertTrue((dest / 'src' / 'main.rs').exists())
        self.assertTrue((dest / 'README.md').exists())
        self.assertTrue((dest / '.gitignore').exists())

    def test_python_readme_contains_name(self):
        """Test that Python README contains project name."""
        dest = Path(self.temp_dir) / 'my-project'
        forge.generate_python_project('my-project', dest)

        readme = (dest / 'README.md').read_text()
        self.assertIn('my-project', readme)

    def test_node_readme_contains_name(self):
        """Test that Node README contains project name."""
        dest = Path(self.temp_dir) / 'my-app'
        forge.generate_node_project('my-app', dest)

        readme = (dest / 'README.md').read_text()
        self.assertIn('my-app', readme)


if __name__ == '__main__':
    unittest.main()
