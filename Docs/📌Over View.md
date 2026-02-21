
Este projeto implementa um pipeline de dados ETL (Extract, Transform, Load) para monitorar criptomoedas utilizando a API pública da CoinGecko. Os dados são extraídos, tratados e carregados em um banco PostgreSQL rodando em container Docker. O projeto foi desenvolvido como portfólio para a área de engenharia de dados, demonstrando boas práticas como modularização, tratamento de erros, logging, uso de variáveis de ambiente, containerização e testes automatizados.

### Cobertura Atual
- `extract.py`: ~91%
- `load.py`: ~87%
- `config.py`: ~33% (depende de variáveis reais, pode ser melhorado com mocks)
- **Total:** ~66%

## 📚 Conceitos Aplicados

- **ETL (Extract, Transform, Load):** Separação clara das responsabilidades.
- **Auditoria:** Coluna `extracted_at` em cada registro.
- **Tratamento de Erros:** Captura de exceções específicas e mensagens amigáveis.
- **Logging:** Uso do módulo `logging` para registro de eventos.
- **Configuração por ambiente:** Uso de `.env` e `get_engine`.
- **Containerização:** PostgreSQL em Docker, com volume para persistência.
- **Testes automatizados:** Testes unitários com mocks, fixtures e cobertura.
- **Boas práticas de código:** Modularização, nomes descritivos, docstrings.

## Sumário

1. [[⚙️ Configuração do Ambiente (Fedora Linux)]]
2. [[📁 Estrutura do Projeto]]
3. [[🔄 Fluxo de Dados (ETL)]] 
4. [[🐳 Docker e Banco de Dados]]
5. [[Testes automatizados]]
6. [[🔐 Variáveis de Ambiente (.env)]]
7. [[🚀 Como Executar o Pipeline]]
