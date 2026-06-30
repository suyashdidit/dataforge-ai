from __future__ import annotations

from app.impact.analyzer import ImpactAnalyzer
from app.impact.models import (
    FindingSeverity,
    ImpactAsset,
    ImpactReport,
    ImpactRiskLevel,
    RiskFinding,
)
from app.scanner.models import ProjectMetadata


class ImpactService:
    def analyze(self, changed_model: str, project_metadata: ProjectMetadata) -> ImpactReport:
        analyzer = ImpactAnalyzer(project_metadata.lineage)
        affected_assets = analyzer.get_downstream_assets(changed_model)

        risk_score, risk_level, findings, reasons = self._compute_risk(
            changed_model,
            project_metadata,
            affected_assets,
        )

        return ImpactReport(
            changed_asset=changed_model,
            affected_assets=affected_assets,
            risk_score=risk_score,
            risk_level=risk_level,
            findings=findings,
            reasons=reasons,
        )

    def _compute_risk(
        self,
        changed_model: str,
        project_metadata: ProjectMetadata,
        affected_assets: list[ImpactAsset],
    ) -> tuple[int, ImpactRiskLevel, list[RiskFinding], list[str]]:
        findings: list[RiskFinding] = []
        reasons: list[str] = []
        score = 0
        downstream_count = len(affected_assets)

        model_metadata = next(
            (model for model in project_metadata.models if model.name == changed_model),
            None,
        )

        if downstream_count > 3:
            score += 30
            findings.append(
                RiskFinding(
                    type="downstream_model_exposure",
                    severity=FindingSeverity.HIGH,
                    message="more than 3 downstream models",
                )
            )
            reasons.append("more than 3 downstream models")
        elif downstream_count > 0:
            score += 10
            findings.append(
                RiskFinding(
                    type="downstream_models",
                    severity=FindingSeverity.MEDIUM,
                    message=f"{downstream_count} downstream models",
                )
            )
            reasons.append("downstream dependencies")

        if model_metadata is not None:
            if not model_metadata.has_tests:
                score += 20
                findings.append(
                    RiskFinding(
                        type="missing_tests",
                        severity=FindingSeverity.MEDIUM,
                        message="missing tests",
                    )
                )
                reasons.append("missing tests")
            if "missing_documentation" in model_metadata.risk_flags:
                score += 10
                findings.append(
                    RiskFinding(
                        type="missing_documentation",
                        severity=FindingSeverity.LOW,
                        message="missing documentation",
                    )
                )
                reasons.append("missing documentation")

        risk_level = self._risk_level_from_score(score)
        return score, risk_level, findings, reasons

    def _risk_level_from_score(self, score: int) -> ImpactRiskLevel:
        if score >= 71:
            return ImpactRiskLevel.HIGH
        if score >= 31:
            return ImpactRiskLevel.MEDIUM
        return ImpactRiskLevel.LOW
