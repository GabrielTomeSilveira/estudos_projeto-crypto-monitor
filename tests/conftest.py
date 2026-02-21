import pytest
import pandas as pd
from sqlalchemy import create_engine, text
from src.config import get_engine  # import original, mas vamos substituir para testes

@pytest.fixture
def sample_crypto_data():
    """Retorna um DataFrame de exemplo como se viesse da API."""
    return pd.DataFrame([
        {
            "coin_id": "bitcoin",
            "price_brl": 250000.00,
            "market_cap_brl": 5e12,
            "volume_brl": 1e11,
            "extracted_at": pd.Timestamp.now()
        },
        {
            "coin_id": "ethereum",
            "price_brl": 15000.00,
            "market_cap_brl": 1.8e12,
            "volume_brl": 5e10,
            "extracted_at": pd.Timestamp.now()
        }
    ])

@pytest.fixture
def mock_engine():
    """
    Cria uma engine SQLite em memória para testes de carga.
    Isso evita depender do PostgreSQL real durante os testes.
    """
    engine = create_engine("sqlite:///:memory:")
    # Cria a tabela para os testes
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE precos_crypto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coin_id TEXT,
                price_brl REAL,
                market_cap_brl REAL,
                volume_brl REAL,
                extracted_at TIMESTAMP
            )
        """))
    return engine