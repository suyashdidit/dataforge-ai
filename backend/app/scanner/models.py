from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class FileType(StrEnum):
    SQL = "sql"
    DBT_MODEL = "dbt_model"
    OTHER = "other"


@dataclass(frozen=True)
class FileMetadata:
    path: str
    type: FileType
    size: int


@dataclass(frozen=True)
class ModelMetadata:
    name: str
    file_path: str
    dependencies: list[str]
    has_tests: bool
    risk_flags: list[str]


@dataclass(frozen=True)
class ProjectMetadata:
    project_name: str
    scanned_files: int
    dbt_detected: bool
    sql_files: list[FileMetadata]
    dbt_models: list[FileMetadata]
    models: list[ModelMetadata]
    lineage: dict[str, list[str]]
    risks: list[str]
    detected_dependencies: list[str]

    @property
    def total_files(self) -> int:
        return self.scanned_files
