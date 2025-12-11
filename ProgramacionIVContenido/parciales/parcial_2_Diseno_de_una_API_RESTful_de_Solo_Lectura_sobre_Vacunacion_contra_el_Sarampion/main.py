from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from app.data_access import get_all_records, get_record_by_year
from app.models import ProvincialCoverage, VaccinationRecord
from app.services import simulate_provincial_data

app = FastAPI(
    title="Cobertura de vacunación contra el sarampión en Panamá",
    description=(
        "API RESTful de solo lectura que expone el indicador SH.IMM.MEAS del Banco "
        "Mundial para Panamá."
    ),
    version="1.0.0",
)


@app.get("/vacunas", response_model=list[VaccinationRecord], tags=["Vacunas"])
def read_all_vaccines() -> list[VaccinationRecord]:
    """Devuelve todos los registros disponibles."""

    return list(get_all_records())


@app.get("/vacunas/{year}", response_model=VaccinationRecord, tags=["Vacunas"])
def read_vaccine_by_year(year: int) -> VaccinationRecord:
    """Devuelve el registro para un año específico."""

    record = get_record_by_year(year)
    if record is None:
        raise HTTPException(status_code=404, detail="No se encontró el año solicitado")

    return record


@app.get(
    "/vacunas/provincia/{province}",
    response_model=list[ProvincialCoverage],
    tags=["Vacunas"],
)
def read_provincial_data(
    province: str,
    year: int | None = Query(
        default=None,
        description="Año a consultar. Si no se especifica se usa el más reciente disponible.",
    ),
) -> list[ProvincialCoverage]:
    """Devuelve los datos simulados para una provincia específica."""

    records = list(get_all_records())
    if not records:
        raise HTTPException(status_code=503, detail="No hay datos disponibles")

    selected_year = year if year is not None else max(record.year for record in records)

    simulated = simulate_provincial_data(selected_year)

    filtered = [record for record in simulated if record.province.lower() == province.lower()]
    if not filtered:
        raise HTTPException(status_code=404, detail="Provincia no encontrada o sin datos")

    return filtered
