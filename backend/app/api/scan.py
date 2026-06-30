from fastapi import APIRouter, Depends, HTTPException

from app.scanner.service import ScannerService
from app.schemas.scan import ScanRequest, ScanResponse

router = APIRouter(prefix="/scan", tags=["Scanner"])


def get_scanner_service() -> ScannerService:
    return ScannerService()


scanner_service_dependency = Depends(get_scanner_service)


@router.post(
    "/",
    response_model=ScanResponse,
)
def scan_project(
    request: ScanRequest,
    service: ScannerService = scanner_service_dependency,
) -> ScanResponse:
    try:
        metadata = service.scan(request.path)
        return ScanResponse(
            project_name=metadata.project_name,
            dbt_detected=metadata.dbt_detected,
            scanned_files=metadata.scanned_files,
            sql_files=metadata.sql_files,
            dbt_models=metadata.dbt_models,
            models=[
                {
                    "name": model.name,
                    "file_path": model.file_path,
                    "dependencies": model.dependencies,
                    "has_tests": model.has_tests,
                    "risk_flags": model.risk_flags,
                }
                for model in metadata.models
            ],
            lineage=metadata.lineage,
            risks=metadata.risks,
            detected_dependencies=metadata.detected_dependencies,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
