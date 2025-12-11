import os
from dotenv import load_dotenv

load_dotenv()


def keydb_settings() -> dict:
    return {
        "host": os.getenv("KEYDB_HOST", "localhost"),
        "port": int(os.getenv("KEYDB_PORT", "6379")),
        "password": os.getenv("KEYDB_PASSWORD"),
        "db": int(os.getenv("KEYDB_DB", "0")),
    }
