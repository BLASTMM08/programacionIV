from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Iterable

from app.models import VaccinationRecord


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "vaccination_data.json"


@lru_cache(maxsize=1)
def load_records() -> tuple[VaccinationRecord, ...]:
    """Carga y valida los registros desde el archivo JSON."""

    with DATA_PATH.open("r", encoding="utf-8") as fp:
        raw_records = json.load(fp)

    return tuple(VaccinationRecord(**record) for record in raw_records)


def get_all_records() -> Iterable[VaccinationRecord]:
    """Devuelve todos los registros disponibles."""

    return load_records()


def get_record_by_year(year: int) -> VaccinationRecord | None:
    """Busca un registro por año."""

    return next((record for record in load_records() if record.year == year), None)
