### `docker-compose.yml`

```yaml
services:
  postgres:
    image: postgres:15
    container_name: crypto_postgres
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "${DB_PORT}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped
volumes:
  postgres_data:
```

**Explicação:**
- O serviço `postgres` usa a imagem oficial.
- As variáveis de ambiente são injetadas a partir do arquivo `.env`.
- O volume `postgres_data` persiste os dados entre execuções.
- O script `init.sql` é montado no diretório de inicialização do PostgreSQL, sendo executado automaticamente na primeira criação do container.

### Script de Inicialização (`scripts/init.sql`)

```sql
CREATE TABLE IF NOT EXISTS precos_crypto (
    id SERIAL PRIMARY KEY,
    coin_id VARCHAR(50),
    price_brl NUMERIC,
    market_cap_brl NUMERIC,
    volume_brl NUMERIC,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Função:** Garantir que a tabela exista antes de qualquer inserção. Isso é essencial para o funcionamento correto do pipeline com `if_exists='append'`.

### Comandos Docker

```bash 
# Subir o banco em background
docker compose up -d

# Parar e remover containers e volumes (apaga dados)
docker compose down -v

# Executar comando dentro do container
docker exec -it crypto_postgres psql -U <user> -d <db> -c "\dt"
```

### Serviço `app` (pipeline Python)
O `docker-compose.yml` agora inclui um serviço `app` que constrói a imagem da aplicação a partir do `Dockerfile`. Esse serviço:
- Depende do PostgreSQL (aguarda o healthcheck).
- Carrega as variáveis de ambiente do arquivo `.env`.
- Executa `python main.py` e encerra.
Assim, com um único comando (`docker compose up`) você sobe o banco e executa o pipeline de forma isolada e reproduzível.