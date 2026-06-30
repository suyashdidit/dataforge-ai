from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root():
    return {
        "message": "Welcome to DataForge AI"
    }


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }