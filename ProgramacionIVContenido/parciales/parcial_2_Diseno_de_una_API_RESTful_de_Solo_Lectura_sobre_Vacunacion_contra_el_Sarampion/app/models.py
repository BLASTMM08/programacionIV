from __future__ import annotations

from pydantic import BaseModel, Field


class VaccinationRecord(BaseModel):
    """Modelo de un registro anual de vacunación."""

    year: int = Field(..., description="Año del registro")
    country: str = Field(..., description="País de origen del dato")
    indicator: str = Field(..., description="Indicador del Banco Mundial")
    coverage: float = Field(..., description="Cobertura porcentual de vacunación")


class ProvincialCoverage(BaseModel):
    """Modelo de un registro simulado por provincia basado en un año específico."""

    province: str = Field(..., description="Nombre de la provincia")
    year: int = Field(..., description="Año del registro base")
    coverage: float = Field(..., description="Cobertura porcentual estimada")
