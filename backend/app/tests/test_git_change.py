import subprocess
from pathlib import Path

from fastapi.testclient import TestClient

from app.git.analyzer import GitChangeAnalyzer
from app.git.service import GitChangeService
from app.main import app

client = TestClient(app)


def init_git_repo(repo_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=repo_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True)
    (repo_path / "README.md").write_text("# repo")
    subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "initial commit"], cwd=repo_path, check=True)
    current_branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=repo_path,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    if current_branch != "main":
        subprocess.run(["git", "branch", "-M", "main"], cwd=repo_path, check=True)


def test_git_change_analyzer_detects_changed_sql_models(tmp_path: Path) -> None:
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

    analyzer = GitChangeAnalyzer(repo_path=tmp_path)
    changed_files = analyzer.get_diff_files(base_branch="main")
    changed_models = analyzer.get_changed_models(changed_files)

    assert len(changed_files) == 1
    assert changed_files[0].path == "models/orders.sql"
    assert changed_files[0].change_type.name.lower() == "modified"
    assert changed_models == ["orders"]


def test_git_change_service_integration_with_impact(tmp_path: Path) -> None:
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

    service = GitChangeService()
    report = service.analyze_changes(str(tmp_path), base_branch="main")

    assert report.changed_models == ["orders"]
    assert len(report.impact_reports) == 1
    assert report.impact_reports[0].changed_asset == "orders"
    assert report.impact_reports[0].affected_asset_names == ["customer_metrics"]


def test_git_analyze_change_endpoint(tmp_path: Path) -> None:
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

    response = client.post(
        "/analyze-change/",
        json={"path": str(tmp_path), "base_branch": "main"},
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["changed_models"] == ["orders"]
    assert json_data["impact_reports"][0]["changed_asset"] == "orders"
    assert json_data["impact_reports"][0]["affected_assets"][0]["name"] == "customer_metrics"
    assert isinstance(json_data["impact_reports"][0]["risk_score"], int)
    assert isinstance(json_data["impact_reports"][0]["findings"], list)
