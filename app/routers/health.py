from __future__ import annotations

import os
import platform
import sys
import time

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/health")

START_TIME = time.time()


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class SystemInfoResponse(BaseModel):
    os: str
    python_version: str
    uptime_seconds: float
    cpu_count: int | None


@router.get(
    "/live",
    response_model=HealthResponse,
    summary="Liveness probe",
    description="Returns 200 if the API Gateway process is running.",
    operation_id="health_live",
)
async def liveness() -> HealthResponse:
    from app.config import settings
    return HealthResponse(status="ok", service="api-gateway", version=settings.APP_VERSION)


@router.get(
    "/ready",
    response_model=HealthResponse,
    summary="Readiness probe",
    description="Returns 200 if the API Gateway can handle traffic (all config loaded).",
    operation_id="health_ready",
)
async def readiness() -> HealthResponse:
    from app.config import settings
    return HealthResponse(status="ok", service="api-gateway", version=settings.APP_VERSION)


@router.get("/test", tags=["Testing"])
async def test_endpoint() -> dict[str, str]:
    """Sample endpoint for manual testing and validation."""
    return {"message": "API Gateway is reachable and responsive!"}


@router.get(
    "/info",
    response_model=SystemInfoResponse,
    summary="System Information",
    description="Returns basic system information and uptime.",
    operation_id="health_info",
)
async def system_info() -> SystemInfoResponse:
    return SystemInfoResponse(
        os=f"{platform.system()} {platform.release()}",
        python_version=sys.version.split()[0],
        uptime_seconds=round(time.time() - START_TIME, 2),
        cpu_count=os.cpu_count(),
    )