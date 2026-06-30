from pathlib import Path

from app.impact.service import ImpactService
from app.reporting.formatter import format_report_markdown
from app.scanner.service import ScannerService


def test_demo_project_scans() -> None:
    example_root = Path(__file__).resolve().parents[3] / "examples" / "demo_dbt_project"
    service = ScannerService()
    metadata = service.scan(str(example_root))

    assert metadata.dbt_detected is True
    assert metadata.project_name == "demo_dbt_project"
    assert len(metadata.models) == 3
    assert any(model.name == "orders" for model in metadata.models)


def test_demo_project_impact_detects_downstream() -> None:
    example_root = Path(__file__).resolve().parents[3] / "examples" / "demo_dbt_project"
    service = ScannerService()
    metadata = service.scan(str(example_root))

    impact = ImpactService().analyze("customers", metadata)

    assert impact.changed_asset == "customers"
    assert {asset.name for asset in impact.affected_assets} == {"orders", "revenue"}
    assert impact.risk_score > 0


def test_demo_markdown_generation() -> None:
    report = {
        "changed_models": ["orders"],
        "impact_reports": [
            {
                "changed_asset": "orders",
                "affected_assets": [{"name": "revenue"}],
                "risk_score": 85,
                "risk_level": "high",
                "findings": [
                    {
                        "type": "downstream_dependency",
                        "severity": "high",
                        "message": "breaking downstream dependency",
                    }
                ],
                "reasons": ["downstream dependencies"],
            }
        ],
    }

    markdown = format_report_markdown(report)
    assert "## DataForge Impact Report" in markdown
    assert "HIGH" in markdown
    assert "Score:" in markdown
    assert "85/100" in markdown
    assert "- revenue" in markdown
    assert "breaking downstream dependency" in markdown
