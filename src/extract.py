import requests
import pandas as pd
from datetime import datetime

def fetch_crypto_data():
    """
    Extrai dados de criptomoedas da API CoinGecko (mercado).
    Retorna um DataFrame com as colunas:
    - coin_id: identificador da moeda (ex: bitcoin)
    - price_brl: preço em reais
    - market_cap_brl: capitalização de mercado em reais
    - volume_brl: volume de negociação em reais
    - extracted_at: timestamp da extração (auditoria)
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "brl",          # Moeda de referência: real brasileiro
        "order": "market_cap_desc",    # Ordenar por maior capitalização
        "per_page": 10,                 # Número de moedas (você pode aumentar)
        "page": 1,
        "sparkline": "false"            # Não precisamos dos gráficos
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Levanta exceção para códigos 4xx/5xx

        data = response.json()  # Lista de dicionários

        # Extrair apenas os campos desejados
        records = []
        for coin in data:
            records.append({
                "coin_id": coin["id"],
                "price_brl": coin["current_price"],
                "market_cap_brl": coin["market_cap"],
                "volume_brl": coin["total_volume"]
            })

        # Criar DataFrame
        df = pd.DataFrame(records)

        # Adicionar coluna de auditoria: data/hora da extração
        df["extracted_at"] = datetime.now()

        print(f"✅ [EXTRACT] Dados extraídos com sucesso: {len(df)} moedas.")
        return df

    except requests.exceptions.RequestException as e:
        print(f"❌ [EXTRACT] Erro na requisição à API: {e}")
        return None
    except Exception as e:
        print(f"❌ [EXTRACT] Erro inesperado: {e}")
        return None