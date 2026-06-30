# Security Policy

Thank you for caring about security in DataForge AI.

## Reporting a vulnerability

If you discover a security issue, please report it responsibly by opening an issue and tagging it as a security concern, or by contacting the maintainers directly through the repository's issue tracker.

## Supported versions

This repository is actively maintained for the current `main` branch and the latest supported Python 3.14 environment.

## Security best practices

- Do not commit secrets, API tokens, or private credentials.
- Use environment variables for sensitive configuration.
- Run `uv run pytest` and `uv run ruff check app` before merging changes.
- Keep dependencies up to date and review transitive package changes.

## Disclosure

We appreciate coordinated disclosure. Please allow maintainers time to respond before publishing details publicly.
