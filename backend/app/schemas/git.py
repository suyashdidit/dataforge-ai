from __future__ import annotations

from pydantic import BaseModel


class GitChangeRequest(BaseModel):
    path: str
    base_branch: str = "main"


class ImpactAssetSchema(BaseModel):
    name: str
    type: str
    relationship: str


class RiskFindingSchema(BaseModel):
    type: str
    severity: str
    message: str


class GitImpactReportSchema(BaseModel):
    changed_asset: str
    affected_assets: list[ImpactAssetSchema]
    risk_score: int
    risk_level: str
    findings: list[RiskFindingSchema]
    reasons: list[str]


class GitChangeResponse(BaseModel):
    changed_models: list[str]
    impact_reports: list[GitImpactReportSchema]
