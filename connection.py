"""Configuração de banco de dados para Flask e SQLAlchemy."""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") 
print("DATABASE_URL =", DATABASE_URL)
if not DATABASE_URL:
    raise ValueError("A variável DATABASE_URL não foi encontrada no arquivo .env ou nas variáveis de ambiente")

def parse_bool(value, default=False):
    if value is None:
        return default
    return str(value).strip().lower() in ("1", "true", "yes", "on")

class Config:
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "future": True,
    }
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    DEBUG = parse_bool(os.getenv("DEBUG", "False"))

engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    future=True,
)

Base = declarative_base()

def test_database_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("✅ Banco de dados conectado com sucesso!")
    except OperationalError as exc:
        print("⚠️ Não foi possível conectar ao banco de dados no startup.")
        print(exc)

if parse_bool(os.getenv("VERIFY_DB_CONNECTION", "False")):
    test_database_connection()
