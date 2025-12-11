import sys
from pathlib import Path

# Asegura que el paquete principal del parcial esté en sys.path durante las pruebas
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
