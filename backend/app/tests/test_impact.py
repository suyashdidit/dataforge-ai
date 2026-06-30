from pathlib import Path

from fastapi.testclient import TestClient

from app.impact.service import ImpactService
from app.main import app
from app.scanner.service import ScannerService

client = TestClient(app)


def test_impact_service_detects_downstream_models(tmp_path: Path) -> None:
    models_dir = tmp_path / "models"
    models_dir.mkdir(parents=True)

    (models_dir / "orders.sql").write_text("SELECT 1;")
    (models_dir / "customer_metrics.sql").write_text(
        "SELECT * FROM {{ ref('orders') }};"
    )
    (models_dir / "revenue_dashboard.sql").write_text(
        "SELECT * FROM {{ ref('customer_metrics') }};"
    )

    service = ScannerService()
    metadata = service.scan(str(tmp_path))

    impact = ImpactService().analyze("orders", metadata)

    assert impact.changed_asset == "orders"
    assert [
        asset.name
        for asset in impact.affected_assets
    ] == ["customer_metrics", "revenue_dashboard"]
    assert impact.risk_score >= 0
    assert impact.risk_level in {"high", "medium"}
    assert isinstance(impact.findings, list)
    assert all(hasattr(finding, "type") for finding in impact.findings)
    assert "downstream dependencies" in impact.reasons


def test_impact_service_reports_findings_and_score(tmp_path: Path) -> None:
    models_dir = tmp_path / "models"
    models_dir.mkdir(parents=True)

    (models_dir / "orders.sql").write_text("SELECT 1;")
    (models_dir / "customer_metrics.sql").write_text(
        "SELECT * FROM {{ ref('orders') }};"
    )

    service = ScannerService()
    metadata = service.scan(str(tmp_path))
    impact = ImpactService().analyze("orders", metadata)

    assert impact.risk_score >= 10
    assert impact.risk_level in {"low", "medium", "high"}
    assert len(impact.findings) >= 1
    assert any(finding.type == "downstream_models" for finding in impact.findings)


def test_impact_api_endpoint(tmp_path: Path) -> None:
    models_dir = tmp_path / "models"
    models_dir.mkdir(parents=True)

    (models_dir / "orders.sql").write_text("SELECT 1;")
    (models_dir / "customer_metrics.sql").write_text(
        "SELECT * FROM {{ ref('orders') }};"
    )

    response = client.post(
        "/impact/",
        json={"path": str(tmp_path), "model": "orders"},
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["changed_asset"] == "orders"
    assert json_data["affected_assets"][0]["name"] == "customer_metrics"
    assert isinstance(json_data["risk_score"], int)
    assert json_data["risk_level"] in {"high", "medium", "low"}
    assert isinstance(json_data["findings"], list)
    assert isinstance(json_data["reasons"], list)
