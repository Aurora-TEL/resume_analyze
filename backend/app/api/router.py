from fastapi import APIRouter

from app.api.admin import router as admin_router
from app.api.auth import router as auth_router
from app.api.analysis import router as analysis_router
from app.api.health import router as health_router
from app.api.jobs import router as jobs_router
from app.api.reports import router as reports_router
from app.api.resumes import router as resumes_router
from app.api.users import router as users_router

api_router = APIRouter()
api_router.include_router(admin_router)
api_router.include_router(analysis_router)
api_router.include_router(auth_router)
api_router.include_router(health_router, tags=["health"])
api_router.include_router(jobs_router)
api_router.include_router(reports_router)
api_router.include_router(resumes_router)
api_router.include_router(users_router)
