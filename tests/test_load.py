import pytest
import pandas as pd
from sqlalchemy import text
from src.load import load_data_to_postgres

def test_load_data_to_postgres_inserts_data(sample_crypto_data, mock_engine, mocker):
    """
    Testa se os dados são inseridos corretamente na tabela.
    """
    # Substitui a engine original pela mock_engine
    mocker.patch("src.load.get_engine", return_value=mock_engine)
    
    # Executa a carga
    load_data_to_postgres(sample_crypto_data, "precos_crypto")
    
    # Verifica se os dados foram inseridos
    with mock_engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM precos_crypto")).scalar()
        assert result == 2
        
        # Verifica um registro específico
        bitcoin = conn.execute(
            text("SELECT coin_id, price_brl FROM precos_crypto WHERE coin_id = 'bitcoin'")
        ).first()
        assert bitcoin[0] == "bitcoin"
        assert bitcoin[1] == 250000.00

def test_load_data_to_postgres_handles_empty_dataframe(mock_engine, mocker):
    """
    Testa o comportamento quando o DataFrame é vazio.
    """
    mocker.patch("src.load.get_engine", return_value=mock_engine)
    df_vazio = pd.DataFrame(columns=["coin_id", "price_brl"])
    
    # Deve executar sem erro, mas não inserir nada
    load_data_to_postgres(df_vazio, "precos_crypto")
    
    with mock_engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM precos_crypto")).scalar()
        assert count == 0

def test_load_data_to_postgres_handles_database_error(sample_crypto_data, mocker):
    """
    Testa se a função levanta ValueError quando a tabela não existe.
    Neste teste, mockamos o método to_sql para que ele levante a exceção,
    simulando o comportamento do PostgreSQL.
    """
    from sqlalchemy import create_engine
    bad_engine = create_engine("sqlite:///:memory:")  # engine qualquer, não usaremos de fato

    # Patch na engine e no método to_sql
    mocker.patch("src.load.get_engine", return_value=bad_engine)
    
    # Mock do método to_sql no DataFrame para levantar ValueError
    mock_to_sql = mocker.patch("pandas.DataFrame.to_sql", side_effect=ValueError("(psycopg2.errors.UndefinedTable) relation \"precos_crypto\" does not exist"))

    with pytest.raises(ValueError, match="relation .* does not exist"):
        load_data_to_postgres(sample_crypto_data, "precos_crypto")
    
    # Verifica se to_sql foi chamado (opcional)
    mock_to_sql.assert_called_once()