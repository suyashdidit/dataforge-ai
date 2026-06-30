import json
import os
import subprocess
import sys
from pathlib import Path


def init_git_repo(repo_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=repo_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True)
    (repo_path / "README.md").write_text("# repo")
    subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "initial commit"], cwd=repo_path, check=True)
    subprocess.run(["git", "branch", "-M", "main"], cwd=repo_path, check=True)


def run_dataforge(repo_root: Path, *args: str) -> str:
    script = Path(__file__).resolve().parents[3] / "backend" / "dataforge"
    env = os.environ.copy()
    result = subprocess.run(
        [sys.executable, str(script), "analyze-change", ".", *args],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def test_cli_analyze_change_outputs_valid_json(tmp_path: Path) -> None:
    init_git_repo(tmp_path)

    models_dir = tmp_path / "models"
    models_dir.mkdir(parents=True)
    (models_dir / "orders.sql").write_text("SELECT 1;")
    (models_dir / "customer_metrics.sql").write_text(
        "SELECT * FROM {{ ref('orders') }};"
    )
    subprocess.run(["git", "add", "models"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "add models"], cwd=tmp_path, check=True)
    subprocess.run(["git", "checkout", "-b", "feature"], cwd=tmp_path, check=True)

    (models_dir / "orders.sql").write_text("SELECT 2;")
    subprocess.run(["git", "add", "models/orders.sql"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "modify orders"], cwd=tmp_path, check=True)

    output = run_dataforge(tmp_path, "--json")
    parsed = json.loads(output)

    assert parsed["changed_models"] == ["orders"]
    assert isinstance(parsed["impact_reports"], list)
    assert parsed["impact_reports"][0]["changed_asset"] == "orders"
    assert parsed["impact_reports"][0]["risk_score"] >= 0
    assert parsed["impact_reports"][0]["findings"]


def test_cli_analyze_change_human_output(tmp_path: Path) -> None:
    init_git_repo(tmp_path)

    models_dir = tmp_path / "models"
    models_dir.mkdir(parents=True)
    (models_dir / "orders.sql").write_text("SELECT 1;")
    (models_dir / "customer_metrics.sql").write_text(
        "SELECT * FROM {{ ref('orders') }};"
    )
    subprocess.run(["git", "add", "models"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "add models"], cwd=tmp_path, check=True)
    subprocess.run(["git", "checkout", "-b", "feature"], cwd=tmp_path, check=True)

    (models_dir / "orders.sql").write_text("SELECT 2;")
    subprocess.run(["git", "add", "models/orders.sql"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "modify orders"], cwd=tmp_path, check=True)

    output = run_dataforge(tmp_path)
    assert "DataForge Impact Report" in output
    assert "Changed models:" in output
    assert "Risk:" in output
    assert "Affected:" in output
    assert "Findings:" in output


def test_cli_analyze_change_outputs_markdown(tmp_path: Path) -> None:
    init_git_repo(tmp_path)

    models_dir = tmp_path / "models"
    models_dir.mkdir(parents=True)
    (models_dir / "orders.sql").write_text("SELECT 1;")
    (models_dir / "customer_metrics.sql").write_text(
        "SELECT * FROM {{ ref('orders') }};"
    )
    subprocess.run(["git", "add", "models"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "add models"], cwd=tmp_path, check=True)
    subprocess.run(["git", "checkout", "-b", "feature"], cwd=tmp_path, check=True)

    (models_dir / "orders.sql").write_text("SELECT 2;")
    subprocess.run(["git", "add", "models/orders.sql"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "modify orders"], cwd=tmp_path, check=True)

    output = run_dataforge(tmp_path, "--markdown")
    assert "## DataForge Impact Report" in output
    assert "Risk:" in output
    assert "Score:" in output
    assert "Changed:" in output
    assert "Affected:" in output
    assert "Findings:" in output
    assert "- customer_metrics" in output
