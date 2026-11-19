from pathlib import Path

import pandas as pd

# Note-se que eu usei essa mesma library customizada, tanto aqui quanto no exercício de meio de módulo para realizar a limpeza de dados, porém aqui com pequenas adaptações

# Ler o arquivo CSV e retornar um DataFrame do Pandas
def carregar_dados() -> pd.DataFrame:
    return pd.read_csv(Path(__file__).resolve().parent.parent / 'data' / 'manutencao_preditiva.csv')

# Explorar o DataFrame, mostrando informações básicas sobre os dados
def explorar(df: pd.DataFrame) -> None:
    print('\n=== INSPECAO INICIAL DO DATASET ===')
    print(df.head())
    print('Formato:', df.shape)
    print('Colunas:', list(df.columns))
    df.info()
    print(df.describe())
    print('\nValores nulos por coluna:')
    print(df.isnull().sum().sort_values(ascending=False))

# Contar o número de espaços extras em cada coluna de texto. Não foi pedido para contar e remover espaços extras nesta tarefa, porém manti o código e fiz mesmo assim nas colunas de texto
def contar_espacos_extras(df: pd.DataFrame) -> pd.Series:
    return pd.Series({
        coluna: (df[coluna] != df[coluna].str.strip()).sum()
        for coluna in ['id_produto', 'tipo']
    })

# Remover espaços extras de cada coluna de texto. Não foi pedido para contar e remover espaços extras nesta tarefa, porém manti o código e fiz mesmo assim nas colunas de texto
def remover_espacos(df: pd.DataFrame) -> pd.DataFrame:
    print('\n[Espacos] Campos com espacos extras antes:')
    print(contar_espacos_extras(df))
    for coluna in ['id_produto', 'tipo']:
        df[coluna] = df[coluna].str.strip()
    print('[Espacos] Campos com espacos extras depois:')
    print(contar_espacos_extras(df))
    return df

# Imputar registros com valores nulos
def imputar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    print(f'\n[Nulos] Registros antes: {len(df)}')
    print('[Nulos] Ausentes antes:')
    print(df[COLUNAS_CRITICAS].isnull().sum())
    df_limpo = df.dropna(subset=COLUNAS_CRITICAS)
    print(f'[Nulos] Registros removidos: {len(df) - len(df_limpo)}')
    print('[Nulos] Ausentes depois:')
    print(df_limpo[COLUNAS_CRITICAS].isnull().sum())
    print(f'[Nulos] Registros depois: {len(df_limpo)}')
    return df_limpo

# Limpar os dados do DataFrame, aplicando todas as funções de limpeza e retornando o DataFrame limpo e um relatório das alterações feitas
def limpar_dados(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    print('\n=== LIMPEZA DOS DADOS ===')
    bruto = df.copy()

    df = remover_espacos(df.copy())
    removidos_data = bruto.index.difference(df.index)
    df = imputar_nulos(df).copy()
    removidos_nulos = bruto.index.difference(df.index).difference(removidos_data)

    removidos = pd.concat([
        bruto.loc[removidos_data].assign(motivo='data invalida'),
        bruto.loc[removidos_nulos].assign(motivo='valor ausente'),
    ])
    relatorio = {
        'iniciais': len(bruto),
        'finais': len(df),
        'clientes_sinalizados': int(df['cliente_fora_do_padrao'].sum()),
        'removidos': removidos,
    }
    return df, relatorio

