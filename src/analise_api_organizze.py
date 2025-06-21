import pandas as pd
import datetime
import requests
import smtplib
import os
import re

def obter_nome_categoria(id_categoria):
    """
    Obtém o nome da categoria com base no ID da categoria.
    Argumentos:
        id_categoria (int): O ID da categoria.
    Retorna:
        str: O nome da categoria correspondente ao ID.
    """

    token = os.getenv('TOKEN_ORGANIZZE')
    headers = {
        'Authorization': f'Basic {token}'
    }
    url_categorias = "https://api.organizze.com.br/rest/v2/categories"
    response = requests.get(url_categorias, headers=headers)
    if response.status_code == 200:
        categorias = response.json()
        
    for categoria in categorias:
        if categoria['id'] == id_categoria:
            return categoria['name']

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
    df['Categoria'] = df['category_id'].apply(obter_nome_categoria)
    df = df.drop(columns=['category_id'])

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
    # Configurações do e-mail
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

def obter_ids_cartoes(headers, url_base):
    """
    Obtém os IDs das contas de cartões de crédito a partir da API Organizze.
    Args:
        headers (dict): Cabeçalhos HTTP necessários para autenticação na API.
    Returns:
        dict: Um dicionário contendo os IDs das contas de cartões de crédito.
    Raises:
        HTTPError: Exceção levantada caso a resposta da API retorne um código de status diferente de 200.
    """
    url_cartoes = f"{url_base}credit_cards"
    response = requests.get(url_cartoes, headers=headers)
    if response.status_code == 200:
        return {cartao['name']: cartao['id'] for cartao in response.json()}
    else:
        response.raise_for_status()

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

    url_base = "https://api.organizze.com.br/rest/v2/"

    ids_cartoes = obter_ids_cartoes(headers, url_base)
    
    #print(ids_cartoes)
    # Definindo os IDs dos cartoes de credito com base no que veio da API. Estes nomes devem ser os mesmos que foram
    # cadastrados no Organizze
    id_itau_azul = ids_cartoes['Cartao_Itau_Azul']
    id_sant_aa = ids_cartoes['Cartao_Santander_AA']

    
    hoje = datetime.datetime.now()
    start_date = (hoje - datetime.timedelta(days=365)).strftime('%Y-%m-%d')
    end_date = (hoje + datetime.timedelta(days=60)).strftime('%Y-%m-%d')    

    faturas_itau = obter_faturas(headers, id_itau_azul, url_base, start_date, end_date)
    faturas_santander = obter_faturas(headers, id_sant_aa, url_base, start_date, end_date)
    

    fatura_atual_itau = verificar_fatura(faturas_itau, 10)
    fatura_atual_santander = verificar_fatura(faturas_santander, 10)

    id_faturaatual_itau = fatura_atual_itau['id']
    id_faturaatual_santander = fatura_atual_santander['id']
    
    transacoes_itau = obter_transacoes_fatura(headers, id_itau_azul, id_faturaatual_itau, url_base)
    transacoes_santander = obter_transacoes_fatura(headers, id_sant_aa, id_faturaatual_santander, url_base)


    # por conta do problema do open finance que nao esta trazendo as compras parceladas da fatura anterior automaticamente
    # vamos buscar as transacoes da fatura anterior e somar 1 ao campo installment
    # somente as compras parceladas que sao trazidas para estas bases
    transacoes_anteriores_itau = obter_transacoes_fatura_anterior(headers, id_itau_azul, id_faturaatual_itau, url_base, hoje)
    transacoes_anteriores_santander = obter_transacoes_fatura_anterior(headers, id_sant_aa, id_faturaatual_santander, url_base, hoje)
    
    
    #soma 1 ao campo installment dessas transacoes que sao da fatura anterior
    transacoes_anteriores_itau = {k: {**v, 'installment': v['installment'] + 1} for k, v in transacoes_anteriores_itau.items()}
    transacoes_anteriores_santander = {k: {**v, 'installment': v['installment'] + 1} for k, v in transacoes_anteriores_santander.items()}

    #comparar as transacoes da fatura atual com as transacoes da fatura anterior para evitar duplicidade
    #a comparacao vai ser feita pelo campo amount_cents e date
    #caso a transacao da fatura anterior tenha o mesmo amount_cents e date da transacao da fatura atual, ela sera apagada do dicionario transacoes_anteriores
    transacoes_anteriores_itau = {k: v for k, v in transacoes_anteriores_itau.items() if not any(
        v['amount_cents'] == transacao['amount_cents'] and v['date'] == transacao['date']
        for transacao in transacoes_itau['transactions']
    )}
    
    transacoes_anteriores_santander = {k: v for k, v in transacoes_anteriores_santander.items() if not any(
        v['amount_cents'] == transacao['amount_cents'] and v['date'] == transacao['date']
        for transacao in transacoes_santander['transactions']
    )}
    
    # Adiciona as transações da fatura anterior ao dicionário de transações atuais
    transacoes_itau['transactions'] += list(transacoes_anteriores_itau.values())
    transacoes_santander['transactions'] += list(transacoes_anteriores_santander.values())

    transacoes_itau = transacoes_itau['transactions']
    transacoes_santander = transacoes_santander['transactions']
        
    #concatenar as duas listas de transacoes
    transacoes = transacoes_itau + transacoes_santander  

    #deleta as chaves que nao sao necessarias
    for transacao in transacoes:
        keys_to_keep = ['description', 'date', 'amount_cents', 'total_installments', 'installment', 'category_id']
        for key in list(transacao.keys()):
            if key not in keys_to_keep:
                del transacao[key]
                    
    #criar um dataframe com as transacoes
    df = pd.DataFrame(transacoes)
    
    #ajustar formatacao do dataframe
    df = ajustar_dataframe(df)

    #criar uma variavel que soma a quantidade de transacoes parceladas - essa conta e feita somando a quantidade de transacoes que tem as colunas installment e total_installments diferentes
    df['Parcelado'] = (df['installment'] != df['total_installments']).astype(int)
    qtde_parcelado = df['Parcelado'].sum()

    #determonar quantas transacoes ja estao na ultima parcela, ou seja, installment = total_installments;total_installments precisa ser maior que 1
    df['Ultima_parcela'] = ((df['installment'] == df['total_installments']) & (df['total_installments'] > 1)).astype(int)
    qtde_ultima_parcela = df['Ultima_parcela'].sum()
    
    #cria um csv com as transacoes
    df.to_csv('transacoes_ajustado.csv')
    
    # Agrupar por categoria e somar os valores
    df_grouped = df.groupby('Categoria')['Valor'].sum().reset_index()
    
    # Preencher valores zerados com 0
    df_grouped['Valor'] = df_grouped['Valor'].abs()
    
    #determina limites de gastos por categoria
    limites = {
        'alimentacao_casa': 800,
        'anuidade': 236,
        'assinaturas': 450,
        'beleza': 200,
        'casa': 500,
        'compras': 800,
        'diversao-lazer-comida': 500,
        'educacao': 4250,
        'esporte': 50,
        'outros': 200,
        'saude': 300,
        'seguro_carro': 403,
        'transp(ub+gas+vel+ccr)': 1400,
        'viagem': 700
    }
    df_grouped['Limite'] = df_grouped['Categoria'].map(limites).fillna(0)
    
    #cria coluna porcentagem
    df_grouped['Porcentagem'] = (df_grouped['Valor'] / df_grouped['Limite'] * 100).map('{:.2f}%'.format)
    
    #soma o total de gastos
    total_limite = df_grouped['Limite'].sum()
    
    #chama a funcao de enviar email com uma tabela com os gastos separados por categoria, com porcentagel, limite e total gasto
    enviar_email(df_grouped, round(df_grouped['Valor'].sum(), 2), total_limite, qtde_parcelado, qtde_ultima_parcela)

if __name__ == "__main__":
    main()
