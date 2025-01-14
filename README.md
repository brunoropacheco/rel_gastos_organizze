# rel_gastos_organizze

### README for `analise_api_organizze.py`

## Overview
This script fetches and processes financial transactions from the Organizze API. It performs the following steps:
1. Checks for the presence of the `TOKEN_ORGANIZZE` environment variable.
2. Sets up the headers for API requests.
3. Defines account IDs for Itau and Santander.
4. Constructs the base URL and date range for fetching transactions.
5. Fetches invoices for Itau and Santander accounts.
6. Verifies and retrieves the current invoice for each account.
7. Fetches transactions for the current invoices.
8. Filters transactions to keep only relevant keys.
9. Creates dataframes for Itau and Santander transactions and concatenates them.
10. Adjusts the dataframe and saves it to a CSV file.
11. Groups transactions by category and calculates the total value and limits.
12. Sends an email with the grouped data and total values.

## Requirements
- Python 3.x
- Pandas
- Matplotlib
- Requests
- smtplib
- re
- json
- datetime
- numpy
- Environment variables: `TOKEN_ORGANIZZE`, `API_MAILTRAP`

## How to Run
1. Ensure all required libraries are installed.
2. Set the environment variables `TOKEN_ORGANIZZE` and `API_MAILTRAP`.
3. Execute the script:
   ```bash
   python analise_api_organizze.py
   ```

## Functions
### ajustar_dataframe(df)
Adjusts the dataframe by:
- Updating the `description` and `amount_cents` columns.
- Removing unnecessary columns and rows.

### criar_grafico(df)
Creates and displays a bar chart of expenses by category.

### enviar_email_mailtrap(df_grouped, total)
Sends an email with the grouped data and total values using Mailtrap.

### extrair_transacoes(arquivo)
Extracts transactions from a file.

### ajusta_caracteres(coluna)
Adjusts special characters in the dataframe.

### classificar_despesa(descricao)
Classifies expenses based on specific terms in the description.

### obter_faturas(headers, id_cartao, url_base, start_date, end_date)
Fetches invoices from the Organizze API.

### verificar_fatura(faturas, dia_limite)
Verifies and retrieves the current invoice for an account.

### obter_transacoes_fatura(headers, id_cartao, id_fatura, url_base)
Fetches transactions for a specific invoice.

### main()
Main function to fetch and process financial transactions from Organizze API.

## Repository Information
- Repository: [brunoropacheco/rel_gastos_organizze](https://github.com/brunoropacheco/rel_gastos_organizze)
- Language: Python
- Visibility: Public

Feel free to update this README with any additional information or instructions specific to your use case.
