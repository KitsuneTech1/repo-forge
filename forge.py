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


def _validate_project_name(name):
    """Reject names that could escape the destination or break generated code."""
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", name):
        raise ValueError(
            "project name must start with a letter or number and contain only "
            "letters, numbers, hyphens, and underscores"
        )


def _write_common_files(dest, language):
    """Write files shared by every generated repository."""
    workflow_dir = dest / ".github" / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / "ci.yml").write_text(CI_FILES[language], encoding="utf-8")

    license_path = dest / "LICENSE"
    if not license_path.exists():
        license_path.write_text(LICENSE_TEXT, encoding="utf-8")


def generate_python_project(name, dest):
    """Generate a Python project scaffold."""
    _validate_project_name(name)
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    module_name = name.replace("-", "_")

    src_dir = dest / module_name
    src_dir.mkdir(exist_ok=True)
    (src_dir / "__init__.py").write_text(
        f'"""{name} package."""\n\n__version__ = "0.1.0"\n',
        encoding="utf-8",
    )
    (src_dir / "main.py").write_text(
        f'''#!/usr/bin/env python3
"""Main module for {name}."""


def main():
    """Print the starter greeting."""
    print("Hello from {name}")


if __name__ == "__main__":
    main()
''',
        encoding="utf-8",
    )
    (src_dir / "__main__.py").write_text(
        "from .main import main\n\n\nif __name__ == \"__main__\":\n    main()\n",
        encoding="utf-8",
    )

    tests_dir = dest / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / "__init__.py").write_text("", encoding="utf-8")
    (tests_dir / "test_main.py").write_text(
        f'''"""Tests for {name}."""

import unittest


class TestMain(unittest.TestCase):
    """Test the generated entry point."""

    def test_main_is_callable(self):
        from {module_name}.main import main

        self.assertTrue(callable(main))


if __name__ == "__main__":
    unittest.main()
''',
        encoding="utf-8",
    )

    (dest / "pyproject.toml").write_text(
        f'''[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{name}"
version = "0.1.0"
description = ""
authors = [{{"name": "Author", "email": "author@example.com"}}]
readme = "README.md"
license = {{text = "MIT"}}
requires-python = ">=3.8"

[tool.setuptools]
packages = ["{module_name}"]
''',
        encoding="utf-8",
    )
    (dest / ".gitignore").write_text(
        """__pycache__/\n*.py[cod]\n*$py.class\n*.so\n.Python\nbuild/\ndevelop-eggs/\ndist/\ndownloads/\neggs/\n.eggs/\nlib/\nlib64/\nparts/\nsdist/\nvar/\nwheels/\n*.egg-info/\n.installed.cfg\n*.egg\n.pytest_cache/\n.coverage\nhtmlcov/\n.venv\nvenv/\nENV/\n""",
        encoding="utf-8",
    )
    (dest / "README.md").write_text(
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

MIT License

Copyright (c) 2026 Author
''',
        encoding="utf-8",
    )
    _write_common_files(dest, "python")


def generate_node_project(name, dest):
    """Generate a Node.js project scaffold."""
    _validate_project_name(name)
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)

    src_dir = dest / "src"
    src_dir.mkdir(exist_ok=True)
    (src_dir / "index.js").write_text(
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
        encoding="utf-8",
    )

    test_dir = dest / "test"
    test_dir.mkdir(exist_ok=True)
    (test_dir / "index.test.js").write_text(
        f'''const {{ main }} = require("../src/index.js");

describe("{name}", () => {{
    test("main function exists", () => {{
        expect(typeof main).toBe("function");
    }});
}});
''',
        encoding="utf-8",
    )

    (dest / "package.json").write_text(
        json.dumps(
            {
                "name": name,
                "version": "0.1.0",
                "description": "",
                "main": "src/index.js",
                "scripts": {"test": "jest", "start": "node src/index.js"},
                "author": "",
                "license": "MIT",
                "devDependencies": {"jest": "^29.0.0"},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (dest / ".gitignore").write_text(
        """node_modules/\n.npm\n.DS_Store\ndist/\nbuild/\n.env\n.env.local\n*.log\ncoverage/\n.vscode/\n.idea/\n""",
        encoding="utf-8",
    )
    (dest / "README.md").write_text(
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

MIT License

Copyright (c) 2026 Author
''',
        encoding="utf-8",
    )
    _write_common_files(dest, "node")


def generate_rust_project(name, dest):
    """Generate a Rust project scaffold."""
    _validate_project_name(name)
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)

    (dest / "Cargo.toml").write_text(
        f'''[package]
name = "{name}"
version = "0.1.0"
edition = "2021"
authors = ["Author <author@example.com>"]
license = "MIT"

[dependencies]

[dev-dependencies]
''',
        encoding="utf-8",
    )
    src_dir = dest / "src"
    src_dir.mkdir(exist_ok=True)
    (src_dir / "main.rs").write_text(
        f'''/// Main function for {name}
fn main() {{
    println!("Hello from {name}");
}}

#[cfg(test)]
mod tests {{
    #[test]
    fn it_works() {{
        assert_eq!(2 + 2, 4);
    }}
}}
''',
        encoding="utf-8",
    )
    (dest / ".gitignore").write_text(
        """/target/\n**/*.rs.bk\nCargo.lock\n.DS_Store\n.vscode/\n.idea/\n""",
        encoding="utf-8",
    )
    (dest / "README.md").write_text(
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

MIT License

Copyright (c) 2026 Author
''',
        encoding="utf-8",
    )
    _write_common_files(dest, "rust")


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
