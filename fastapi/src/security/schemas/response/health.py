from pydantic import BaseModel


class ServiceStatusType(BaseModel):
    database: bool


class HealthCheckResponse(BaseModel):
    success: bool
    up: ServiceStatusType