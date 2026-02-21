
1) **Clone o repositório** e entre na pasta.
2)  **Crie o ambiente virtual** e ative:
```bash    
    python -m venv venv
    source venv/bin/activate
```

3) **Instale as dependências:**
```bash 
    pip install -r requirements.txt
```

4) **Configure o arquivo `.env`** com as credenciais do banco.

5) **Suba o banco de dados:**
```bash
    docker compose up --build
```

6) **Execute o pipeline:**
```bash
    python main.py
```

7) **Para testes:**
```bash
 pytest tests/ -v
``` 
