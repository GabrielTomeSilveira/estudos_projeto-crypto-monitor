Utilizamos `pytest` com plugins `pytest-mock` e `pytest-cov`. Os testes estão na pasta `tests/`.
### Estrutura dos Testes

#### `conftest.py` (Fixtures)

- `sample_crypto_data`: DataFrame de exemplo com duas criptomoedas.
- `mock_engine`: engine SQLite em memória com a tabela criada para testes de carga.
#### `test_extract.py`
- `test_fetch_crypto_data_returns_dataframe`: mocka a requisição HTTP e verifica se o DataFrame tem as colunas esperadas.
- `test_fetch_crypto_data_handles_api_error`: simula erro HTTP e verifica se retorna `None`.
- `test_fetch_crypto_data_handles_empty_response`: simula resposta vazia e verifica retorno `None` ou DataFrame vazio.
#### `test_load.py`
- `test_load_data_to_postgres_inserts_data`: usa `mock_engine` (SQLite) e verifica se os dados são inseridos corretamente.
- `test_load_data_to_postgres_handles_empty_dataframe`: insere DataFrame vazio e verifica se nada é adicionado.
- `test_load_data_to_postgres_handles_database_error`: **teste crítico** – mocka o método `to_sql` do pandas para levantar `ValueError` simulando tabela inexistente. Verifica se a função relança a exceção.

### Mock do Erro de Tabela Inexistente

No PostgreSQL, `df.to_sql` com `append` em tabela inexistente levanta `ValueError`. Como usamos SQLite nos testes (que cria a tabela automaticamente), precisamos simular esse comportamento:

```python
def test_load_data_to_postgres_handles_database_error(sample_crypto_data, mocker):
    mocker.patch("src.load.get_engine", return_value=some_engine)
    mocker.patch("pandas.DataFrame.to_sql", side_effect=ValueError("relation does not exist"))
    with pytest.raises(ValueError, match="relation .* does not exist"):
        load_data_to_postgres(sample_crypto_data, "precos_crypto")
```

Isso garante que a lógica de captura de erro na função `load_data_to_postgres` seja testada adequadamente.

### Execução dos Testes

``` bash 
# Rodar todos os testes com verbose
pytest tests/ -v

# Com cobertura
pytest --cov=src tests/

# Teste específico
pytest tests/test_load.py::test_load_data_to_postgres_handles_database_error -v
```


