# Contributing to DataForge AI

Thank you for contributing to DataForge AI.

## Setup

```bash
git clone https://github.com/your-org/dataforge-ai.git
cd dataforge-ai/backend
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Run tests

```bash
cd dataforge-ai/backend
uv run pytest
uv run ruff check app
```

## Local demo

```bash
cd dataforge-ai/backend
chmod +x demo/run_demo.sh
./demo/run_demo.sh
```

## Pull request guidance

- Keep changes focused on one feature, fix, or enhancement.
- Update README, ARCHITECTURE.md, or ROADMAP.md as needed when adding functionality.
- Add tests for new behavior and run `uv run pytest` locally.
- Ensure formatting with `uv run ruff check app`.
