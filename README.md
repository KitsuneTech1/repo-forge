# repo-forge

Scaffold a new MIT-licensed repository with a README, CI workflow, tests, and a language-specific `.gitignore` for Python, Node.js, or Rust.

The tool is a single Python file and uses only the Python standard library. It generates starter code and configuration. It does not install packages, initialize Git, or create a remote repository.

## Usage

Run the tool with Python 3.8 or newer:

```bash
python forge.py my-project
```

The command creates `./my-project`. Use `--lang` for Node.js or Rust:

```bash
python forge.py my-app --lang node
python forge.py my-tool --lang rust
```

Use `--dest` to choose the parent directory:

```bash
python forge.py my-project --dest /path/to/projects
```

That creates `/path/to/projects/my-project`.

## Generated files

Every project includes:

- A versioned `0.1.0` starter entry point
- A README with installation, usage, testing, and license sections
- An MIT `LICENSE` with `Author` and `2026` placeholders
- A language-specific `.gitignore`
- A GitHub Actions workflow at `.github/workflows/ci.yml`
- An example test, using a `tests` directory for Python, a `test` directory for Node.js, and an inline test module for Rust
- The language's build or package configuration: `pyproject.toml`, `package.json`, or `Cargo.toml`

Generated project names may contain letters, numbers, hyphens, and underscores, and must start with a letter or number. The generated files are overwritten if they already exist. An existing `LICENSE` file is preserved.

## After generation

1. Replace the brief description in `README.md`.
2. Replace `Author` in `LICENSE` and the language configuration.
3. Implement the project functionality.
4. Install the language's declared development tools if needed.
5. Run the generated test command.
6. Initialize Git and make the first commit when ready.

The generated test commands are:

```bash
python -m unittest discover -s tests
npm test
cargo test
```

## Testing repo-forge

```bash
python -m unittest
```

The test suite writes only temporary project files and makes no network calls.

## License

MIT License

Copyright (c) 2026 KitsuneTech1
