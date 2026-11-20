from pathlib import Path

import pandas as pd

COLUNAS_NULOS = ['temperatura_ar_k', 'temperatura_processo_k',
                 'torque_nm', 'velocidade_rotacao_rpm']

def carregar_dados() -> pd.DataFrame:
    """Lê o arquivo CSV de manutenção preditiva e retorna um DataFrame do Pandas."""
    return pd.read_csv(Path(__file__).resolve().parent.parent / 'data' / 'manutencao_preditiva.csv')

def explorar(df: pd.DataFrame) -> None:
    """Explora o DataFrame, exibindo informações básicas, colunas, resumo estatístico e nulos."""
    print('\n INSPECAO INICIAL DO DATASET')
    print(df.head())
    print('\nFormato:', df.shape)
    print('\nColunas:', list(df.columns))
    df.info()
    print('\nDescrição:\n')
    print(df.describe())
    print('\nValores nulos por coluna:')
    print(df.isnull().sum().sort_values(ascending=False))

def contar_espacos_extras(df: pd.DataFrame) -> pd.Series:
    """Conta o número de espaços extras em cada coluna de texto especificada."""
    return pd.Series({
        coluna: (df[coluna] != df[coluna].str.strip()).sum()
        for coluna in ['id_produto', 'tipo']
    })

def remover_espacos(df: pd.DataFrame) -> pd.DataFrame:
    """Remove espaços extras das colunas de texto de identificação e tipo."""
    print('\n[Espacos] Campos com espacos extras antes:')
    print(contar_espacos_extras(df))
    for coluna in ['id_produto', 'tipo']:
        df[coluna] = df[coluna].str.strip()
    print('[Espacos] Campos com espacos extras depois:')
    print(contar_espacos_extras(df))
    return df

def remover_duplicados(df: pd.DataFrame) -> pd.DataFrame:
    """Remove linhas duplicadas, ou seja, cópias exatas de outra linha do DataFrame."""
    print(f'\n[Duplicados] Registros antes: {len(df)}')
    print(f'[Duplicados] Linhas duplicadas encontradas: {df.duplicated().sum()}')
    df_limpo = df.drop_duplicates()
    print(f'[Duplicados] Registros depois: {len(df_limpo)}')
    return df_limpo

def imputar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """Preenche os nulos de cada coluna com a média dessa coluna."""
    df = df.copy()

    print(f'\n[Nulos] Registros antes: {len(df)}')
    print('[Nulos] Ausentes antes:')
    print(df[COLUNAS_NULOS].isnull().sum())
    print('\n')

    # Calcula a média de cada coluna (os NaN são ignorados no cálculo)
    medias = df[COLUNAS_NULOS].mean()
    # Troca só os NaN de cada coluna pela média da própria coluna
    df[COLUNAS_NULOS] = df[COLUNAS_NULOS].fillna(medias)
    print('[Nulos] Média usada no preenchimento:')
    print(medias.round(2))
    print('\n')

    print('[Nulos] Ausentes depois:')
    print(df[COLUNAS_NULOS].isnull().sum())
    print(f'[Nulos] Registros depois: {len(df)}')
    return df

def limpar_dados(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Aplica todas as etapas de limpeza no DataFrame e retorna os dados limpos junto a um relatório."""
    print('\n LIMPEZA DOS DADOS')
    relatorio = {'iniciais': len(df)}

    df = remover_espacos(df.copy())
    df = remover_duplicados(df)
    relatorio['duplicados_removidos'] = relatorio['iniciais'] - len(df)

    relatorio['nulos_preenchidos'] = df[COLUNAS_NULOS].isnull().sum().to_dict()
    df = imputar_nulos(df)
    relatorio['finais'] = len(df)

    return df, relatorio
