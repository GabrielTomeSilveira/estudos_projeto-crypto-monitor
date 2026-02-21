### 1️⃣ Extração (`src/extract.py`)

**Função:** `fetch_crypto_data()`
- **Fonte:** API CoinGecko (endpoint `/coins/markets`)
- **Parâmetros:** `vs_currency=brl`, `order=market_cap_desc`, `per_page=10`
- **Retorno:** `pandas.DataFrame` com colunas:
    - `coin_id`: identificador da moeda (ex: `bitcoin`)
    - `price_brl`: preço em reais
    - `market_cap_brl`: capitalização de mercado
    - `volume_brl`: volume negociado
    - `extracted_at`: timestamp da extração (auditoria)
- **Tratamento de erros:**
    - Se a requisição falhar ou retornar lista vazia, retorna `None`.
    - Uso de `response.raise_for_status()` para capturar códigos HTTP de erro.
- **Logging:** Mensagens de sucesso ou erro são exibidas no console.

**Código resumido:**
``` python
import requests, pandas as pd
from datetime import datetime
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {...}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        # selecionar colunas e adicionar extracted_at
        return df
    except Exception as e:
        print(f"❌ [EXTRACT] {e}")
        return None
```
### 2️⃣ Configuração (`src/config.py`)

**Responsabilidade:** Carregar variáveis de ambiente e criar a engine SQLAlchemy.
- Usa `python-dotenv` para carregar o arquivo `.env`.
- Valida se todas as variáveis obrigatórias estão presentes.
- Retorna uma engine configurada para PostgreSQL.

**Código:**
```python 
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_engine():
    required = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        raise ValueError(f"Variáveis ausentes: {missing}")
    
    url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    return create_engine(url)
```

### 3️⃣ Carga (`src/load.py`)

**Função:** `load_data_to_postgres(df, table_name)`
- **Estratégia:** `if_exists='append'` – adiciona linhas mantendo histórico. 
- **Exigência:** A tabela deve existir previamente (criada via script SQL).
- **Tratamento de exceções:**
    - `ValueError`: captura erro de tabela inexistente e orienta o usuário.
    - `SQLAlchemyError`, `OperationalError`: erros de conexão ou banco.
    - Qualquer outro erro inesperado.
- **Logging:** mensagens de sucesso ou erro, e relançamento da exceção para que o pipeline falhe.

**Código:**
``` python 
def load_data_to_postgres(df, table_name):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            df.to_sql(table_name, con=conn, if_exists='append', index=False)
        print(f"✅ [LOAD] {len(df)} linhas inseridas em '{table_name}'.")
    except ValueError as ve:
        print(f"❌ [LOAD] Tabela '{table_name}' não existe. Execute scripts/init.sql primeiro.")
        raise
    except (SQLAlchemyError, OperationalError) as e:
        print(f"❌ [LOAD] Erro de banco: {e}")
        raise
    except Exception as e:
        print(f"❌ [LOAD] Erro inesperado: {e}")
        raise
```


### 4️⃣ Orquestração (`main.py`)
- Importa as funções de extração e carga.
- Configura logging (nível INFO).
- Executa o pipeline:
    1. Extrai dados; se falhar ou não houver dados, aborta com código de erro.
    2. Carrega dados no banco; se falhar, registra erro e retorna código 1.
    3. Se tudo ok, retorna 0 (sucesso).

**Código:**

``` python 
import logging
from src.extract import fetch_crypto_data
from src.load import load_data_to_postgres

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_pipeline():
    logger.info("🚀 Iniciando pipeline")
    df = fetch_crypto_data()
    if df is None or df.empty:
        logger.error("Extração falhou. Abortando.")
        return 1
    logger.info(f"✅ Extraídos {len(df)} registros.")
    try:
        load_data_to_postgres(df, "precos_crypto")
        logger.info("✨ Pipeline concluído com sucesso!")
        return 0
    except Exception:
        logger.error("❌ Pipeline falhou.")
        return 1

if __name__ == "__main__":
    exit(run_pipeline())
```

