from __future__ import annotations

from pathlib import Path

from app.scanner.dbt import (
    detect_dbt_project,
    discover_model_files,
    model_name_from_path,
)
from app.scanner.lineage import build_model_lineage
from app.scanner.models import FileMetadata, FileType, ModelMetadata, ProjectMetadata
from app.scanner.parser import detect_risks, extract_dependencies, scan_directory


class ScannerService:
    def scan(self, path: str) -> ProjectMetadata:
        project_path = Path(path).expanduser().resolve()
        if not project_path.exists() or not project_path.is_dir():
            raise FileNotFoundError(f"Project path not found: {project_path}")

        dbt_project = detect_dbt_project(project_path)
        dbt_detected = dbt_project is not None

        files: list[FileMetadata] = list(scan_directory(project_path))
        sql_files = [file for file in files if file.type == FileType.SQL]
        dbt_models = [file for file in files if file.type == FileType.DBT_MODEL]

        model_files = [Path(file.path) for file in dbt_models]
        if dbt_project:
            model_files = [path for path in discover_model_files(dbt_project)]

        models: list[ModelMetadata] = []
        dependencies: list[str] = []
        risk_flags: list[str] = []

        for model_path in model_files:
            sql_text = model_path.read_text(errors="ignore")
            model_name = (
                model_name_from_path(model_path, dbt_project)
                if dbt_project
                else model_path.with_suffix("").name
            )
            model_dependencies = extract_dependencies(sql_text)
            model_risks = detect_risks(sql_text)
            dependencies.extend(model_dependencies)

            if dbt_project:
                relative_model_path = model_path.relative_to(dbt_project.root_path)
            else:
                relative_model_path = model_path.relative_to(project_path)

            tests_exist = any(
                [
                    project_path.joinpath("tests", "models", f"{model_path.stem}.yml").exists(),
                    project_path.joinpath(
                        "tests",
                        "models",
                        relative_model_path.with_suffix(".yml"),
                    ).exists(),
                ]
            )

            documentation_missing = not any(
                [
                    project_path.joinpath("models", f"{model_path.stem}.yml").exists(),
                    project_path.joinpath("models", relative_model_path.with_suffix(".yml")).exists(),
                ]
            )

            model_risk_flags = []
            if not tests_exist:
                model_risk_flags.append("missing_tests")
            if documentation_missing:
                model_risk_flags.append("missing_documentation")
            if model_risks:
                model_risk_flags.extend(model_risks)

            models.append(
                ModelMetadata(
                    name=model_name,
                    file_path=str(model_path),
                    dependencies=sorted(set(model_dependencies)),
                    has_tests=tests_exist,
                    risk_flags=sorted(set(model_risk_flags)),
                )
            )

        lineage = build_model_lineage(models)

        if not dbt_detected and any(file.type == FileType.OTHER for file in files):
            risk_flags.append("unsupported_file")

        risks = sorted(set(risk_flags + [flag for model in models for flag in model.risk_flags]))

        return ProjectMetadata(
            project_name=dbt_project.project_name if dbt_project else project_path.name,
            scanned_files=len(files),
            dbt_detected=dbt_detected,
            sql_files=sql_files,
            dbt_models=dbt_models,
            models=models,
            lineage=lineage,
            risks=risks,
            detected_dependencies=sorted(set(dependencies)),
        )
