import pytest
import pandas as pd
from src.extract import fetch_crypto_data

def test_fetch_crypto_data_returns_dataframe(mocker):
    """
    Testa se a função retorna um DataFrame não vazio quando a API responde com sucesso.
    """
    # Simula a resposta da API com dados falsos
    mock_response = [
        {
            "id": "bitcoin",
            "current_price": 250000.00,
            "market_cap": 5e12,
            "total_volume": 1e11
        },
        {
            "id": "ethereum",
            "current_price": 15000.00,
            "market_cap": 1.8e12,
            "total_volume": 5e10
        }
    ]
    
    # Cria um mock para requests.get
    mock_get = mocker.patch("src.extract.requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response
    
    # Executa a função
    df = fetch_crypto_data()
    
    # Verificações
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["coin_id", "price_brl", "market_cap_brl", "volume_brl", "extracted_at"]
    assert df.iloc[0]["coin_id"] == "bitcoin"
    assert df.iloc[0]["price_brl"] == 250000.00

def test_fetch_crypto_data_handles_api_error(mocker):
    """
    Testa se a função retorna None quando a API falha (ex: status_code != 200).
    """
    mock_get = mocker.patch("src.extract.requests.get")
    mock_get.return_value.status_code = 500
    mock_get.return_value.raise_for_status.side_effect = Exception("Erro HTTP")
    
    df = fetch_crypto_data()
    assert df is None

def test_fetch_crypto_data_handles_empty_response(mocker):
    """
    Testa se a função retorna None quando a API retorna lista vazia.
    """
    mock_get = mocker.patch("src.extract.requests.get")
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []
    
    df = fetch_crypto_data()
    assert df is None or df.empty  # Dependendo da implementação, pode retornar None ou df vazio