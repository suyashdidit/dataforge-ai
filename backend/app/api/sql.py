from fastapi import APIRouter

from app.ai.service import AIService

router = APIRouter(prefix="/sql", tags=["SQL"])


@router.post("/explain")
def explain(payload: dict):

    sql = payload["sql"]

    service = AIService()

    return {
        "result": service.explain_sql(sql)
    }