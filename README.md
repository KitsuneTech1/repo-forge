<p align="center"><a href="https://kitsunetechnologies.org/work"><img src="https://raw.githubusercontent.com/KitsuneTech1/.github/main/assets/kitsune-banner.svg" alt="Built by Kitsune Technologies" width="760"></a></p>

# Repo Forge

Generate a starter repository with working tests, CI, and gitignore for Python, Node.js, or Rust.

[![Build Status](https://github.com/KitsuneTech1/repo-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/KitsuneTech1/repo-forge/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)

Repo Forge is a single Python file that scaffolds a new project with everything set up: a README template, test structure, GitHub Actions CI, and a language-specific `.gitignore`. It uses only the Python standard library and creates real, working code you can test and build on immediately.


## Architecture & Data Flow

```mermaid
flowchart LR
    A[CLI: repo-forge --type python|node|rust] --> B[Template Synthesis Engine]
    B --> C[Generate Starter Code, Tests, .gitignore]
    C --> D[Generate GitHub Actions CI Workflow]
    D --> E[Ready-to-Ship Initialized Repository]
```

## Quick start

Clone the repo and run the generator:

```bash
git clone https://github.com/KitsuneTech1/repo-forge.git
cd repo-forge
python forge.py my-project
```

This creates a new `my-project` directory with a working Python scaffold. Run its tests right away:

```bash
cd my-project
python -m unittest discover -s tests
```

For Node.js or Rust, add `--lang`:

```bash
python forge.py my-app --lang node
python forge.py my-tool --lang rust
```

To generate in a different directory:

```bash
python forge.py my-project --dest /path/to/projects
```

## What you get

Every generated project includes:

- A versioned `0.1.0` entry point and starter module
- A README template with sections for installation, usage, testing, and license
- A `LICENSE` file (MIT, with `Author` and year placeholders to fill in)
- A language-specific `.gitignore`
- A GitHub Actions workflow (`.github/workflows/ci.yml`) that runs tests on push and pull request
- Working example tests in the right structure for each language
- Build configuration: `pyproject.toml`, `package.json`, or `Cargo.toml`

Project names can include letters, numbers, hyphens, and underscores, and must start with a letter or number. Windows reserved names like `CON` and `NUL` are rejected. Generated files overwrite existing ones, except existing `LICENSE` files are kept.

## After generating a project

1. Replace the placeholder description in `README.md`.
2. Update the `Author` field in `LICENSE` and the language config.
3. Implement your functionality.
4. Verify tests pass: `python -m unittest discover -s tests` (Python), `npm test` (Node), or `cargo test` (Rust).
5. Initialize Git and make your first commit when ready.

## Testing repo-forge itself

The test suite runs offline:

```bash
python -m unittest
```

## License

MIT. Copyright (c) 2026 Kitsune Technologies LLC. Do what you like with it, commercially or otherwise, just keep the copyright notice. Full text in [LICENSE](LICENSE).

---

<p align="center"><sub>Part of <b>Buildtober 2026</b>: 31 open source projects in 31 days. Built by <a href="https://kitsunetechnologies.org/work">Kitsune Technologies</a>. More at <a href="https://github.com/KitsuneTech1">github.com/KitsuneTech1</a>.</sub></p>
