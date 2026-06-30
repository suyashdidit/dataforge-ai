from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from app.impact.models import ImpactReport


class ChangeType(StrEnum):
    ADDED = "added"
    MODIFIED = "modified"
    DELETED = "deleted"


@dataclass(frozen=True)
class ChangedFile:
    path: str
    change_type: ChangeType


@dataclass(frozen=True)
class GitChangeReport:
    changed_files: list[ChangedFile]
    changed_models: list[str]
    impact_reports: list[ImpactReport] = field(default_factory=list)
