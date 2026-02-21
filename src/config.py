import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_engine():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")

    # Validação robusta
    missing = [var for var in ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"] if os.getenv(var) is None]
    if missing:
        raise ValueError(f"Variáveis de ambiente faltando: {missing}")

    connection_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    return create_engine(connection_url)