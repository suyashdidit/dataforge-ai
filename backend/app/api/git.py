import subprocess

from fastapi import APIRouter, Depends, HTTPException

from app.git.service import GitChangeService
from app.schemas.git import GitChangeRequest, GitChangeResponse

router = APIRouter(prefix="/analyze-change", tags=["Git"])


def get_git_change_service() -> GitChangeService:
    return GitChangeService()


git_change_service_dependency = Depends(get_git_change_service)


@router.post(
    "/",
    response_model=GitChangeResponse,
)
def analyze_git_changes(
    request: GitChangeRequest,
    service: GitChangeService = git_change_service_dependency,
) -> GitChangeResponse:
    try:
        report = service.analyze_changes(request.path, request.base_branch)
        return GitChangeResponse(
            changed_models=report.changed_models,
            impact_reports=[
                {
                    "changed_asset": impact.changed_asset,
                    "affected_assets": [
                        {
                            "name": asset.name,
                            "type": asset.type,
                            "relationship": asset.relationship,
                        }
                        for asset in impact.affected_assets
                    ],
                    "risk_score": impact.risk_score,
                    "risk_level": impact.risk_level,
                    "findings": [
                        {
                            "type": finding.type,
                            "severity": finding.severity,
                            "message": finding.message,
                        }
                        for finding in impact.findings
                    ],
                    "reasons": impact.reasons,
                }
                for impact in report.impact_reports
            ],
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except subprocess.CalledProcessError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
