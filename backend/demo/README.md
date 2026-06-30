# DataForge AI Demo Repository

The demo repository shows the end-to-end experience for DataForge AI using a small sample dbt project.

## Structure

- `dbt_project.yml` — dbt project config
- `models/orders.sql` — base model
- `models/customers.sql` — upstream model
- `models/revenue.sql` — downstream model

## Demo steps

From the `backend` directory:

```bash
./demo/run_demo.sh
```

This script runs:

1. `uv run python demo/demo.py`
2. `./dataforge analyze-change`

The demo flow:

- creates `backend/demo/sample_dbt_repo`
- initializes Git and commits a baseline
- switches to a feature branch
- modifies `models/orders.sql`
- runs change impact analysis
- prints a structured JSON report

## Example CLI usage

```bash
cd backend
dataforge analyze-change demo/sample_dbt_repo --markdown
```

## Demo artifacts

- `backend/demo/demo.gif` — animated demonstration of the demo flow and output

## Notes

The demo harness is intentionally small and reproducible, so you can use it as a starting point for more advanced dbt and Git integration tests.
