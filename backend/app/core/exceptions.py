from typing import Any

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, message: str, code: int = 1000, status_code: int = 400, errors: Any = None):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.errors = errors
        super().__init__(message)


def _error_payload(message: str, code: int, errors: Any = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "success": False,
        "code": code,
        "message": message,
    }
    if errors is not None:
        payload["errors"] = errors
    return payload


async def app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_payload(exc.message, exc.code, exc.errors),
    )


async def http_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_payload(str(exc.detail), exc.status_code),
        )
    return JSONResponse(
        status_code=500,
        content=_error_payload("Internal server error", 5000),
    )


async def validation_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=422,
            content=_error_payload("Validation failed", 4220, exc.errors()),
        )
    return JSONResponse(
        status_code=400,
        content=_error_payload(str(exc), 4000),
    )
