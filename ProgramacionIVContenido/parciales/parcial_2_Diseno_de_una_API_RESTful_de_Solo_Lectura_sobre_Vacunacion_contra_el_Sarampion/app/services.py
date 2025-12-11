from __future__ import annotations

from typing import Iterable

from app.data_access import get_record_by_year
from app.models import ProvincialCoverage

_PROVINCES = (
    "Bocas del Toro",
    "Coclé",
    "Colón",
    "Chiriquí",
    "Darién",
    "Herrera",
    "Los Santos",
    "Panamá",
    "Panamá Oeste",
    "Veraguas",
)


def simulate_provincial_data(year: int) -> Iterable[ProvincialCoverage]:
    """Genera datos simulados por provincia a partir de la cobertura nacional.

    Se aplica un ligero ajuste porcentual para cada provincia con el fin de ofrecer
    diversidad en los resultados manteniendo coherencia con el valor nacional.
    """

    base_record = get_record_by_year(year)
    if not base_record:
        return ()

    base_coverage = base_record.coverage
    adjustments = [-2.0, -1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5, 1.0, -0.5]

    simulated = []
    for province, delta in zip(_PROVINCES, adjustments):
        adjusted = max(0.0, min(100.0, base_coverage + delta))
        simulated.append(
            ProvincialCoverage(
                province=province,
                year=year,
                coverage=round(adjusted, 1),
            )
        )

    return tuple(simulated)
