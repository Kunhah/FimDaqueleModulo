from pathlib import Path

import pandas as pd

def carregar_dados() -> pd.DataFrame:
    """Lê o arquivo CSV de manutenção preditiva e retorna um DataFrame do Pandas."""
    return pd.read_csv(Path(__file__).resolve().parent.parent / 'data' / 'manutencao_preditiva.csv')

def explorar(df: pd.DataFrame) -> None:
    """Explora o DataFrame, exibindo informações básicas, colunas, resumo estatístico e nulos."""
    print('\n=== INSPECAO INICIAL DO DATASET ===')
    print(df.head())
    print('Formato:', df.shape)
    print('Colunas:', list(df.columns))
    df.info()
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

def imputar_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """Remove registros com valores nulos nas colunas críticas definidas."""
    print(f'\n[Nulos] Registros antes: {len(df)}')
    print('[Nulos] Ausentes antes:')
    print(df[COLUNAS_CRITICAS].isnull().sum())
    df_limpo = df.dropna(subset=COLUNAS_CRITICAS)
    print(f'[Nulos] Registros removidos: {len(df) - len(df_limpo)}')
    print('[Nulos] Ausentes depois:')
    print(df_limpo[COLUNAS_CRITICAS].isnull().sum())
    print(f'[Nulos] Registros depois: {len(df_limpo)}')
    return df_limpo

def limpar_dados(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Aplica todas as etapas de limpeza no DataFrame e retorna os dados limpos junto a um relatório."""
    print('\n=== LIMPEZA DOS DADOS ===')
    
    bruto = df.copy()

    df_sem_espacos = remover_espacos(bruto.copy())
    removidos_data = bruto.index.difference(df_sem_espacos.index)
    
    df_final = imputar_nulos(df_sem_espacos)
    removidos_nulos = df_sem_espacos.index.difference(df_final.index)

    removidos = pd.concat([
        bruto.loc[removidos_data].assign(motivo='data invalida'),
        bruto.loc[removidos_nulos].assign(motivo='valor ausente'),
    ])
    
    relatorio = {
        'iniciais': len(bruto),
        'finais': len(df_final),
        'clientes_sinalizados': int(df_final['cliente_fora_do_padrao'].sum()),
        'removidos': removidos,
    }
    
    return df_final, relatorio