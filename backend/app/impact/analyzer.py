from __future__ import annotations

from collections import defaultdict

from app.impact.models import ImpactAsset


class ImpactAnalyzer:
    def __init__(self, lineage: dict[str, list[str]]) -> None:
        self.lineage = lineage
        self.reverse_lineage = self._build_reverse_lineage(lineage)

    def _build_reverse_lineage(self, lineage: dict[str, list[str]]) -> dict[str, list[str]]:
        reverse: dict[str, list[str]] = defaultdict(list)
        for model, dependencies in lineage.items():
            for dependency in dependencies:
                reverse[dependency].append(model)
        return {model: sorted(dependents) for model, dependents in reverse.items()}

    def get_downstream_assets(self, model_name: str) -> list[ImpactAsset]:
        visited: set[str] = set()
        queue: list[tuple[str, str]] = [(model_name, "self")]
        affected_assets: list[ImpactAsset] = []

        while queue:
            current, relationship = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)

            if current != model_name:
                affected_assets.append(
                    ImpactAsset(
                        name=current,
                        type="model",
                        relationship=relationship,
                    )
                )

            for downstream in self.reverse_lineage.get(current, []):
                if downstream not in visited:
                    queue.append((downstream, "downstream"))

        return sorted(affected_assets, key=lambda asset: asset.name)

    def get_downstream_names(self, model_name: str) -> list[str]:
        return [asset.name for asset in self.get_downstream_assets(model_name)]
