import pandas as pd

from .config import MESES_PT


def classificar_trimestre(mes: int) -> str:
    if mes <= 3:
        return 'Q1'
    elif mes <= 6:
        return 'Q2'
    elif mes <= 9:
        return 'Q3'
    else:
        return 'Q4'


def classificar_faixa_receita(receita: float) -> str:
    if receita < 500:
        return 'Baixo Valor'
    elif receita < 5000:
        return 'Medio Valor'
    else:
        return 'Alto Valor'


def criar_colunas_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['receita_total'] = (df['quantidade'] * df['preco_unitario']).round(2)
    df['mes'] = df['data_venda'].dt.month
    df['mes_nome'] = df['mes'].map(MESES_PT)
    df['trimestre'] = df['mes'].apply(classificar_trimestre)
    df['ano'] = df['data_venda'].dt.year
    df['faixa_receita_item'] = df['receita_total'].apply(classificar_faixa_receita)

    print('\n=== COLUNAS DERIVADAS ===')
    colunas = ['receita_total', 'mes', 'mes_nome', 'trimestre', 'ano', 'faixa_receita_item']
    print(df[colunas].head().to_string(index=False))
    return df
