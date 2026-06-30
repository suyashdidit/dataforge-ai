from __future__ import annotations

import re
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from app.git.models import ChangedFile, ChangeType

SQL_PATTERN = re.compile(r"\.sql$", re.IGNORECASE)
DBT_MODEL_SEGMENT = "models"
IGNORE_PATTERNS = [re.compile(r"(^|/)(docs?|documentation)(/|$)")]


@dataclass(frozen=True)
class GitChangeAnalyzer:
    repo_path: Path

    def _run_git(self, *args: str) -> str:
        completed = subprocess.run(
            ["git", "-C", str(self.repo_path), *args],
            capture_output=True,
            text=True,
            check=True,
        )
        return completed.stdout

    def get_diff_files(self, base_branch: str = "main") -> list[ChangedFile]:
        current_branch = self._run_git("rev-parse", "--abbrev-ref", "HEAD").strip()
        if current_branch == base_branch:
            diff_output = self._run_git("diff", "--name-status")
        else:
            diff_output = self._run_git("diff", "--name-status", f"{base_branch}...HEAD")

        changed_files: list[ChangedFile] = []

        for line in diff_output.splitlines():
            if not line.strip():
                continue
            status, *paths = line.split("\t")
            path = paths[-1]
            if self._should_include_file(path):
                change_type = self._map_status(status)
                if change_type is not None:
                    changed_files.append(ChangedFile(path=path, change_type=change_type))

        return changed_files

    def _should_include_file(self, path: str) -> bool:
        normalized = path.replace("\\", "/")
        if any(pattern.search(normalized) for pattern in IGNORE_PATTERNS):
            return False
        if SQL_PATTERN.search(normalized):
            return True
        return False

    def _map_status(self, status: str) -> ChangeType | None:
        if status == "A":
            return ChangeType.ADDED
        if status == "M":
            return ChangeType.MODIFIED
        if status == "D":
            return ChangeType.DELETED
        return None

    def get_changed_models(self, changed_files: Iterable[ChangedFile]) -> list[str]:
        models: list[str] = []
        for file in changed_files:
            if SQL_PATTERN.search(file.path) and DBT_MODEL_SEGMENT in Path(file.path).parts:
                model_name = self._extract_model_name(file.path)
                models.append(model_name)
        return sorted(set(models))

    def _extract_model_name(self, path: str) -> str:
        parts = Path(path).parts
        if DBT_MODEL_SEGMENT in parts:
            models_index = parts.index(DBT_MODEL_SEGMENT)
            model_path = Path(".".join(parts[models_index + 1:]))
            return model_path.with_suffix("").as_posix().replace("/", ".")
        return Path(path).with_suffix("").name
