# Relatório de Gastos de Cartão de Crédito

Este projeto automatiza a análise de transações financeiras dos cartões de crédito associados ao aplicativo Organizze utilizando sua API. O script principal calcula os gastos totais, compara com limites pré-definidos por categoria e pode enviar um e-mail contendo um resumo detalhado das despesas.

## Estrutura do Projeto

- **`/src/analise_api_organizze.py`**: Script principal que realiza toda a análise das transações.
- **`requirements.txt`**: Lista de dependências do projeto.
- **`.gitignore`**: Arquivo que especifica quais arquivos e diretórios devem ser ignorados pelo Git.
- **`README.md`**: Este arquivo de documentação.
- **`fluxo.drawio`**: Diagrama que ilustra o fluxo de execução do script.
- **`migration/`**: Diretório contendo scripts SQL para migrações.
- **`tests/`**: Diretório contendo testes do projeto.

## Dependências

O projeto depende das seguintes bibliotecas Python (listadas em `requirements.txt`):
- pandas
- requests
- dateutil
- smtplib
- numpy
- google-api-python-client
- google-auth
- google-auth-oauthlib

Para instalar todas as dependências, execute:

```sh
pip install -r requirements.txt
```

## Configuração

Antes de executar o script, defina as seguintes variáveis de ambiente:

- `TOKEN_ORGANIZZE`: Token de autenticação para a API do Organizze.
- `PASSWORD_GMAIL`: Senha de aplicativo para o Gmail (usado para enviar o relatório por e-mail).
- `GOOGLE_DRIVE_CREDENTIALS`: JSON string com as credenciais do service account do Google para acessar o Google Drive e Sheets (usado para carregar limites de categorias).

## Execução

Para executar o script, utilize:

```sh
python src/analise_api_organizze.py
```

## Fluxo de Execução

O arquivo `fluxo.drawio` contém um diagrama do fluxo do script. Abra com [draw.io](https://app.diagrams.net/) ou extensões compatíveis do VS Code.

## Funcionalidades Detalhadas

O script realiza as seguintes operações:

1. **Autenticação na API Organizze**
   - Obtém o token de autenticação da variável de ambiente.
   - Configura os cabeçalhos HTTP para as requisições.

2. **Obtenção de Dados dos Cartões**
   - Identifica os IDs dos cartões cadastrados na plataforma Organizze.
   - Determina o intervalo de datas para análise (últimos 365 dias até 60 dias à frente).

3. **Processamento de Faturas**
   - Busca as faturas dos cartões Itaú e Santander dentro do intervalo definido.
   - Identifica a fatura atual de cada cartão com base na data de vencimento.
   - Obtém as transações das faturas atuais.

4. **Tratamento de Compras Parceladas**
   - O script processa apenas as transações que já estão alocadas na fatura atual.
   - **IMPORTANTE**: Transações parceladas com parcelas futuras precisam ser movidas manualmente no Organizze para a fatura atual sempre que a fatura virar. A API do Organizze não permite mover automaticamente parcelas entre faturas, por isso é necessário fazer isso manualmente na interface do Organizze.

5. **Processamento de Dados**
   - Processa as transações atuais em um DataFrame.
   - Remove duplicatas considerando descrição, data e valor.
   - Mantém apenas as colunas relevantes para análise.

6. **Carregamento de Limites de Categorias**
   - O script tenta carregar os limites de gastos por categoria de uma planilha do Google Sheets chamada 'Financas2026' na aba 'Limites'.
   - Os limites são lidos da coluna A (categorias) e coluna B (valores), começando da linha 1.
   - Se a planilha não for encontrada ou houver erro na autenticação, o script usa limites padrão hardcoded.

7. **Análise e Categorização**
   - Identifica transações parceladas e aquelas na última parcela.
   - Agrupa transações por categoria.
   - Compara gastos com os limites carregados (do Google Sheets ou padrão).

8. **Geração de Saídas**
   - Salva as transações processadas em arquivos CSV (`transacoes_atuais.csv`, `transacoes_passadas.csv`, `transacoes_ajustado.csv`).
   - (Opcional) Envia um e-mail com uma tabela detalhada dos gastos por categoria, incluindo:
     - Valor total gasto
     - Limite por categoria (carregado do Google Sheets ou padrão)
     - Porcentagem do limite utilizado
     - Quantidade de transações parceladas
     - Quantidade de transações na última parcela

## Exemplo de Uso

Após configurar as variáveis de ambiente e instalar as dependências, basta rodar o script principal. Os arquivos CSV gerados podem ser abertos com o Excel ou extensões de edição de CSV no VS Code para análise detalhada.

## Contato

Para mais informações, entre em contato com brunoropacheco@gmail.com.

---

**Nota:** Este README foi ajustado para refletir o funcionamento do código atual. Atualize conforme necessário para atender suas necessidades específicas.
