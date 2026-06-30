from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DbtProject:
    project_name: str
    root_path: Path
    model_paths: list[Path]


def parse_simple_yaml_value(text: str, key: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(f"{key}:"):
            return stripped.split(":", 1)[1].strip().strip('"').strip("'")
    return None


def detect_dbt_project(root_path: Path) -> DbtProject | None:
    project_file = root_path / "dbt_project.yml"
    if not project_file.exists():
        return None

    content = project_file.read_text(errors="ignore")
    project_name = parse_simple_yaml_value(content, "name") or root_path.name

    model_paths: list[Path] = []
    default_models = root_path / "models"
    if default_models.exists() and default_models.is_dir():
        model_paths.append(default_models)

    # Fallback: discover directories named models under the project root.
    if not model_paths:
        model_paths = [path for path in root_path.rglob("models") if path.is_dir()]

    return DbtProject(project_name=project_name, root_path=root_path, model_paths=model_paths)


def discover_model_files(project: DbtProject) -> Iterable[Path]:
    for models_path in project.model_paths:
        yield from models_path.rglob("*.sql")


def model_name_from_path(model_path: Path, project: DbtProject) -> str:
    for models_path in project.model_paths:
        try:
            relative = model_path.relative_to(models_path)
            return relative.with_suffix("").as_posix().replace("/", ".")
        except ValueError:
            continue
    return model_path.stem
