# DataForge AI Demo Repository

This demo repo is built to show the current DataForge AI change impact flow.

## Structure

- `dbt_project.yml` — dbt project config
- `models/orders.sql` — base model
- `models/customer_metrics.sql` — downstream model
- `models/revenue_dashboard.sql` — downstream dashboard model

## Demo steps

From the `backend` directory:

```bash
./demo/run_demo.sh
```

This script runs:

1. `uv run python demo/demo.py`
2. `./dataforge analyze-change`

The demo script will:

- create the sample dbt repo
- initialize git and commit the baseline
- switch to a `feature` branch
- modify `models/orders.sql`
- run the current change impact analysis
- print the impact report

The CLI wrapper provides:

- `./dataforge setup-demo`
- `./dataforge analyze-change`
