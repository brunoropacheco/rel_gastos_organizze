# Análise de API Organizze

Este projeto realiza a análise de transações financeiras utilizando a API do Organizze. Ele classifica as despesas em categorias, gera gráficos e envia um e-mail com um resumo das despesas.

## Estrutura do Projeto

- 

analise_api_organizze.py

: Script principal que realiza a análise das transações.
- 

requirements.txt

: Lista de dependências do projeto.
- 

.gitignore

: Arquivo que especifica quais arquivos e diretórios devem ser ignorados pelo Git.
- 

README.md

: Este arquivo.

## Dependências

As dependências do projeto estão listadas no arquivo 

requirements.txt

. Para instalá-las, execute:

```sh
pip install -r requirements.txt
```

## Configuração

Antes de executar o script, você precisa definir algumas variáveis de ambiente:

- `TOKEN_ORGANIZZE`: Token de autenticação para a API do Organizze.
- `API_MAILTRAP`: Token de autenticação para o Mailtrap.

## Execução

Para executar o script, utilize o seguinte comando:

```sh
python analise_api_organizze.py
```

## Funcionalidades

O script realiza as seguintes etapas:

1. Verifica a presença da variável de ambiente `TOKEN_ORGANIZZE`.
2. Configura os cabeçalhos para as requisições à API.
3. Define os IDs das contas do Itau e Santander.
4. Constrói a URL base e o intervalo de datas para buscar as transações.
5. Busca as faturas das contas do Itau e Santander.
6. Verifica e recupera a fatura atual de cada conta.
7. Busca as transações das faturas atuais.
8. Filtra as transações para manter apenas as chaves relevantes.
9. Cria dataframes para as transações do Itau e Santander e as concatena.
10. Ajusta o dataframe e salva em um arquivo CSV.
11. Agrupa as transações por categoria e calcula o valor total e os limites.
12. Envia um e-mail com os dados agrupados e os valores totais.

## Contato

Para mais informações, entre em contato com [seu email].

---

Você pode ajustar o conteúdo conforme necessário para melhor atender às suas necessidades.