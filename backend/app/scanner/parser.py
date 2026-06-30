from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path

from app.scanner.models import FileMetadata, FileType

DBT_MODEL_DIR = "models"

REF_PATTERN = re.compile(r"\{\{\s*ref\(['\"](?P<name>[^'\"]+)['\"]\)\s*\}\}")
SOURCE_PATTERN = re.compile(
    r"\{\{\s*source\(['\"](?P<source>[^'\"]+)['\"],"
    r"\s*['\"](?P<table>[^'\"]+)['\"]\)\s*\}\}"
)
TABLE_REF_PATTERN = re.compile(r"(?i)\b(?:from|join)\s+([a-zA-Z_][\w\.]+)")
SELECT_STAR_PATTERN = re.compile(r"(?i)select\s+\*")


def detect_file_type(path: Path) -> FileType:
    if path.suffix.lower() == ".sql":
        if DBT_MODEL_DIR in path.parts:
            return FileType.DBT_MODEL
        return FileType.SQL
    return FileType.OTHER


def scan_directory(path: Path) -> Iterable[FileMetadata]:
    for item in path.rglob("*"):
        if item.is_file():
            file_type = detect_file_type(item)
            yield FileMetadata(path=str(item), type=file_type, size=item.stat().st_size)


def extract_dependencies(sql: str) -> list[str]:
    dependencies: list[str] = []

    dependencies.extend(match.group("name") for match in REF_PATTERN.finditer(sql))
    dependencies.extend(
        f"{match.group('source')}.{match.group('table')}"
        for match in SOURCE_PATTERN.finditer(sql)
    )
    dependencies.extend(match.group(1) for match in TABLE_REF_PATTERN.finditer(sql))

    return sorted(set(dependencies))


def detect_risks(sql: str) -> list[str]:
    warnings: list[str] = []
    if SELECT_STAR_PATTERN.search(sql):
        warnings.append("select_star_usage")
    return warnings
