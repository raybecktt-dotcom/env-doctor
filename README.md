# 🏥 ENV-DOCTOR
> **Detect missing, empty, type-mismatched, and drifting environment variables before they break local builds or CI pipelines.**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tested with Pytest](https://img.shields.io/badge/tested%20with-pytest-yellow.svg)](https://docs.pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Key Features

* **🔍 Drift Detection:** Instantly flags missing or unpopulated `.env` keys defined in your template (`.env.example`).
* **🛡️ Secret Leak Scanner:** Scans sensitive variables (`API_KEY`, `SECRET`, `PASSWORD`) for weak, hardcoded, or default values (`12345`, `admin`, `secret`).
* **🏷️ Type & Format Annotations:** Enforces inline type declarations (`# type: int`, `# type: bool`, `# type: url`) right inside `.env.example`.
* **📄 Multi-Format Output:** Supports human-friendly terminal logs, `--format json` for tooling, and `--format markdown` for GitHub Actions summaries (`$GITHUB_STEP_SUMMARY`).
* **🪝 Pre-commit Integration:** Easily configures as a Git pre-commit hook to block invalid commits locally.

---

## 🏗️ Project Architecture

```text
env-doctor/
├── .github/
│   └── workflows/
│       └── ci.yml             # Automated CI testing pipeline
├── src/
│   ├── __init__.py
│   ├── checker.py             # Type validation & secret scanning engine
│   ├── cli.py                 # Multi-format CLI parser & report formatter
│   └── parser.py              # .env parser with inline annotation support
├── tests/
│   ├── __init__.py
│   └── test_checker.py        # Comprehensive test suite
├── .gitignore
├── .pre-commit-hooks.yaml     # Pre-commit hook definition
├── conftest.py                # Pytest path resolver
├── pyproject.toml
└── README.md
