from fastapi import APIRouter

from app.core.config import get_settings
from app.utils.response import success_response

router = APIRouter()


@router.get("/health", summary="Service health check")
def health_check():
    settings = get_settings()
    return success_response(
        data={
            "status": "healthy",
            "environment": settings.app_env,
        }
    )
