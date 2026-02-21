projeto-crypto-monitor/

```text
├── .env                      # Credenciais do banco (NÃO versionado)
├── .gitignore                # Arquivos ignorados pelo git
├── docker-compose.yml        # Orquestração do PostgreSQL
├── requirements.txt          # Dependências Python
├── README.md                 # Documentação resumida
├── main.py                   # Orquestrador do pipeline
├── scripts/
│   └── init.sql              # Script SQL para criar a tabela
├── src/                      # Código fonte
│   ├── __init__.py
│   ├── config.py             # Configurações (engine, variáveis)
│   ├── extract.py            # Extração da API
│   ├── load.py               # Carga no banco
│   └── utils.py              # (opcional) funções auxiliares
├── tests/                    # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py           # Fixtures compartilhadas
│   ├── test_extract.py
│   └── test_load.py
└── data/                     # Dados locais (ignorados)
```


