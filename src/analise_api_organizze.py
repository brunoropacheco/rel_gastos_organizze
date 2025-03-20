import pandas as pd
import matplotlib.pyplot as plt
import datetime
import requests
import smtplib
import os
import re

def ajustar_dataframe(df):
    """
    Ajusta e processa um DataFrame contendo dados de transações financeiras.
    Argumentos:
        df (pd.DataFrame): O DataFrame de entrada com as seguintes colunas:
            - 'description' (str): Descrição da transação.
            - 'amount_cents' (int): Valor da transação em centavos.
    Retorna:
        pd.DataFrame: Um DataFrame processado com os seguintes ajustes:
            - A coluna 'description' é processada usando a função `ajusta_caracteres`.
            - Uma nova coluna 'Valor' é adicionada, representando o valor da transação em reais (convertido de 'amount_cents').
            - A coluna 'amount_cents' é removida.
            - Uma nova coluna 'Categoria' é adicionada, categorizando as transações com base na coluna 'description' usando a função `classificar_despesa`.
            - Linhas coringa são adicionadas para categorias predefinidas que estão ausentes na coluna 'Categoria', com 'description' definido como 'coringa' e 'Valor' definido como 0.
            - Linhas contendo a string 'deb._autom._de_fatura' na coluna 'description' são removidas.
    """
    # Ajusta os caracteres da coluna 'Descricao' e 'Tipo'
    df['description'] = ajusta_caracteres(df['description'].astype(str))
    
    # Ajusta os caracteres da coluna 'Valor'
    df['Valor'] = df['amount_cents'] / 100.0

    #apagar coluna amount_cents
    df = df.drop(columns=['amount_cents'])
    
    # Aplica a função para criar a nova coluna 'Categoria'
    df['Categoria'] = df['description'].apply(classificar_despesa)

    # Adiciona transações coringa para categorias sem valor
    categorias = ['viagem', 'alimentacao_casa', 'seguro_carro', 'transp(ub+gas+vel+ccr)', 'compras', 'assinaturas', 'saude', 'casa', 'educacao', 'esporte', 'diversao-lazer-comida', 'beleza', 'anuidade', 'outros']
    new_rows = []
    for categoria in categorias:
        if categoria not in df['Categoria'].values:
            new_rows.append({'description': 'coringa', 'Valor': 0, 'Categoria': categoria})
    if new_rows:
        df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)

    #apagar a linha que contem a seguinte cadeia de caracteres 'deb._autom._de_fatura'
    df = df[~df['description'].str.contains('deb._autom._de_fatura')]

    return df

def enviar_email(df_grouped, total, total_limite, qtde_parcelado, qtde_ultima_parcela):
    """
    Envia um e-mail com um relatório detalhado de despesas por categoria.
    Argumentos:
        df_grouped (pd.DataFrame): Um DataFrame contendo os dados agrupados de despesas com as colunas 
                                   'Categoria', 'Valor', 'Limite' e 'Porcentagem'.
        total (float): O valor total gasto.
        total_limite (float): O limite total disponível.
        qtde_parcelado (int): A quantidade de transações parceladas.
        qtde_ultima_parcela (int): A quantidade de transações que estão na última parcela.
    Retorna:
        None
    """
    sender = 'brunoropacheco@gmail.com'
    #receiver = "Gmail Bruno <brunoropacheco@gmail.com>;<bruno.rpacheco@transpetro.com.br>;<mariliaampereira@gmail.com>"
    receiver = ['brunoropacheco@gmail.com']
    password = os.getenv('PASSWORD_GMAIL')
    message = f"""\
Subject: Relatorio de Gastos de Cartoes
To: {receiver}
From: {sender}
Content-Type: text/html

<html>
  <body>
    <p>Data: {datetime.datetime.now().strftime('%d/%m/%Y')}</p>
    <h2>Despesas por Categoria:</h2>
    <table border="1">
      <tr>
        <th>Categoria</th>
        <th>Valor</th>
        <th>Limite</th>
        <th>Porcentagem</th>
      </tr>
      {''.join(f'<tr><td>{row["Categoria"]}</td><td>{row["Valor"]}</td><td>{row["Limite"]}</td><td>{row["Porcentagem"]}</td></tr>' for _, row in df_grouped.iterrows())}
    </table>
    <p>Total Utilizado: R$ {total}</p>
    <p>Total Limite: R$ {total_limite}</p>
    <p>Quantidade de transacoes parceladas: {qtde_parcelado}</p>
    <p>Quantidade de transacoes na ultima parcela: {qtde_ultima_parcela}</p>
  </body>
</html>
"""
    #Total: R$ {total}
    print(message)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Inicia a conexão TLS
        server.login(sender, password)  # Faz login com o e-mail e senha do aplicativo
        server.sendmail(sender, receiver, message)  # Envia o e-mail

def extrair_transacoes(arquivo):
    """
    Extrai transações de um arquivo de texto.
    Esta função lê um arquivo de texto contendo transações, onde cada linha
    representa uma transação. As linhas que começam com uma data no formato
    'dd.mm.aaaa' são consideradas válidas e são processadas. Cada transação
    é separada por ponto e vírgula (';') e retornada como uma lista de listas.
    Args:
        arquivo (str): O caminho para o arquivo de texto contendo as transações.
    Returns:
        list: Uma lista de listas, onde cada sublista representa uma transação
        extraída do arquivo.
    """
    with open(arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    transacoes = []
    for linha in linhas:
        if re.match(r'\d{2}\.\d{2}\.\d{4}', linha):
            transacoes.append(linha.strip().split(';'))

    return transacoes

def ajusta_caracteres(coluna):
    """
    Ajusta os caracteres de uma coluna de texto substituindo caracteres especiais 
    por seus equivalentes sem acentuação, além de substituir espaços e hifens por 
    underscores. Também converte todo o texto para letras minúsculas.

    Args:
        coluna (pd.Series): Série do pandas contendo os textos a serem ajustados.

    Returns:
        pd.Series: Série do pandas com os textos ajustados.
    """
    mapeamento = {
        'á': 'a', 'ã': 'a', 'ç': 'c', 'é': 'e', 'ê': 'e', 'í': 'i', 'ó': 'o', 'õ': 'o', 'ú': 'u',
        '-': '_', ' ': '_'
    }
    for k, v in mapeamento.items():
        coluna = coluna.str.replace(k, v)
    return coluna.str.lower()

def classificar_despesa(descricao):
    """
    Classifica uma despesa com base em sua descrição.

    A função analisa a descrição fornecida e retorna uma categoria correspondente
    à despesa, como 'viagem', 'alimentacao_casa', 'seguro_carro', entre outras.
    Caso a descrição não corresponda a nenhuma das categorias predefinidas, a
    função retorna 'outros'.

    Parâmetros:
        descricao (str): A descrição da despesa.

    Retorna:
        str: A categoria da despesa.
    """
    # Crie uma função para classificar as despesas com base nos termos
    # Lógica de classificação
    if 'movida' in descricao or 'rentcars' in descricao or 'melia' in descricao or 'latam' in descricao or 'iberia' in descricao or 'unidas' in descricao or 'airbnb' in descricao or 'azul' in descricao or 'smiles' in descricao or 'gol' in descricao or 'city_hall' in descricao or 'foco_aluguel' in descricao or 'tam_lin' in descricao:
        return 'viagem'
    elif 'hfruti_dcm' in descricao or 'dom_atacadista' in descricao or 'rede_economia' in descricao or 'sam_s_club' in descricao or 'buffet' in descricao or 'hortifruti' in descricao or 'mercado_' in descricao or 'pao_de_açucar' in descricao or 'mercear' in descricao or 'hermon' in descricao or 'tempero' in descricao or 'alimento' in descricao or 'padar' in descricao or 'depos' in descricao or 'sams' in descricao or 'assai' in descricao or 'pao_de' in descricao or 'lulu' in descricao or 'frutas' in descricao:
        return 'alimentacao_casa'
    elif 'hdi' in descricao:
        return 'seguro_carro'
    elif 'centro_automotivo_pend' in descricao or 'uber' in descricao or 'pop_' in descricao or '99_tecnologia' in descricao or '99app' in descricao or 'estaciona' in descricao or 'posto' in descricao or 'conectcar' in descricao or 'tembici' in descricao or 'park' in descricao or 'barcas' in descricao or 'digipare' in descricao or 'auto_pos' in descricao:
        return 'transp(ub+gas+vel+ccr)'
    elif 'pantys' in descricao or 'borelli_niteroi' in descricao or 'relusa' in descricao or 'lojas_g' in descricao or 'roupas' in descricao or 'panna' in descricao or 'assb_comerci' in descricao or 'toy_boy' in descricao or 'kop' in descricao or 'happy' in descricao or 'presente' in descricao or 'daiso' in descricao or 'picadilly' in descricao or 'elister_joias' in descricao or 'nestle_brasil_ltda' in descricao or 'arte_dos_vinhos' in descricao or 'riachuelo' in descricao or 'americanas' in descricao or 'cell' in descricao or 'mundo_baby' in descricao or 'centauro' in descricao or 'cea' in descricao or 'renner' in descricao or 'pag*lojasrennersa' in descricao or 'iphone' in descricao or 'casa_e_vi' in descricao or 'relusa' in descricao or 'marketplace' in descricao or 'mr_cat' in descricao or 'cresci_e_perdi' in descricao or 'tonys_baby' in descricao or 'cirandinha_baby' in descricao or 'loungerie' in descricao or 'amazon' in descricao or 'shein' in descricao or 'calcad' in descricao or 'mercadolivre' in descricao or 'compras' in descricao:
        return 'compras'
    elif 'produtos_globo' in descricao or 'ilha_mix' in descricao or 'melimais' in descricao or 'netflix' in descricao or 'spotify' in descricao or 'apple.com/bill' in descricao or 'apple_com/bill' in descricao or 'primebr' in descricao or 'doist' in descricao:
        return 'assinaturas'
    elif 'saude' in descricao or 'dermage' in descricao or 'drog' in descricao or 'labora' in descricao:
        return 'saude'
    elif 'midea' in descricao or 'calhas' in descricao or 'first_class' in descricao or 'chaveiro' in descricao or 'leroy' in descricao or 'angela' in descricao or 'camica' in descricao or 'tok' in descricao or 'darkstore' in descricao or 'obras_casa' in descricao or 'eletrodomestico' in descricao:
        return 'casa'
    elif 'dne' in descricao or 'educacao' in descricao or 'infne' in descricao or 'cisco' in descricao or 'rdmedicine' in descricao or 'papelaria' in descricao or 'livraria' in descricao or 'colegio' in descricao or 'saraiva' in descricao or 'cursos' in descricao or 'curso' in descricao or 'escola' in descricao or 'faculdade' in descricao or 'universidade' in descricao:
        return 'educacao'
    elif 'academia' in descricao or 'atividade_fisica' in descricao or 'funcional' in descricao or 'esportes' in descricao:
        return 'esporte'
    elif 'cheirin_bao' in descricao or 'belarmino' in descricao or 'mcdonald' in descricao or 'burger' in descricao or 'subway' in descricao or 'kfc' in descricao or 'bobs' in descricao or 'outback' in descricao or 'pizza' in descricao or 'boulevard_go' in descricao or 'starbuc' in descricao or 'cookie' in descricao or 'cafe' in descricao or 'ex_touro' in descricao or 'beco_do_espa' in descricao or 'rockribs' in descricao or 'lanch' in descricao or 'suco' in descricao or 'megamatte' in descricao or 'chocolate' in descricao or 'rei_do_mate' in descricao or 'sunomono'  in descricao or 'drink' in descricao or 'convenie' in descricao or 'hot_dog' in descricao or 'rest' in descricao or 'food' in descricao or 'emporio' in descricao or 'bacio_di' in descricao or 'verdanna' in descricao or 'ifd' in descricao or 'comida_fora' in descricao or 'rio_arena' in descricao or 'beto_carrero' in descricao or 'ticket' in descricao or 'rio_Arena' in descricao or 'coffee' in descricao or 'casal_20' in descricao or 'panito' in descricao or 'sush' in descricao or 'sabor' in descricao or 'cheiro' in descricao or 'delicate' in descricao or 'art_cafe_lapa' in descricao:
        return 'diversao-lazer-comida'    
    elif 'natura___propria' in descricao or 'maboltt' in descricao or 'chic' in descricao or 'cabel' in descricao or 'sephora' in descricao or 'skin' in descricao or 'boticario' in descricao or '_beleza' in descricao:
        return 'beleza' 
    elif 'anuid' in descricao:
        return 'anuidade'
    else:
        return 'outros'
    
def obter_faturas(headers, id_cartao, url_base, start_date, end_date):
    """
    Obtém as faturas de um cartão de crédito em um intervalo de datas específico.

    Args:
        headers (dict): Cabeçalhos HTTP necessários para autenticação na API.
        id_cartao (str): Identificador único do cartão de crédito.
        url_base (str): URL base da API Organizze.
        start_date (str): Data de início do intervalo no formato 'YYYY-MM-DD'.
        end_date (str): Data de término do intervalo no formato 'YYYY-MM-DD'.

    Returns:
        list: Uma lista de faturas no formato JSON retornada pela API.

    Raises:
        HTTPError: Caso a resposta da API retorne um código de status diferente de 200.
    """
    url_faturas = f"{url_base}credit_cards/{id_cartao}/invoices?start_date={start_date}&end_date={end_date}"
    response = requests.get(url_faturas, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def verificar_fatura(faturas, dia_limite):
    """
    Verifica se há uma fatura com vencimento no próximo mês de referência, 
    considerando o dia limite informado.
    Se o dia atual for menor ou igual ao dia_limite, o mês de referência será 
    o mês atual. Caso contrário, o mês de referência será o próximo mês. 
    A função retorna a fatura correspondente ao mês e ano de referência, 
    caso exista, ou None caso contrário.
    Parâmetros:
        faturas (list): Lista de dicionários contendo informações das faturas. 
                        Cada dicionário deve ter a chave 'date' no formato 'YYYY-MM-DD'.
        dia_limite (int): Dia do mês que define o limite para considerar o mês atual 
                          ou o próximo mês como referência.
    Retorna:
        dict ou None: Retorna o dicionário da fatura correspondente ao mês e ano 
                      de referência, ou None se nenhuma fatura for encontrada.
    """
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
    """
    Obtém as transações de uma fatura específica de um cartão de crédito.

    Args:
        headers (dict): Cabeçalhos HTTP necessários para autenticação na API.
        id_cartao (str): Identificador único do cartão de crédito.
        id_fatura (str): Identificador único da fatura do cartão de crédito.
        url_base (str): URL base da API Organizze.

    Returns:
        dict: Dados das transações da fatura em formato JSON, caso a requisição seja bem-sucedida.

    Raises:
        HTTPError: Exceção levantada caso a resposta da API retorne um código de status diferente de 200.
    """
    url_transacoes = f"{url_base}credit_cards/{id_cartao}/invoices/{id_fatura}"
    response = requests.get(url_transacoes, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def obter_transacoes_fatura_anterior(headers, id_cartao, id_fatura_atual, url_base, hoje):
    """
    Obtém as transações da fatura anterior de um cartão de crédito, considerando apenas as transações parceladas
    que possuem parcelas restantes.
    Args:
        headers (dict): Cabeçalhos HTTP para autenticação na API.
        id_cartao (str): Identificador do cartão de crédito.
        id_fatura_atual (str): Identificador da fatura atual.
        url_base (str): URL base da API.
        hoje (datetime.date): Data atual para determinar o período de análise.
    Returns:
        dict: Um dicionário contendo as transações da fatura anterior que possuem parcelas restantes.
              A chave é o ID da transação e o valor é o objeto da transação.
    Raises:
        HTTPError: Caso a requisição à API retorne um código de status diferente de 200.
    """
    transacoes_anteriores = {}
    
    if 10 <= hoje.day <= 19:
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
    Função principal para análise de transações e geração de relatórios financeiros.
    Esta função realiza as seguintes etapas:
    1. Obtém os tokens de autenticação e configura os cabeçalhos para chamadas à API Organizze.
    2. Define os IDs das contas de cartões de crédito e o intervalo de datas para análise.
    3. Obtém as faturas dos cartões de crédito no período especificado.
    4. Identifica as faturas atuais e obtém suas transações.
    5. Busca transações de faturas anteriores e ajusta o campo de parcelas (installment).
    6. Combina as transações atuais e anteriores, mantendo apenas os campos relevantes.
    7. Converte as transações em DataFrames e ajusta os dados para análise.
    8. Calcula a quantidade de transações parceladas e as que estão na última parcela.
    9. Gera um arquivo CSV com as transações ajustadas.
    10. Agrupa os dados por categoria, calcula os valores totais e compara com os limites definidos.
    11. Envia um e-mail com o resumo das informações financeiras.
    Saída:
    - Gera um arquivo CSV chamado 'transacoes_ajustado.csv' com as transações ajustadas.
    - Envia um e-mail com o resumo financeiro, incluindo valores totais, limites e porcentagens.
    Requisitos:
    - As funções auxiliares `obter_faturas`, `verificar_fatura`, `obter_transacoes_fatura`, 
        `obter_transacoes_fatura_anterior`, `ajustar_dataframe` e `enviar_email` devem estar implementadas.
    - As bibliotecas `os`, `datetime`, `pandas` e outras necessárias devem estar importadas.
    """
    token = os.getenv('TOKEN_ORGANIZZE')
    headers = {
        'Authorization': f'Basic {token}'
    }

    id_itau_azul = '1704776'
    id_sant_aa = '1704790'

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


    # por conta do problema do open finance que nao esta trazendo as compras parceladas da fatura anterior automaticamente
    # vamos buscar as transacoes da fatura anterior e somar 1 ao campo installment
    transacoes_anteriores_itau = obter_transacoes_fatura_anterior(headers, id_itau_azul, id_fatura_itau, url_base, hoje)
    transacoes_anteriores_santander = obter_transacoes_fatura_anterior(headers, id_sant_aa, id_fatura_santander, url_base, hoje)
    
    
    #soma 1 ao campo installment dessas transacoes que sao da fatura anterior
    transacoes_anteriores_itau = {k: {**v, 'installment': v['installment'] + 1} for k, v in transacoes_anteriores_itau.items()}
    transacoes_anteriores_santander = {k: {**v, 'installment': v['installment'] + 1} for k, v in transacoes_anteriores_santander.items()}

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

    #criar uma variavel que soma a quantidade de transacoes parceladas - essa conta e feita somando a quantidade de transacoes que tem as colunas installment e total_installments diferentes
    df['Parcelado'] = (df['installment'] != df['total_installments']).astype(int)
    qtde_parcelado = df['Parcelado'].sum()

    #determonar quantas transacoes ja estao na ultima parcela, ou seja, installment = total_installments;total_installments precisa ser maior que 1
    df['Ultima_parcela'] = ((df['installment'] == df['total_installments']) & (df['total_installments'] > 1)).astype(int)
    qtde_ultima_parcela = df['Ultima_parcela'].sum()
    
    df.to_csv('transacoes_ajustado.csv')
    df_grouped = df.groupby('Categoria')['Valor'].sum().reset_index()
    # Preencher valores zerados com 0
    df_grouped['Valor'] = df_grouped['Valor'].abs()
    limites = {
        'alimentacao_casa': 300,
        'anuidade': 236,
        'assinaturas': 140,
        'beleza': 200,
        'casa': 500,
        'compras': 800,
        'diversao-lazer-comida': 500,
        'educacao': 4250,
        'esporte': 50,
        'outros': 200,
        'saude': 300,
        'seguro_carro': 680,
        'transp(ub+gas+vel+ccr)': 1200,
        'viagem': 2000
    }
    df_grouped['Limite'] = df_grouped['Categoria'].map(limites).fillna(0)
    #df_grouped['Limite'] = df_grouped['Limite'].replace(0, np.nan)
    #coluna porcentagem
    df_grouped['Porcentagem'] = (df_grouped['Valor'] / df_grouped['Limite'] * 100).map('{:.2f}%'.format)
    total_limite = df_grouped['Limite'].sum()
    #imprimir o total no email
    enviar_email(df_grouped, round(df_grouped['Valor'].sum(), 2), total_limite, qtde_parcelado, qtde_ultima_parcela)

if __name__ == "__main__":
    main()
