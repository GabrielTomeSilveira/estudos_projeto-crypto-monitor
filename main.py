from src.extract import fetch_crypto_data
from src.load import load_data_to_postgres
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_pipeline():
    logger.info("--- 🚀 Iniciando Pipeline de Dados Crypto ---")

    # Extração
    df = fetch_crypto_data()
    if df is None or df.empty:
        logger.error("⚠️ Pipeline abortado: A extração não retornou dados.")
        return 1  # Código de erro

    logger.info(f"--- 🔄 Dados extraídos: {len(df)} registros ---")

    # Carga
    try:
        load_data_to_postgres(df, "precos_crypto")
        logger.info("--- ✨ Pipeline finalizado com sucesso! ---")
        return 0  # Sucesso
    except Exception:
        logger.error("--- ❌ Pipeline falhou. Verifique os logs acima. ---")
        return 1

if __name__ == "__main__":
    exit(run_pipeline())

