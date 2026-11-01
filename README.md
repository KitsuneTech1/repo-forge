<p align="center"><a href="https://kitsunetechnologies.org/work"><img src="https://raw.githubusercontent.com/KitsuneTech1/.github/main/assets/kitsune-banner.svg" alt="Built by Kitsune Technologies" width="760"></a></p>

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
- A `LICENSE` file. New projects receive MIT with `Author` and `2026` placeholders
- A language-specific `.gitignore`
- A GitHub Actions workflow at `.github/workflows/ci.yml`
- An example test, using a `tests` directory for Python, a `test` directory for Node.js, and an inline test module for Rust
- The language's build or package configuration: `pyproject.toml`, `package.json`, or `Cargo.toml`

Generated project names may contain letters, numbers, hyphens, and underscores, and must start with a letter or number. Windows device names such as `CON` and `NUL` are rejected. The generated files are overwritten if they already exist. An existing `LICENSE` file is preserved and referenced by the generated metadata.

## After generation

1. Replace the brief description in `README.md`.
2. If a new MIT `LICENSE` was generated, replace its `Author` placeholder. Replace `Author` in the language configuration if desired.
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

MIT. Copyright (c) 2026 Kitsune Technologies LLC. Do what you like with it, commercially or otherwise, just keep the copyright notice. Full text in [LICENSE](LICENSE).

---

<p align="center"><sub>Part of <b>Buildtober 2026</b>: 31 open source projects in 31 days. Built by <a href="https://kitsunetechnologies.org/work">Kitsune Technologies</a>. More at <a href="https://github.com/KitsuneTech1">github.com/KitsuneTech1</a>.</sub></p>
