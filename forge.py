#!/usr/bin/env python3
"""Generate a starter repository with real project baseline."""

import sys
import json
from pathlib import Path
from argparse import ArgumentParser


def generate_python_project(name, dest):
    """Generate a Python project scaffold."""
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)

    # Main module
    src_dir = dest / name.replace('-', '_')
    src_dir.mkdir(exist_ok=True)
    (src_dir / '__init__.py').write_text('"""' + name + ' package."""\n\n__version__ = "0.1.0"\n')
    (src_dir / 'main.py').write_text(f'''#!/usr/bin/env python3
"""Main module for {name}."""


def main():
    """Main entry point."""
    print("Hello from {name}")


if __name__ == "__main__":
    main()
''')

    # Tests
    tests_dir = dest / 'tests'
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / '__init__.py').write_text('')
    (tests_dir / 'test_main.py').write_text(f'''"""Tests for {name}."""

import unittest


class TestMain(unittest.TestCase):
    """Test main module."""

    def test_import(self):
        """Test that module imports."""
        import {name.replace('-', '_')}
        self.assertIsNotNone({name.replace('-', '_')})


if __name__ == "__main__":
    unittest.main()
''')

    # pyproject.toml
    (dest / 'pyproject.toml').write_text(f'''[build-system]
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
packages = ["{{name.replace('-', '_')}}"]
''')

    # .gitignore
    (dest / '.gitignore').write_text('''__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.pytest_cache/
.coverage
htmlcov/
.venv
venv/
ENV/
''')

    # README
    (dest / 'README.md').write_text(f'''# {name}

Brief description of what this project does.

## Installation

```bash
pip install -e .
```

## Usage

```bash
python -m {name.replace('-', '_')}
```

## Testing

```bash
python -m unittest discover tests
```

## License

MIT License

Copyright (c) 2026 Author
''')


def generate_node_project(name, dest):
    """Generate a Node.js project scaffold."""
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)

    # Source directory
    src_dir = dest / 'src'
    src_dir.mkdir(exist_ok=True)
    (src_dir / 'index.js').write_text(f'''/**
 * Main entry point for {name}
 */

function main() {{
    console.log("Hello from {name}");
}}

module.exports = {{ main }};

if (require.main === module) {{
    main();
}}
''')

    # Tests
    test_dir = dest / 'test'
    test_dir.mkdir(exist_ok=True)
    name_var = name.replace('-', '_')
    (test_dir / 'index.test.js').write_text(f'''const {name_var} = require("../src/index.js");

describe("{name}", () => {{
    test("main function exists", () => {{
        expect(typeof {name_var}.main).toBe("function");
    }});
}});
''')

    # package.json
    (dest / 'package.json').write_text(json.dumps({
        "name": name,
        "version": "0.1.0",
        "description": "",
        "main": "src/index.js",
        "scripts": {
            "test": "jest",
            "start": "node src/index.js"
        },
        "author": "",
        "license": "MIT",
        "devDependencies": {
            "jest": "^29.0.0"
        }
    }, indent=2))

    # .gitignore
    (dest / '.gitignore').write_text('''node_modules/
.npm
.DS_Store
dist/
build/
.env
.env.local
*.log
coverage/
.vscode/
.idea/
''')

    # README
    (dest / 'README.md').write_text(f'''# {name}

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

## License

MIT License

Copyright (c) 2026 Author
''')


def generate_rust_project(name, dest):
    """Generate a Rust project scaffold."""
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)

    # Cargo.toml
    (dest / 'Cargo.toml').write_text(f'''[package]
name = "{name}"
version = "0.1.0"
edition = "2021"
authors = ["Author <author@example.com>"]
license = "MIT"

[dependencies]

[dev-dependencies]
''')

    # Source directory
    src_dir = dest / 'src'
    src_dir.mkdir(exist_ok=True)
    (src_dir / 'main.rs').write_text(f'''/// Main function for {name}
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
''')

    # .gitignore
    (dest / '.gitignore').write_text('''/target/
**/*.rs.bk
Cargo.lock
.DS_Store
.vscode/
.idea/
''')

    # README
    (dest / 'README.md').write_text(f'''# {name}

Brief description of what this project does.

## Build

```bash
cargo build --release
```

## Test

```bash
cargo test
```

## License

MIT License

Copyright (c) 2026 Author
''')


def main():
    parser = ArgumentParser(description='Generate a starter repository.')
    parser.add_argument('name', help='Project name')
    parser.add_argument('--lang', choices=['python', 'node', 'rust'], default='python',
                        help='Programming language (default: python)')
    parser.add_argument('--dest', default='.',
                        help='Destination directory (default: current directory)')

    args = parser.parse_args()

    if args.lang == 'python':
        generate_python_project(args.name, args.dest)
    elif args.lang == 'node':
        generate_node_project(args.name, args.dest)
    elif args.lang == 'rust':
        generate_rust_project(args.name, args.dest)

    # Add LICENSE and .gitignore if not present
    dest = Path(args.dest)

    if not (dest / 'LICENSE').exists():
        (dest / 'LICENSE').write_text(f'''MIT License

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
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE OR OTHERWISE
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
''')

    print(f"Generated {args.lang} project: {args.name}")
    print(f"Location: {dest.resolve()}")


if __name__ == '__main__':
    main()
