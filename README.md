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

Para instalar todas as dependências, execute:

```sh
pip install -r requirements.txt
```

## Configuração

Antes de executar o script, defina as seguintes variáveis de ambiente:

- `TOKEN_ORGANIZZE`: Token de autenticação para a API do Organizze.
- `PASSWORD_GMAIL`: Senha de aplicativo para o Gmail (usado para enviar o relatório por e-mail).

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
   - Busca transações parceladas de faturas anteriores que ainda podem impactar a fatura atual.
   - Só considera transações em que alguma parcela pode cair na fatura atual (baseado na data da compra e número de parcelas).
   - Elimina duplicidades entre transações de faturas anteriores e atuais, mantendo a de maior parcela.

5. **Processamento de Dados**
   - Junta transações atuais e passadas em um único DataFrame.
   - Remove duplicatas considerando descrição, data e valor, mantendo o maior número de parcela.
   - Mantém apenas as colunas relevantes para análise.

6. **Análise e Categorização**
   - Identifica transações parceladas e aquelas na última parcela.
   - Agrupa transações por categoria.
   - Compara gastos com limites pré-definidos por categoria.

7. **Geração de Saídas**
   - Salva as transações processadas em arquivos CSV (`transacoes_atuais.csv`, `transacoes_passadas.csv`, `transacoes_ajustado.csv`).
   - (Opcional) Envia um e-mail com uma tabela detalhada dos gastos por categoria, incluindo:
     - Valor total gasto
     - Limite por categoria
     - Porcentagem do limite utilizado
     - Quantidade de transações parceladas
     - Quantidade de transações na última parcela

## Exemplo de Uso

Após configurar as variáveis de ambiente e instalar as dependências, basta rodar o script principal. Os arquivos CSV gerados podem ser abertos com o Excel ou extensões de edição de CSV no VS Code para análise detalhada.

## Contato

Para mais informações, entre em contato com brunoropacheco@gmail.com.

---

**Nota:** Este README foi ajustado para refletir o funcionamento do código atual. Atualize conforme necessário para atender suas necessidades específicas.
