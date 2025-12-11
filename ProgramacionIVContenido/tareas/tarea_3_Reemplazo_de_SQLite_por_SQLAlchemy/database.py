"""Configuración de la base de datos y creación de sesiones de SQLAlchemy."""
from __future__ import annotations

import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, declarative_base, sessionmaker

load_dotenv()

Base = declarative_base()


class DatabaseError(RuntimeError):
    """Error envoltorio para problemas de conexión o consulta."""


# Cadena de conexión: mariadb+pymysql://usuario:password@host:puerto/base
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "mariadb+pymysql://biblioteca_user:biblioteca_pass@localhost:3306/biblioteca",
)


def get_engine():
    """Crea un engine de SQLAlchemy listo para usarse con MariaDB."""
    try:
        return create_engine(DATABASE_URL, echo=False, future=True)
    except SQLAlchemyError as exc:
        raise DatabaseError(f"No se pudo crear el engine: {exc}") from exc


_engine = get_engine()
SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    """Crea las tablas en la base de datos si no existen."""
    Base.metadata.create_all(bind=_engine)


def get_session() -> Generator[Session, None, None]:
    """Provee una sesión transaccional usando contexto generador."""
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as exc:
        session.rollback()
        raise DatabaseError(f"Error durante la operación: {exc}") from exc
    finally:
        session.close()
