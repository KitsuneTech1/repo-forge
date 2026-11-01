#!/usr/bin/env python3
"""Generate a small starter repository with a working project baseline."""

import json
import re
import sys
from argparse import ArgumentParser
from pathlib import Path


LICENSE_TEXT = """MIT License

Copyright (c) 2026 Author

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


CI_FILES = {
    "python": """name: CI

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.x"
      - run: python -m unittest discover -s tests
""",
    "node": """name: CI

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20.x"
      - run: npm install
      - run: npm test
""",
    "rust": """name: CI

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cargo test
""",
}


WINDOWS_DEVICE_NAMES = frozenset(
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{number}" for number in range(1, 10)}
    | {f"LPT{number}" for number in range(1, 10)}
)


def _reject_symlink_components(path):
    """Reject symlinked path components before any generated file is touched."""
    path = Path(path)
    for component in (path, *path.parents):
        if component.is_symlink():
            raise ValueError(f"refusing to use symbolic link path: {path}")


def _ensure_directory(path, *, parents=False):
    """Create a real directory without following an existing symlink."""
    path = Path(path)
    _reject_symlink_components(path)
    if path.exists() and not path.is_dir():
        raise ValueError(f"expected a directory: {path}")
    path.mkdir(parents=parents, exist_ok=True)
    _reject_symlink_components(path)


def _write_file(path, content):
    """Write a regular generated file without following an existing symlink."""
    path = Path(path)
    _reject_symlink_components(path)
    if path.exists() and not path.is_file():
        raise ValueError(f"expected a regular file: {path}")
    path.write_text(content, encoding="utf-8")


def _has_existing_license(dest):
    """Return whether a usable license file already exists in the destination."""
    license_path = Path(dest) / "LICENSE"
    _reject_symlink_components(license_path)
    if not license_path.exists():
        return False
    if not license_path.is_file():
        raise ValueError(f"expected LICENSE to be a regular file: {license_path}")
    return True


def _validate_project_name(name):
    """Reject names that could escape the destination or break generated code."""
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", name):
        raise ValueError(
            "project name must start with a letter or number and contain only "
            "letters, numbers, hyphens, and underscores"
        )
    if name.upper() in WINDOWS_DEVICE_NAMES:
        raise ValueError(f"project name is a reserved Windows device name: {name}")


def _write_common_files(dest, language, existing_license):
    """Write files shared by every generated repository."""
    workflow_dir = dest / ".github" / "workflows"
    _ensure_directory(workflow_dir, parents=True)
    _write_file(workflow_dir / "ci.yml", CI_FILES[language])

    if not existing_license:
        _write_file(dest / "LICENSE", LICENSE_TEXT)


def generate_python_project(name, dest):
    """Generate a Python project scaffold."""
    _validate_project_name(name)
    dest = Path(dest)
    _ensure_directory(dest, parents=True)
    existing_license = _has_existing_license(dest)
    module_name = name.replace("-", "_")

    src_dir = dest / module_name
    _ensure_directory(src_dir)
    _write_file(
        src_dir / "__init__.py",
        f'"""{name} package."""\n\n__version__ = "0.1.0"\n',
    )
    _write_file(
        src_dir / "main.py",
        f'''#!/usr/bin/env python3
"""Main module for {name}."""


def main():
    """Print the starter greeting."""
    print("Hello from {name}")


if __name__ == "__main__":
    main()
''',
    )
    _write_file(
        src_dir / "__main__.py",
        "from .main import main\n\n\nif __name__ == \"__main__\":\n    main()\n",
    )

    tests_dir = dest / "tests"
    _ensure_directory(tests_dir)
    _write_file(tests_dir / "__init__.py", "")
    _write_file(
        tests_dir / "test_main.py",
        f'''"""Tests for {name}."""

import importlib
import io
import unittest
from contextlib import redirect_stdout


class TestMain(unittest.TestCase):
    """Test the generated entry point."""

    def test_main_is_callable(self):
        main = importlib.import_module("{module_name}.main").main

        self.assertTrue(callable(main))

    def test_main_prints_greeting(self):
        main = importlib.import_module("{module_name}.main").main
        output = io.StringIO()

        with redirect_stdout(output):
            main()

        self.assertEqual(output.getvalue(), "Hello from {name}\\n")


if __name__ == "__main__":
    unittest.main()
''',
    )

    license_metadata = '{file = "LICENSE"}' if existing_license else '{text = "MIT"}'
    _write_file(
        dest / "pyproject.toml",
        f'''[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{name}"
version = "0.1.0"
description = ""
authors = [{{"name": "Author"}}]
readme = "README.md"
license = {license_metadata}
requires-python = ">=3.8"

[tool.setuptools]
packages = ["{module_name}"]
''',
    )
    _write_file(
        dest / ".gitignore",
        """__pycache__/\n*.py[cod]\n*$py.class\n*.so\n.Python\nbuild/\ndevelop-eggs/\ndist/\ndownloads/\neggs/\n.eggs/\nlib/\nlib64/\nparts/\nsdist/\nvar/\nwheels/\n*.egg-info/\n.installed.cfg\n*.egg\n.pytest_cache/\n.coverage\nhtmlcov/\n.venv\nvenv/\nENV/\n""",
    )
    license_section = "See LICENSE." if existing_license else "MIT License\n\nCopyright (c) 2026 Author"
    _write_file(
        dest / "README.md",
        f'''# {name}

Brief description of what this project does.

## Installation

```bash
pip install -e .
```

## Usage

```bash
python -m {module_name}
```

## Testing

```bash
python -m unittest discover -s tests
```

The same test command runs in GitHub Actions for pushes and pull requests.

## License

{license_section}
''',
    )
    _write_common_files(dest, "python", existing_license)


def generate_node_project(name, dest):
    """Generate a Node.js project scaffold."""
    _validate_project_name(name)
    dest = Path(dest)
    _ensure_directory(dest, parents=True)
    existing_license = _has_existing_license(dest)

    src_dir = dest / "src"
    _ensure_directory(src_dir)
    _write_file(
        src_dir / "index.js",
        f'''/**
 * Main entry point for {name}
 */

function main() {{
    console.log("Hello from {name}");
}}

module.exports = {{ main }};

if (require.main === module) {{
    main();
}}
''',
    )

    test_dir = dest / "test"
    _ensure_directory(test_dir)
    _write_file(
        test_dir / "index.test.js",
        f'''const {{ main }} = require("../src/index.js");

describe("{name}", () => {{
    test("main function exists", () => {{
        expect(typeof main).toBe("function");
    }});

    test("main prints the greeting", () => {{
        const log = jest.spyOn(console, "log").mockImplementation(() => {{}});
        try {{
            main();
            expect(log).toHaveBeenCalledWith("Hello from {name}");
        }} finally {{
            log.mockRestore();
        }}
    }});
}});
''',
    )

    license_metadata = "SEE LICENSE IN LICENSE" if existing_license else "MIT"
    _write_file(
        dest / "package.json",
        json.dumps(
            {
                "name": name,
                "version": "0.1.0",
                "description": "",
                "main": "src/index.js",
                "scripts": {"test": "jest --runInBand", "start": "node src/index.js"},
                "author": "",
                "license": license_metadata,
                "devDependencies": {"jest": "^29.0.0"},
            },
            indent=2,
        )
        + "\n",
    )
    _write_file(
        dest / ".gitignore",
        """node_modules/\n.npm\n.DS_Store\ndist/\nbuild/\n.env\n.env.local\n*.log\ncoverage/\n.vscode/\n.idea/\n""",
    )
    license_section = "See LICENSE." if existing_license else "MIT License\n\nCopyright (c) 2026 Author"
    _write_file(
        dest / "README.md",
        f'''# {name}

Brief description of what this project does.

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```

## Testing

```bash
npm test
```

The same test command runs in GitHub Actions for pushes and pull requests.

## License

{license_section}
''',
    )
    _write_common_files(dest, "node", existing_license)


def generate_rust_project(name, dest):
    """Generate a Rust project scaffold."""
    _validate_project_name(name)
    dest = Path(dest)
    _ensure_directory(dest, parents=True)
    existing_license = _has_existing_license(dest)

    license_metadata = 'license-file = "LICENSE"' if existing_license else 'license = "MIT"'
    _write_file(
        dest / "Cargo.toml",
        f'''[package]
name = "{name}"
version = "0.1.0"
edition = "2021"
authors = ["Author"]
{license_metadata}

[dependencies]

[dev-dependencies]
''',
    )
    src_dir = dest / "src"
    _ensure_directory(src_dir)
    _write_file(
        src_dir / "main.rs",
        f'''/// Main function for {name}
fn main() {{
    println!("{{}}", greeting());
}}

fn greeting() -> &'static str {{
    "Hello from {name}"
}}

#[cfg(test)]
mod tests {{
    use super::*;

    #[test]
    fn it_works() {{
        assert_eq!(greeting(), "Hello from {name}");
    }}
}}
''',
    )
    _write_file(
        dest / ".gitignore",
        """/target/\n**/*.rs.bk\nCargo.lock\n.DS_Store\n.vscode/\n.idea/\n""",
    )
    license_section = "See LICENSE." if existing_license else "MIT License\n\nCopyright (c) 2026 Author"
    _write_file(
        dest / "README.md",
        f'''# {name}

Brief description of what this project does.

## Build

```bash
cargo build --release
```

## Testing

```bash
cargo test
```

The same test command runs in GitHub Actions for pushes and pull requests.

## License

{license_section}
''',
    )
    _write_common_files(dest, "rust", existing_license)


def main():
    """Parse arguments and generate a project directory."""
    parser = ArgumentParser(description="Generate a starter repository.")
    parser.add_argument("name", help="Project name")
    parser.add_argument(
        "--lang",
        choices=["python", "node", "rust"],
        default="python",
        help="Programming language (default: python)",
    )
    parser.add_argument(
        "--dest",
        default=".",
        help="Parent directory for the generated project (default: current directory)",
    )

    args = parser.parse_args()
    try:
        _validate_project_name(args.name)
    except ValueError as error:
        parser.error(str(error))

    dest = Path(args.dest) / args.name
    generators = {
        "python": generate_python_project,
        "node": generate_node_project,
        "rust": generate_rust_project,
    }
    generators[args.lang](args.name, dest)

    print(f"Generated {args.lang} project: {args.name}")
    print(f"Location: {dest.resolve()}")


if __name__ == "__main__":
    sys.exit(main())
