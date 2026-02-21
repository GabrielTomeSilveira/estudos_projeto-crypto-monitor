
> **Nota:** Este documento registra todos os passos, decisões e correções feitas para adicionar o Apache Airflow como orquestrador do pipeline ETL de criptomoedas.

## Índice

- [[#1. Objetivo]]
    
- [[#2. Estrutura de Arquivos Criada]]
    
- [[#3. Configuração do Dockerfile.airflow]]
    
- [[#4. Ajustes no docker-compose.yml]]
    
- [[#5. Criação da DAG]]
    
- [[#6. Problemas e Soluções]]
    
    - [[#6.1. Tag da Imagem do Airflow]]
        
    - [[#6.2. Conflito de Versão do SQLAlchemy]]
        
    - [[#6.3. Erro no load.py (`cursor`)]]
        
    - [[#6.4. Banco do Airflow Não Inicializado]]
        
    - [[#6.5. Login no Airflow (criação de usuário)]]
        
    - [[#6.6. Erro de permissão no Docker]]
        
- [[#7. Adição do pgAdmin (Interface Gráfica)]]
    
- [[#8. Testes e Validação]]
    
- [[#9. Agendamento e Ajustes Finais]]
    

---

## 1. Objetivo

Adicionar um orquestrador ao pipeline ETL para executar o script `main.py` de forma agendada (a cada hora), com interface web para monitoramento e logs centralizados.

---

## 2. Estrutura de Arquivos Criada

Foram adicionados/modificados os seguintes arquivos:

```text

projeto-crypto-monitor/
├── Dockerfile.airflow          # Imagem customizada do Airflow
├── docker-compose.yml          # Adicionados serviços: airflow-init, webserver, scheduler, pgadmin
├── dags/
│   └── crypto_pipeline_dag.py  # DAG que executa o pipeline
├── scripts/
│   └── init-airflow-db.sh      # Script opcional (substituído por airflow-init)
└── .env                        # (ajustado: DB_HOST=postgres)

---
```
## 3. Configuração do Dockerfile.airflow

Arquivo base para construir a imagem do Airflow com as dependências do projeto.

```dockerfile

FROM apache/airflow:2.10.5
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
```

> **Nota:** Inicialmente tentamos `apache/airflow:2.10.5-python3.13`, mas essa tag não existe. Corrigido para `2.10.5` (que usa Python 3.12).

---

## 4. Ajustes no docker-compose.yml

O arquivo foi expandido para incluir:

- **Âncora `x-airflow-common`** com configurações compartilhadas (build, volumes, env).
    
- **Serviço `airflow-init`**: executa `airflow db init` (cria as tabelas do Airflow no banco).
    
- **Serviços `airflow-webserver`** e **`airflow-scheduler`**: dependem do `airflow-init` para só subirem após a inicialização do banco.
    
- **Serviço `pgadmin`**: interface gráfica para visualizar os dados no PostgreSQL.
    

Ajuste crítico: o `depends_on` foi movido da âncora para cada serviço individualmente, com condições (`service_healthy` e `service_completed_successfully`). A versão do Compose foi declarada como `3.8` para suportar essa sintaxe.

Exemplo do serviço `airflow-scheduler`:

```yaml

airflow-scheduler:
  <<: *airflow-common
  command: scheduler
  depends_on:
    postgres:
      condition: service_healthy
    airflow-init:
      condition: service_completed_successfully

```

## 5. Criação da DAG

Arquivo `dags/crypto_pipeline_dag.py` define a DAG que executa o pipeline.

```python

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.extract import fetch_crypto_data
from src.load import load_data_to_postgres
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2026, 2, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
dag = DAG(
    'crypto_pipeline',
    default_args=default_args,
    description='Pipeline ETL de criptomoedas',
    schedule_interval='@hourly',   # depois alterado para testes
    catchup=False,
)
def run_pipeline(**context):
    df = fetch_crypto_data()
    if df is None or df.empty:
        raise ValueError("Extração falhou")
    load_data_to_postgres(df, 'precos_crypto')
    return "OK"
tarefa = PythonOperator(
    task_id='executa_pipeline_etl',
    python_callable=run_pipeline,
    dag=dag,
)

```

## 6. Problemas e Soluções

### 6.1. Tag da Imagem do Airflow

**Erro:** `docker.io/apache/airflow:2.10.5-python3.13: not found`  
**Solução:** Usar `apache/airflow:2.10.5` (Python 3.12). O código do projeto permanece compatível.

### 6.2. Conflito de Versão do SQLAlchemy

**Erro:** O Airflow (que usa SQLAlchemy 1.4) estava sendo sobrescrito pela versão 2.0.36 do `requirements.txt`, causando `MappedAnnotationError`.  
**Solução:** Fixar `sqlalchemy==1.4.52` no `requirements.txt`.

### 6.3. Erro no load.py (`cursor`)

**Erro:** `'Engine' object has no attribute 'cursor'` ou `'Connection' object has no attribute 'cursor'` ao usar `df.to_sql`.  
**Solução:** Substituir o uso de `engine` ou `connection` por `engine.begin()` com `method='multi'`:

```python

with engine.begin() as conn:
    df.to_sql(table_name, con=conn, if_exists='append', index=False, method='multi')
```
### 6.4. Banco do Airflow Não Inicializado

**Erro:** `ERROR: You need to initialize the database. Please run` airflow db init``  
**Solução:** Adicionar serviço `airflow-init` com `command: db init` e dependência no webserver/scheduler.

### 6.5. Login no Airflow

**Problema:** Usuário padrão `airflow/airflow` não é criado automaticamente.  
**Solução:** Criar usuário manualmente dentro do container:

```bash

docker exec -it projeto-crypto-monitor-airflow-scheduler-1 bash
airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com
```

Ou via script no `airflow-init` (não recomendado para produção).

### 6.6. Erro de permissão no Docker

**Erro:** `permission denied while trying to connect to the Docker daemon socket`  
**Solução:** Adicionar usuário ao grupo `docker` e reiniciar sessão:

```bash

sudo usermod -aG docker $USER
newgrp docker
```
---

## 7. Adição do pgAdmin (Interface Gráfica)

Para facilitar a visualização dos dados, adicionamos o serviço `pgadmin` no `docker-compose.yml`:

```yaml

pgadmin:
  image: dpage/pgadmin4
  container_name: crypto_pgadmin
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@admin.com
    PGADMIN_DEFAULT_PASSWORD: admin
  ports:
    - "5050:80"
  depends_on:
    - postgres

Acesso: [http://localhost:5050](http://localhost:5050)  
Login: `admin@admin.com` / senha: `admin`  
Conexão com o banco: host=`postgres`, usuário e senha conforme `.env`.
```
---

## 8. Testes e Validação

- Execução manual do pipeline: `docker compose run --rm app`
    
- Execução via Airflow: ativar DAG e acionar manualmente ("Trigger DAG").
    
- Verificação no pgAdmin: consultar tabela `precos_crypto` após cada execução.
    
- Logs da tarefa no Airflow (clicar na tarefa → "Log").
    

---

## 9. Agendamento e Ajustes Finais

- Para testar com frequência, alteramos `schedule_interval` para `'*/5 * * * *'` (a cada 5 minutos).
    
- Após testes, reverter para `'@hourly'` (ou o desejado).
    
- Reiniciar serviços após mudanças: `docker compose restart airflow-scheduler airflow-webserver`
    

---

## ✅ Checklist Final

- Dockerfile.airflow criado e imagem construída
    
- Serviços do Airflow adicionados ao docker-compose
    
- DAG criada e reconhecida pelo Airflow
    
- Conflito de SQLAlchemy resolvido
    
- Erro de `cursor` no `load.py` corrigido
    
- Banco do Airflow inicializado (`airflow db init`)
    
- Usuário admin criado e login funcional
    
- pgAdmin integrado para visualização
    
- Pipeline executando agendado e inserindo dados
