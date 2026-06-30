from __future__ import annotations

from pydantic import BaseModel


class ImpactAssetSchema(BaseModel):
    name: str
    type: str
    relationship: str


class ImpactRequest(BaseModel):
    path: str
    model: str


class RiskFindingSchema(BaseModel):
    type: str
    severity: str
    message: str


class ImpactResponse(BaseModel):
    changed_asset: str
    affected_assets: list[ImpactAssetSchema]
    risk_score: int
    risk_level: str
    findings: list[RiskFindingSchema]
    reasons: list[str]
