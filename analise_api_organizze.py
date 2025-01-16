import pandas as pd
import matplotlib.pyplot as plt
import datetime
import requests
import smtplib
import os
import re
from json import loads
import numpy as np

def ajustar_dataframe(df):
    # Ajusta os caracteres da coluna 'Descricao' e 'Tipo'
    df['description'] = ajusta_caracteres(df['description'])
    
    # Ajusta os caracteres da coluna 'Valor'
    df['Valor'] = df['amount_cents'] / 100.0

    #apagar coluna amount_cents
    df = df.drop(columns=['amount_cents'])
    
    # Aplica a função para criar a nova coluna 'Categoria'
    df['Categoria'] = df['description'].apply(classificar_despesa)

    #apagar a linha que contem a seguinte cadeia de caracteres 'deb._autom._de_fatura'
    df = df[~df['description'].str.contains('deb._autom._de_fatura')]

    return df

def criar_grafico(df):
    # Agrupa por categoria e soma os valores
    df_grouped = df.groupby('Categoria')['Valor'].sum()

    # Cria o gráfico de barras
    df_grouped.plot(kind='bar')

    # Define o título e os rótulos dos eixos
    plt.title('Despesas por Categoria')
    plt.xlabel('Categoria')
    plt.ylabel('Valor')
    plt.savefig('despesas_por_categoria.png')

    # Mostra o gráfico
    plt.show()

def enviar_email_mailtrap(df_grouped, total):
    sender = "Alerta Gastos <mailtrap@demomailtrap.com>"
    receiver = "Gmail Bruno <brunoropacheco@gmail.com>"

    message = f"""\
Subject: Hi Mailtrap
To: {receiver}
From: {sender}

Data: {datetime.datetime.now().strftime('%d/%m/%Y')}
Despesas por Categoria:
{df_grouped}

Total: R$ {total}
"""
    #Total: R$ {total}
    print(message)
    
    with smtplib.SMTP("live.smtp.mailtrap.io", 587) as server:
        server.starttls()
        server.login("api", os.getenv('API_MAILTRAP'))
        server.sendmail(sender, receiver, message)
    

def extrair_transacoes(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                linhas = f.readlines()
            
            transacoes = []
            for linha in linhas:
                if re.match(r'\d{2}\.\d{2}\.\d{4}', linha):
                    transacoes.append(linha.strip().split(';'))

            return transacoes

def ajusta_caracteres(coluna):
    mapeamento = {
        'á': 'a', 'ã': 'a', 'ç': 'c', 'é': 'e', 'ê': 'e', 'í': 'i', 'ó': 'o', 'õ': 'o', 'ú': 'u',
        '-': '_', ' ': '_'
    }
    for k, v in mapeamento.items():
        coluna = coluna.str.replace(k, v)
    return coluna.str.lower()

def classificar_despesa(descricao):
    # Crie uma função para classificar as despesas com base nos termos
    # Lógica de classificação
    if 'movida' in descricao or 'rentcars' in descricao or 'melia' in descricao or 'latam' in descricao or 'iberia' in descricao or 'unidas' in descricao or 'airbnb' in descricao or 'azul' in descricao or 'smiles' in descricao or 'gol' in descricao or 'city_hall' in descricao or 'foco_aluguel' in descricao or 'tam_lin' in descricao:
        return 'viagem'
    elif 'rede_economia' in descricao or 'sam_s_club' in descricao or 'buffet' in descricao or 'hortifruti' in descricao or 'mercado_' in descricao or 'pao_de_açucar' in descricao or 'mercear' in descricao or 'hermon' in descricao or 'tempero' in descricao or 'alimento' in descricao or 'padar' in descricao or 'depos' in descricao or 'sams' in descricao or 'assai' in descricao or 'pao_de' in descricao or 'lulu' in descricao or 'frutas' in descricao:
        return 'alimentacao_casa'
    elif 'centro_automotivo_pend' in descricao or 'uber' in descricao or 'pop_' in descricao or '99_tecnologia' in descricao or 'hdi' in descricao or '99app' in descricao or 'estaciona' in descricao or 'posto' in descricao or 'conectcar' in descricao or 'tembici' in descricao or 'park' in descricao or 'barcas' in descricao or 'digipare' in descricao or 'auto_pos' in descricao:
        return 'transporte'
    elif 'roupas' in descricao or 'panna' in descricao or 'assb_comerci' in descricao or 'toy_boy' in descricao or 'kop' in descricao or 'happy' in descricao or 'presente' in descricao or 'daiso' in descricao or 'picadilly' in descricao or 'elister_joias' in descricao or 'nestle_brasil_ltda' in descricao or 'arte_dos_vinhos' in descricao or 'riahcuelo' in descricao or 'americanas' in descricao or 'cell' in descricao or 'mundo_baby' in descricao or 'centauro' in descricao or 'cea' in descricao or 'renner' in descricao or 'pag*lojasrennersa' in descricao or 'iphone' in descricao or 'casa_e_vi' in descricao or 'relusa' in descricao or 'marketplace' in descricao or 'mr_cat' in descricao or 'cresci_e_perdi' in descricao or 'tonys_baby' in descricao or 'cirandinha_baby' in descricao or 'loungerie' in descricao or 'amazon' in descricao or 'shein' in descricao or 'calcad' in descricao or 'mercadolivre' in descricao:
        return 'compras'
    elif 'produtos_globo' in descricao or 'ilha_mix' in descricao or 'melimais' in descricao or 'netflix' in descricao or 'spotify' in descricao or 'apple.com/bill' in descricao or 'apple_com/bill' in descricao or 'primebr' in descricao or 'doist' in descricao:
        return 'servicos'
    elif 'dermage' in descricao or 'drog' in descricao or 'labora' in descricao:
        return 'saude'
    elif 'liberty' in descricao or 'calhas' in descricao or 'first_class' in descricao or 'chaveiro' in descricao or 'leroy' in descricao or 'lojas_g' in descricao or 'angela' in descricao or 'camica' in descricao or 'tok' in descricao or 'darkstore' in descricao:
        return 'casa'
    elif 'infne' in descricao or 'cisco' in descricao or 'rdmedicine' in descricao or 'papelaria' in descricao or 'livraria' in descricao or 'colegio' in descricao or 'saraiva' in descricao or 'cursos' in descricao or 'curso' in descricao or 'escola' in descricao or 'faculdade' in descricao or 'universidade' in descricao:
        return 'educacao'
    elif 'funcional' in descricao:
        return 'esporte'
    elif 'belarmino' in descricao or 'mcdonald' in descricao or 'burger' in descricao or 'subway' in descricao or 'kfc' in descricao or 'bobs' in descricao or 'outback' in descricao or 'pizza' in descricao or 'boulevard_go' in descricao or 'starbuc' in descricao or 'cookie' in descricao or 'cafe' in descricao or 'ex_touro' in descricao or 'beco_do_espa' in descricao or 'rockribs' in descricao or 'lanch' in descricao or 'suco' in descricao or 'megamatte' in descricao or 'chocolate' in descricao or 'rei_do_mate' in descricao or 'sunomono'  in descricao or 'drink' in descricao or 'convenie' in descricao or 'hot_dog' in descricao or 'rest' in descricao or 'food' in descricao or 'emporio' in descricao or 'bacio_di' in descricao or 'verdanna' in descricao or 'ifd' in descricao or 'comida_fora' in descricao or 'rio_arena' in descricao or 'beto_carrero' in descricao or 'ticket' in descricao or 'rio_Arena' in descricao or 'coffee' in descricao or 'casal_20' in descricao or 'panito' in descricao or 'sush' in descricao or 'sabor' in descricao or 'cheiro' in descricao or 'delicate' in descricao:
        return 'diversao-lazer-comida'    
    elif 'chic' in descricao or 'cabel' in descricao or 'sephora' in descricao or 'skin' in descricao or 'boticario' in descricao:
        return 'beleza' 
    elif 'anuid' in descricao:
        return 'anuidade'
    else:
        return 'outros'

def obter_faturas(headers, id_cartao, url_base, start_date, end_date):
        url_faturas = f"{url_base}credit_cards/{id_cartao}/invoices?start_date={start_date}&end_date={end_date}"
        response = requests.get(url_faturas, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

def verificar_fatura(faturas, dia_limite):
    hoje = datetime.datetime.now()
    if hoje.day <= dia_limite:
        mes = hoje.month
        ano = hoje.year
    else:
        mes = hoje.month + 1
        if mes > 12:
            mes = 1
            ano = hoje.year + 1
        else:
            ano = hoje.year

    for fatura in faturas:
        data_vencimento = datetime.datetime.strptime(fatura['date'], '%Y-%m-%d')
        if data_vencimento.year == ano and data_vencimento.month == mes:
            return fatura
    return None

def obter_transacoes_fatura(headers, id_cartao, id_fatura, url_base):
        url_transacoes = f"{url_base}credit_cards/{id_cartao}/invoices/{id_fatura}"
        response = requests.get(url_transacoes, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

def obter_transacoes_fatura_anterior(headers, id_cartao, id_fatura_atual, url_base, hoje):
    transacoes_anteriores = {}
    
    if 10 <= hoje.day <= 17:
        id_fatura_anterior = str(int(id_fatura_atual) - 1)
        url_transacoes = f"{url_base}credit_cards/{id_cartao}/invoices/{id_fatura_anterior}"
        response = requests.get(url_transacoes, headers=headers)
        
        if response.status_code == 200:
            transacoes = response.json()['transactions']
            
            for transacao in transacoes:
                if transacao['total_installments'] - transacao['installment'] > 0:
                    transacoes_anteriores[transacao['id']] = transacao
        else:
            response.raise_for_status()
    
    return transacoes_anteriores

def main():
    """
    Main function to fetch and process financial transactions from Organizze API.
    This function performs the following steps:
    1. Checks for the presence of the 'AUTHORIZATION_HEADER' environment variable.
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
    Raises:
        ValueError: If the 'AUTHORIZATION_HEADER' environment variable is missing.
    """

    token = os.getenv('TOKEN_ORGANIZZE')
    if not token:
        raise ValueError("Missing TOKEN_ORGANIZZE environment variable")

    headers = {
        'Authorization': f'Basic {token}'
    }

    id_itau_azul = '1654306'
    id_sant_aa = '1654312'

    url_base = "https://api.organizze.com.br/rest/v2/"
    hoje = datetime.datetime.now()
    start_date = (hoje - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
    end_date = (hoje + datetime.timedelta(days=90)).strftime('%Y-%m-%d')    

    faturas_itau = obter_faturas(headers, id_itau_azul, url_base, start_date, end_date)
    faturas_santander = obter_faturas(headers, id_sant_aa, url_base, start_date, end_date)

    fatura_atual_itau = verificar_fatura(faturas_itau, 10)
    fatura_atual_santander = verificar_fatura(faturas_santander, 10)

    id_fatura_itau = fatura_atual_itau['id']
    id_fatura_santander = fatura_atual_santander['id']
    
    transacoes_itau = obter_transacoes_fatura(headers, id_itau_azul, id_fatura_itau, url_base)
    transacoes_santander = obter_transacoes_fatura(headers, id_sant_aa, id_fatura_santander, url_base)

    transacoes_anteriores_itau = obter_transacoes_fatura_anterior(headers, id_itau_azul, id_fatura_itau, url_base, hoje)
    transacoes_anteriores_santander = obter_transacoes_fatura_anterior(headers, id_sant_aa, id_fatura_santander, url_base, hoje)

    transacoes_itau['transactions'] += list(transacoes_anteriores_itau.values())
    transacoes_santander['transactions'] += list(transacoes_anteriores_santander.values())

    transacoes_itau = transacoes_itau['transactions']
    transacoes_santander = transacoes_santander['transactions']

    for transacao in transacoes_itau:
        keys_to_keep = ['description', 'date', 'amount_cents', 'total_installments', 'installment']
        for key in list(transacao.keys()):
            if key not in keys_to_keep:
                del transacao[key]

    for transacao in transacoes_santander:
        keys_to_keep = ['description', 'date', 'amount_cents', 'total_installments', 'installment']
        for key in list(transacao.keys()):
            if key not in keys_to_keep:
                del transacao[key]

    df_itau = pd.DataFrame(transacoes_itau)
    df_santander = pd.DataFrame(transacoes_santander)

    df = pd.concat([df_itau, df_santander], ignore_index=True)
    df = ajustar_dataframe(df)

    df.to_csv('transacoes_ajustado.csv')
    #criar_grafico(df)
    df_grouped = df.groupby('Categoria')['Valor'].sum().reset_index()
    limites = {
        'alimentacao_casa': 500,
        'transporte': 1650,
        'saude': 300,
        'casa': 500,
        'educacao': 2150,
        'esporte': 50,
        'diversao-lazer-comida': 500,
        'beleza': 200,
        'anuidade': 150,
        'outros': 200,
        'compras': 800,
        'servicos': 75,
        'viagem': 2000
    }
    df_grouped['Limite'] = df_grouped['Categoria'].map(limites)
    df_grouped['Limite'] = df_grouped['Limite'].replace(0, np.nan)
    #coluna porcentagem
    df_grouped['Porcentagem'] = df_grouped['Valor'] / df_grouped['Limite']
    #imprimir o total no email
    print(df_grouped)
    enviar_email_mailtrap(df_grouped, df_grouped.sum())
    print("Email enviado com sucesso")

if __name__ == "__main__":
    main()
