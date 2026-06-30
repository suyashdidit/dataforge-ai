from __future__ import annotations

from pathlib import Path

from app.git.analyzer import GitChangeAnalyzer
from app.git.models import GitChangeReport
from app.impact.service import ImpactService
from app.scanner.service import ScannerService


class GitChangeService:
    def analyze_changes(self, path: str, base_branch: str = "main") -> GitChangeReport:
        repo_path = Path(path).expanduser().resolve()
        analyzer = GitChangeAnalyzer(repo_path=repo_path)

        changed_files = analyzer.get_diff_files(base_branch=base_branch)
        changed_models = analyzer.get_changed_models(changed_files)

        if changed_models:
            scanner = ScannerService()
            metadata = scanner.scan(str(repo_path))
            impact_service = ImpactService()
            impact_reports = [
                impact_service.analyze(model_name, metadata)
                for model_name in changed_models
            ]
        else:
            impact_reports = []

        return GitChangeReport(
            changed_files=changed_files,
            changed_models=changed_models,
            impact_reports=impact_reports,
        )
