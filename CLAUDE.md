# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This repository exists to learn CI/CD with GitHub Actions. The Python code is deliberately trivial — a small script with unit-testable functions whose only job is to give the pipeline something to lint, format-check, scan, test, and report on. Keep the Python side simple; the CI pipeline is the actual product.

The full pipeline specification (step order, tool config, secrets, reference workflow YAML) lives in `docs/ci-pipeline.md` — treat it as the source of truth when implementing or changing the pipeline.

## Layout

- `app.py` — simple script with pure functions
- `tests/` — pytest unit tests
- `conftest.py` — empty root conftest; puts the repo root on `sys.path` so tests can `from app import ...`
- `.github/workflows/ci.yml` — the main artifact: single-job Ubuntu CI pipeline
- `requirements-dev.txt` — source list of CI tooling (black, flake8, bandit, pip-audit, pytest, pytest-cov), unpinned
- `requirements-dev.lock` — `pip freeze` lock pinning the full dependency tree; what CI and teammates install from
- `.flake8` — lint config, kept compatible with black (line length 88, ignore E203/W503)
- `pyproject.toml` — black and pytest config
- `docs/ci-pipeline.md` — pipeline design doc

## Pipeline Architecture

One job on `ubuntu-latest`, sequential fail-fast steps in this order:

1. `black --check` — formatting gate
2. `flake8` — lint gate
3. `bandit` — SAST: static security scan of own code (tests/ excluded)
4. `pip-audit` — SCA: CVE scan of installed dependencies
5. `pytest --cov` — tests with coverage, writes `coverage.xml`
6. `actions/upload-artifact` — coverage report artifact
7. `dawidd6/action-send-mail` — email notification with `if: always()` so it fires on both success and failure (it is the only step that runs unconditionally)

Fail-fast is intentional: a lint failure skips tests and coverage upload, but the email still sends. Local commands must mirror these steps exactly so failures are caught before pushing.

Email delivery requires repo secrets: `SMTP_USERNAME`, `SMTP_PASSWORD`, `EMAIL_TO` (see `docs/ci-pipeline.md` for setup, including Gmail app passwords). Never hardcode SMTP credentials.

## Commands

```bash
# Install dev tooling (exact pinned versions)
pip install -r requirements-dev.lock

# After editing requirements-dev.txt: install and regenerate the lock
pip install -r requirements-dev.txt
pip freeze > requirements-dev.lock
# commit both files together

# Formatting check (CI gate) and auto-format
black --check --diff .
black .

# Lint
flake8 .

# Security scan (tests excluded — pytest asserts trip B101; .venv excluded —
# flake8/bandit have no default venv excludes, unlike black/pytest)
bandit -r . -x ./tests,./.venv

# Dependency CVE scan (SCA)
pip-audit

# Tests with coverage, exactly as CI runs them
pytest --cov=app --cov-report=term --cov-report=xml

# Run a single test file / single test by name
pytest tests/test_app.py
pytest tests/test_app.py -k test_name
```

The `--cov=app` value must match the top-level module name; update it if the entry module is renamed.
