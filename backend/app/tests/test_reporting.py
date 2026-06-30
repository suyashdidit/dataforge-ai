from app.reporting.formatter import format_report_markdown


def test_report_formatter_generates_markdown() -> None:
    report = {
        "changed_models": ["orders"],
        "impact_reports": [
            {
                "changed_asset": "orders",
                "affected_assets": [
                    {"name": "customer_metrics"},
                    {"name": "revenue_dashboard"},
                ],
                "risk_score": 72,
                "risk_level": "high",
                "findings": [
                    {"type": "downstream_dependency", "severity": "high", "message": "..."},
                    {"type": "missing_tests", "severity": "medium", "message": "..."},
                ],
                "reasons": ["downstream dependencies", "missing tests"],
            }
        ],
    }

    markdown = format_report_markdown(report)

    assert "## DataForge Impact Report" in markdown
    assert "Risk:" in markdown
    assert "HIGH" in markdown
    assert "Score:" in markdown
    assert "72/100" in markdown
    assert "Changed:" in markdown
    assert "- orders" in markdown
    assert "Affected:" in markdown
    assert "- customer_metrics" in markdown
    assert "- revenue_dashboard" in markdown
    assert "Findings:" in markdown
    assert "- downstream_dependency" in markdown
    assert "- missing_tests" in markdown


def test_report_formatter_no_changed_models() -> None:
    report = {"changed_models": [], "impact_reports": []}
    markdown = format_report_markdown(report)
    assert "No changed dbt models detected." in markdown
