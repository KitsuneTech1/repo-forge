# repo-forge

Scaffold a new MIT-licensed repository with README, CI, tests and .gitignore for Python, Node or Rust in one command.

## What it does

Generates a complete starter repository structure with:
- Source code directory with a main entry point
- Test directory with example test
- README.md with installation and usage sections
- License file (MIT)
- Language-appropriate .gitignore
- Dependency or build configuration (pyproject.toml, package.json, Cargo.toml)

All generated code follows a consistent house style: clear, testable, minimal.

## Installation

```bash
pip install -e .
```

Or run directly:

```bash
python forge.py <name> [options]
```

## Usage

### Python project (default)

```bash
python forge.py my-project
```

This creates:
- my-project/
  - my_project/ (module directory)
    - __init__.py
    - main.py
  - tests/
    - __init__.py
    - test_main.py
  - pyproject.toml
  - README.md
  - .gitignore
  - LICENSE

### Node.js project

```bash
python forge.py my-app --lang node
```

This creates:
- my-app/
  - src/
    - index.js
  - test/
    - index.test.js
  - package.json
  - README.md
  - .gitignore
  - LICENSE

### Rust project

```bash
python forge.py my-tool --lang rust
```

This creates:
- my-tool/
  - src/
    - main.rs
  - Cargo.toml
  - README.md
  - .gitignore
  - LICENSE

### Custom destination

```bash
python forge.py my-project --dest /path/to/projects
```

## Output structure

Each generated project includes:
- A main entry point with example code
- Tests with at least one example test case
- README with installation, usage, and testing sections
- MIT license with "Author" and "2026" placeholders (edit these)
- .gitignore appropriate for the language
- A note that the project is at v0.1.0

## Next steps after generation

1. Edit README.md: replace "Brief description" and fill in real details
2. Edit LICENSE: replace "Author" with your name
3. Implement your functionality
4. Run tests: `python -m unittest` (Python), `npm test` (Node), `cargo test` (Rust)
5. Add dependencies as needed to the appropriate config file
6. Initialize git and make your first commit

## Testing

```bash
python -m unittest test_forge
```

## License

MIT License

Copyright (c) 2026 KitsuneTech1
