from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

from app.scanner.models import ModelMetadata


def build_model_lineage(models: Iterable[ModelMetadata]) -> dict[str, list[str]]:
    lineage: dict[str, list[str]] = defaultdict(list)
    for model in models:
        for dependency in model.dependencies:
            lineage[model.name].append(dependency)
    return {model: sorted(deps) for model, deps in lineage.items()}


def model_name_from_path(path: Path, root_path: Path) -> str:
    return path.relative_to(root_path).with_suffix("").as_posix().replace("/", ".")
