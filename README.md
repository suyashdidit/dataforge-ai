# DataForge AI

DataForge AI analyzes data changes and identifies downstream impact before merge.

## Quick start

```bash
git clone https://github.com/your-org/dataforge-ai.git
cd dataforge-ai/backend
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Run the demo dbt project

```bash
cd dataforge-ai/backend
python ./dataforge analyze-change ../examples/demo_dbt_project --markdown
```

## Run scan and impact analysis

```bash
cd dataforge-ai/backend
python ./dataforge analyze-change /path/to/dbt/project --markdown
```

## Example output

```
# ========================
DataForge Impact Report

Changed:
- orders

Risk: HIGH 85/100

Changed: orders

Affected:
- revenue

Findings:
⚠ breaking downstream dependency

Reasons:
- downstream dependencies

# ========================
```

## Demo fixtures

- `examples/demo_dbt_project/` contains a small dbt project with `customers`, `orders`, and `revenue` models.
- `examples/breaking_change/` contains an illustrative model change with `orders_before.sql` and `orders_after.sql`, showing removal of `customer_id` that creates downstream risk.
