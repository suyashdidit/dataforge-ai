import json
import shutil
import subprocess
import sys
from pathlib import Path

# Ensure backend app package can be imported when executing demo.py directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.git.service import GitChangeService

BASE_DIR = Path(__file__).resolve().parent
REPO_DIR = BASE_DIR / "sample_dbt_repo"


def reset_demo_repo() -> None:
    if REPO_DIR.exists():
        shutil.rmtree(REPO_DIR)


def write_initial_repo() -> None:
    reset_demo_repo()
    REPO_DIR.mkdir(parents=True, exist_ok=True)
    (REPO_DIR / "dbt_project.yml").write_text(
        """name: sample_dbt_project
version: 1.0
"""
    )
    models_dir = REPO_DIR / "models"
    models_dir.mkdir(exist_ok=True)
    (models_dir / "orders.sql").write_text("SELECT 1 as order_id;\n")
    (models_dir / "customer_metrics.sql").write_text(
        "SELECT order_id, COUNT(*) AS order_count FROM {{ ref('orders') }} GROUP BY order_id;\n"
    )
    (models_dir / "revenue_dashboard.sql").write_text(
        "SELECT order_id, order_count FROM {{ ref('customer_metrics') }} WHERE order_count > 0;\n"
    )


def init_git_repo() -> None:
    if not (REPO_DIR / ".git").exists():
        subprocess.run(["git", "init"], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "config", "user.email", "demo@example.com"], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "config", "user.name", "Demo User"], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "add", "."], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "commit", "-m", "initial demo commit"], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=REPO_DIR, check=True)

    current_branch = subprocess.run(
        ["git", "-C", str(REPO_DIR), "branch", "--show-current"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    if current_branch != "feature":
        branches = subprocess.run(
            ["git", "-C", str(REPO_DIR), "branch", "--list", "feature"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if branches:
            subprocess.run(["git", "-C", str(REPO_DIR), "checkout", "feature"], check=True)
        else:
            subprocess.run(["git", "-C", str(REPO_DIR), "checkout", "-b", "feature"], check=True)


def modify_orders_model() -> None:
    (REPO_DIR / "models" / "orders.sql").write_text("SELECT 2 as order_id;\n")
    subprocess.run(["git", "-C", str(REPO_DIR), "add", "models/orders.sql"], check=True)
    subprocess.run(["git", "-C", str(REPO_DIR), "commit", "-m", "modify orders model"], check=True)


def run_change_analysis() -> None:
    service = GitChangeService()
    report = service.analyze_changes(str(REPO_DIR), base_branch="main")

    output = {
        "changed_models": report.changed_models,
        "impact_reports": [
            {
                "changed_asset": impact.changed_asset,
                "affected_assets": [
                    {
                        "name": asset.name,
                        "type": asset.type,
                        "relationship": asset.relationship,
                    }
                    for asset in impact.affected_assets
                ],
                "risk_level": impact.risk_level,
                "reasons": impact.reasons,
            }
            for impact in report.impact_reports
        ],
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    write_initial_repo()
    init_git_repo()
    modify_orders_model()
    run_change_analysis()
