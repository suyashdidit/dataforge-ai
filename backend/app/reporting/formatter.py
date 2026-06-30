from __future__ import annotations

from typing import Any


def format_report_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = ["## DataForge Impact Report", ""]

    changed_models = report.get("changed_models", [])
    impact_reports = report.get("impact_reports", [])

    if changed_models:
        lines.append("Risk:")
        highest_risk = "LOW"
        highest_score = 0
        for impact in impact_reports:
            score = impact.get("risk_score", 0)
            level = impact.get("risk_level", "low")
            if score > highest_score:
                highest_score = score
                highest_risk = level.upper()
        lines.append(f"{highest_risk}")
        lines.append("")
        lines.append("Score:")
        lines.append(f"{highest_score}/100")
        lines.append("")
        lines.append("Changed:")
        for model in changed_models:
            lines.append(f"- {model}")
        lines.append("")

        for impact in impact_reports:
            lines.append(f"### Impact: {impact.get('changed_asset')}")
            lines.append("")
            affected_assets = impact.get("affected_assets", [])
            if affected_assets:
                lines.append("Affected:")
                for asset in affected_assets:
                    lines.append(f"- {asset.get('name')}")
                lines.append("")
            else:
                lines.append("Affected: none")
                lines.append("")

            findings = impact.get("findings", [])
            if findings:
                lines.append("Findings:")
                for finding in findings:
                    lines.append(f"- {finding.get('type')}")
                lines.append("")

            reasons = impact.get("reasons", [])
            if reasons:
                lines.append("Reasons:")
                for reason in reasons:
                    lines.append(f"- {reason}")
                lines.append("")
    else:
        lines.append("No changed dbt models detected.")

    return "\n".join(lines)
