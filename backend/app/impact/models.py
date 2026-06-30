from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ImpactRiskLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FindingSeverity(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass(frozen=True)
class ImpactAsset:
    name: str
    type: str
    relationship: str


@dataclass(frozen=True)
class RiskFinding:
    type: str
    severity: FindingSeverity
    message: str


@dataclass(frozen=True)
class ImpactReport:
    changed_asset: str
    affected_assets: list[ImpactAsset]
    risk_score: int
    risk_level: ImpactRiskLevel
    findings: list[RiskFinding]
    reasons: list[str]

    @property
    def affected_asset_names(self) -> list[str]:
        return [asset.name for asset in self.affected_assets]
