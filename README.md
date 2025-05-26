# Relatório de Gastos de Cartão de Crédito

Este projeto automatiza a análise de transações financeiras dos cartões de crédito associados ao aplicativo Organizze utilizando sua API. O script principal classifica despesas em categorias, calcula os gastos totais, compara com limites pré-definidos por categoria e envia um e-mail contendo um resumo detalhado das despesas.

## Estrutura do Projeto

- **`/src/analise_api_organizze.py`**: Script principal que realiza a análise das transações.
- **`requirements.txt`**: Lista de dependências do projeto.
- **`.gitignore`**: Arquivo que especifica quais arquivos e diretórios devem ser ignorados pelo Git.
- **`README.md`**: Este arquivo de documentação.
- **`fluxo.drawio`**: Diagrama que ilustra o fluxo de execução do script.
- **`migration/`**: Diretório contendo scripts SQL para migrações.
- **`tests/`**: Diretório contendo testes do projeto.

## Dependências

O projeto depende de várias bibliotecas Python listadas no arquivo `requirements.txt`, incluindo:
- pandas
- matplotlib
- requests
- mysql-connector-python
- numpy

Para instalar todas as dependências, execute:

```sh
pip install -r requirements.txt
```

## Configuração

Antes de executar o script, você precisa definir as seguintes variáveis de ambiente:

- `TOKEN_ORGANIZZE`: Token de autenticação para a API do Organizze.
- `PASSWORD_GMAIL`: Senha de aplicativo para o Gmail (usado para enviar o relatório por e-mail).

## Execução

Para executar o script, utilize o seguinte comando:

```sh
python src/analise_api_organizze.py
```

## Fluxo de Execução

O arquivo `fluxo.drawio` contém um diagrama que ilustra o fluxo de execução do script. Você pode abrir este arquivo usando o [draw.io](https://app.diagrams.net/) ou extensões compatíveis do VS Code para visualizar o fluxograma completo.

## Funcionalidades Detalhadas

O script realiza as seguintes operações:

1. **Autenticação na API Organizze**:
   - Obtém o token de autenticação da variável de ambiente.
   - Configura os cabeçalhos HTTP para as requisições.

2. **Obtenção de Dados de Cartões**:
   - Identifica os IDs dos cartões cadastrados na plataforma Organizze.
   - Determina o intervalo de datas para análise (90 dias antes e depois da data atual).

3. **Processamento de Faturas**:
   - Busca as faturas dos cartões (Itaú e Santander) dentro do intervalo definido.
   - Identifica a fatura atual para cada cartão com base na data de vencimento.
   - Obtém as transações das faturas atuais.

4. **Tratamento de Compras Parceladas**:
   - Busca transações parceladas de faturas anteriores que ainda impactam a fatura atual.
   - Ajusta o número da parcela para refletir corretamente na fatura atual.
   - Elimina duplicidades entre transações de faturas anteriores e atuais.

5. **Processamento de Dados**:
   - Filtra e mantém apenas os campos relevantes das transações.
   - Converte os dados para um DataFrame do pandas.
   - Ajusta caracteres especiais e formata valores monetários.

6. **Análise e Categorização**:
   - Identifica transações parceladas e aquelas na última parcela.
   - Agrupa transações por categoria.
   - Compara gastos com limites pré-definidos por categoria.

7. **Geração de Saídas**:
   - Salva as transações processadas em um arquivo CSV (`transacoes_ajustado.csv`).
   - Envia um e-mail com uma tabela detalhada dos gastos por categoria, incluindo:
     - Valor total gasto
     - Limite por categoria
     - Porcentagem do limite utilizado
     - Quantidade de transações parceladas
     - Quantidade de transações na última parcela

## Contato

Para mais informações, entre em contato com brunoropacheco@gmail.com.

---

Nota: Este README foi atualizado para refletir o estado atual do código. Ajuste-o conforme necessário para atender suas necessidades específicas.
