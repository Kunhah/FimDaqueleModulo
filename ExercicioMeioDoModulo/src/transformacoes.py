"""Criação de colunas derivadas (calculadas a partir das colunas originais).

Colunas criadas:
    receita_total       quantidade * preco_unitario
    mes, mes_nome, ano  extraídos de data_venda
    trimestre           Q1 (jan-mar), Q2 (abr-jun), Q3 (jul-set) ou Q4 (out-dez)
    faixa_receita_item  Baixo (< R$ 500), Medio (< R$ 5.000) ou Alto Valor
"""

import pandas as pd

from .config import MESES_PT


def classificar_trimestre(mes: int) -> str:
    """Recebe o número do mês (1 a 12) e devolve o trimestre ('Q1' a 'Q4')."""
    if mes <= 3:
        return 'Q1'
    elif mes <= 6:
        return 'Q2'
    elif mes <= 9:
        return 'Q3'
    else:
        return 'Q4'


def classificar_faixa_receita(receita: float) -> str:
    """Classifica uma venda pelo valor da sua receita."""
    if receita < 500:
        return 'Baixo Valor'
    elif receita < 5000:
        return 'Medio Valor'
    else:
        return 'Alto Valor'


def criar_colunas_derivadas(df: pd.DataFrame) -> pd.DataFrame:
    """Devolve uma cópia de `df` com as colunas derivadas adicionadas.

    Espera receber o DataFrame já limpo (data_venda como data e
    quantidade/preco_unitario como números).
    """
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
