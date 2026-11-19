import re
from datetime import datetime

import pandas as pd

from .config import (
    COLUNAS_CRITICAS,
    COLUNAS_TEXTO,
    CSV_VENDAS,
    FORMATO_DATA,
    PADRAO_CLIENTE,
    PADRAO_CLIENTE_RUIDOSO,
)


def carregar_dados() -> pd.DataFrame:
    return pd.read_csv(CSV_VENDAS)


def explorar(df: pd.DataFrame) -> None:
    print('\n=== INSPECAO INICIAL DO DATASET ===')
    print(df.head())
    print('Formato:', df.shape)
    print('Colunas:', list(df.columns))
    df.info()
    print(df.describe())
    print('\nValores nulos por coluna:')
    print(df.isnull().sum().sort_values(ascending=False))


def contar_espacos_extras(df: pd.DataFrame) -> pd.Series:
    return pd.Series({
        coluna: (df[coluna] != df[coluna].str.strip()).sum()
        for coluna in COLUNAS_TEXTO
    })


def remover_espacos(df: pd.DataFrame) -> pd.DataFrame:
    print('\n[Espacos] Campos com espacos extras antes:')
    print(contar_espacos_extras(df))
    for coluna in COLUNAS_TEXTO:
        df[coluna] = df[coluna].str.strip()
    print('[Espacos] Campos com espacos extras depois:')
    print(contar_espacos_extras(df))
    return df


def converter_data(texto: str) -> datetime | None:
    try:
        return datetime.strptime(texto, FORMATO_DATA)
    except ValueError:
        return None


def remover_datas_invalidas(df: pd.DataFrame) -> pd.DataFrame:
    print(f'\n[Datas] Registros antes: {len(df)}')
    df['data_venda'] = pd.to_datetime(df['data_venda'].apply(converter_data))
    data_invalida = df['data_venda'].isnull()
    print(f'[Datas] Datas invalidas removidas: {data_invalida.sum()} '
          f'(id_venda: {df.loc[data_invalida, "id_venda"].tolist()})')
    df = df[~data_invalida]
    print(f'[Datas] Registros depois: {len(df)}')
    return df


def remover_nulos(df: pd.DataFrame) -> pd.DataFrame:
    print(f'\n[Nulos] Registros antes: {len(df)}')
    print('[Nulos] Ausentes antes:')
    print(df[COLUNAS_CRITICAS].isnull().sum())
    df_limpo = df.dropna(subset=COLUNAS_CRITICAS)
    print(f'[Nulos] Registros removidos: {len(df) - len(df_limpo)}')
    print('[Nulos] Ausentes depois:')
    print(df_limpo[COLUNAS_CRITICAS].isnull().sum())
    print(f'[Nulos] Registros depois: {len(df_limpo)}')
    return df_limpo


def converter_tipos(df: pd.DataFrame) -> pd.DataFrame:
    colunas = ['data_venda'] + COLUNAS_CRITICAS
    print('\n[Tipos] Tipos antes:')
    print(df[colunas].dtypes)
    df['quantidade'] = df['quantidade'].astype(int)
    df['preco_unitario'] = df['preco_unitario'].astype(float)
    print('[Tipos] Tipos depois:')
    print(df[colunas].dtypes)
    return df


def padronizar_clientes(df: pd.DataFrame) -> pd.DataFrame:
    fora_do_padrao = ~df['cliente'].str.fullmatch(PADRAO_CLIENTE)
    print(f'\n[Clientes] Fora do padrao Cliente_NNN antes: {fora_do_padrao.sum()}')
    print(f'[Clientes] Exemplos antes: {df.loc[fora_do_padrao, "cliente"].head().tolist()}')

    original = df['cliente']
    sem_ruido = original.str.replace(r'[^A-Za-z0-9_]', '', regex=True)
    numero = sem_ruido.str.extract(PADRAO_CLIENTE_RUIDOSO, flags=re.IGNORECASE)[0]
    df['cliente'] = ('Cliente_' + numero.str.zfill(3)).fillna(sem_ruido)
    df['cliente_fora_do_padrao'] = fora_do_padrao

    corrigidos = pd.DataFrame({'antes': original, 'depois': df['cliente']})[fora_do_padrao]
    print('[Clientes] Exemplos corrigidos:')
    print(corrigidos.head())

    ainda_fora = ~df['cliente'].str.fullmatch(PADRAO_CLIENTE)
    print(f'[Clientes] Fora do padrao Cliente_NNN depois: {ainda_fora.sum()}')
    if ainda_fora.any():
        print(f'[Clientes] Nao foi possivel padronizar: {df.loc[ainda_fora, "cliente"].tolist()}')
    return df


def limpar_dados(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    print('\n=== LIMPEZA DOS DADOS ===')
    bruto = df.copy()

    df = remover_espacos(df.copy())
    df = remover_datas_invalidas(df)
    removidos_data = bruto.index.difference(df.index)
    df = remover_nulos(df).copy()
    removidos_nulos = bruto.index.difference(df.index).difference(removidos_data)
    df = converter_tipos(df)
    df = padronizar_clientes(df)

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
