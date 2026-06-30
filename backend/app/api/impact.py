from fastapi import APIRouter, Depends, HTTPException

from app.impact.service import ImpactService
from app.scanner.service import ScannerService
from app.schemas.impact import ImpactRequest, ImpactResponse

router = APIRouter(prefix="/impact", tags=["Impact"])


def get_scanner_service() -> ScannerService:
    return ScannerService()


def get_impact_service() -> ImpactService:
    return ImpactService()

scanner_service_dependency = Depends(get_scanner_service)
impact_service_dependency = Depends(get_impact_service)


@router.post(
    "/",
    response_model=ImpactResponse,
)
def analyze_impact(
    request: ImpactRequest,
    service: ImpactService = impact_service_dependency,
    scanner: ScannerService = scanner_service_dependency,
) -> ImpactResponse:
    try:
        metadata = scanner.scan(request.path)
        report = service.analyze(request.model, metadata)

        return ImpactResponse(
            changed_asset=report.changed_asset,
            affected_assets=[
                {
                    "name": asset.name,
                    "type": asset.type,
                    "relationship": asset.relationship,
                }
                for asset in report.affected_assets
            ],
            risk_score=report.risk_score,
            risk_level=report.risk_level,
            findings=[
                {
                    "type": finding.type,
                    "severity": finding.severity,
                    "message": finding.message,
                }
                for finding in report.findings
            ],
            reasons=report.reasons,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
