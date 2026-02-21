import pandas as pd
import logging
from sqlalchemy import Table, MetaData, insert
from sqlalchemy.exc import SQLAlchemyError
from src.config import get_engine

logger = logging.getLogger(__name__)

def load_data_to_postgres(df, table_name):
    """
    Insere os dados do DataFrame na tabela do PostgreSQL usando SQLAlchemy Core.
    """
    try:
        engine = get_engine()
        
        # Converte o DataFrame para uma lista de dicionários (cada linha = um dict)
        data = df.to_dict(orient='records')
        
        # Usa uma transação gerenciada pelo engine.begin()
        with engine.begin() as conn:
            # Reflete a tabela do banco (ou pode definir o schema manualmente)
            metadata = MetaData()
            table = Table(table_name, metadata, autoload_with=conn)
            
            # Executa o insert em lote
            conn.execute(insert(table), data)
        
        logger.info(f"✅ [LOAD] {len(df)} linhas inseridas na tabela '{table_name}'.")
        return True

    except SQLAlchemyError as e:
        logger.error(f"❌ [LOAD] Erro de banco de dados: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ [LOAD] Erro inesperado: {e}")
        raise