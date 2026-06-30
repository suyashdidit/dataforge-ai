# DataForge Demo Output

This file captures the exact demo output from the current DataForge AI flow.

## Commands

From `backend`:

```bash
chmod +x demo/run_demo.sh
./demo/run_demo.sh
./dataforge analyze-change
```

## Expected Output

### Demo runner output

```text
Running demo script...
Initialized empty Git repository in /Users/w/Documents/GitHub/dataforge-ai/backend/demo/sample_dbt_repo/.git/
[main (root-commit) 4b71ec4] initial demo commit
 4 files changed, 5 insertions(+)
 create mode 100644 dbt_project.yml
 create mode 100644 models/customer_metrics.sql
 create mode 100644 models/orders.sql
 create mode 100644 models/revenue_dashboard.sql
Switched to a new branch 'feature'
[feature 59a933f] modify orders model
 1 file changed, 1 insertion(+), 1 deletion(-)
{
  "changed_models": [
    "orders"
  ],
  "impact_reports": [
    {
      "changed_asset": "orders",
      "affected_assets": [
        {
          "name": "customer_metrics",
          "type": "model",
          "relationship": "downstream"
        },
        {
          "name": "revenue_dashboard",
          "type": "model",
          "relationship": "downstream"
        }
      ],
      "risk_level": "medium",
      "reasons": [
        "multiple downstream dependencies",
        "missing tests",
        "missing documentation"
      ]
    }
  ]
}

Running dataforge analyze-change...
{
  "changed_models": [
    "orders"
  ],
  "impact_reports": [
    {
      "changed_asset": "orders",
      "affected_assets": [
        {
          "name": "customer_metrics",
          "type": "model",
          "relationship": "downstream"
        },
        {
          "name": "revenue_dashboard",
          "type": "model",
          "relationship": "downstream"
        }
      ],
      "risk_level": "medium",
      "reasons": [
        "multiple downstream dependencies",
        "missing tests",
        "missing documentation"
      ]
    }
  ]
}

Summary:
Changed models: orders
- orders impacts: customer_metrics, revenue_dashboard
  risk: medium
  reasons: multiple downstream dependencies, missing tests, missing documentation
```
