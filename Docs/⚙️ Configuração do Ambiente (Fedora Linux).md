### Sistema Operacional
- **Distro:** Fedora (versão mais recente)
- **Diferencial:** Pacotes atualizados, kernel otimizado, suporte nativo a containers.
### Python e Ambiente Virtual
- **Python 3.13** instalado via sistema.
- **Ambiente virtual** (`venv`) para isolar dependências:


```bash 
python -m venv venv
source venv/bin/activate
```

### Dependências Principais

Arquivo `requirements.txt`:

```
requests == 2.32.3
pandas == 2.2.3
python-dotenv == 1.0.1
sqlalchemy == 2.0.36
psycopg2-binary == 2.9.10
pytest == 8.3.5
pytest-mock == 3.14.0
pytest-cov == 6.0.0
```

Instalação:
``` bash 
pip install -r requirements.txt
```
