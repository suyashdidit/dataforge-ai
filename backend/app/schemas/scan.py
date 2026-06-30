from __future__ import annotations

from pydantic import BaseModel

from app.scanner.models import FileMetadata


class ModelMetadataSchema(BaseModel):
    name: str
    file_path: str
    dependencies: list[str]
    has_tests: bool
    risk_flags: list[str]


class ScanRequest(BaseModel):
    path: str


class ScanResponse(BaseModel):
    project_name: str
    dbt_detected: bool
    scanned_files: int
    sql_files: list[FileMetadata]
    dbt_models: list[FileMetadata]
    models: list[ModelMetadataSchema]
    lineage: dict[str, list[str]]
    risks: list[str]
    detected_dependencies: list[str]
