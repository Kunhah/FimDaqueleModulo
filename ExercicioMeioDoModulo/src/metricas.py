"""Métricas agregadas de vendas (todas feitas com `groupby` do pandas).

Cada função recebe o DataFrame com as colunas derivadas e devolve uma tabela.
`calcular_metricas` chama todas, imprime e devolve um dicionário com elas.
"""

import pandas as pd


def metricas_por_mes(df: pd.DataFrame) -> pd.DataFrame:
    """Receita, quantidade vendida e número de vendas de cada mês."""
    return df.groupby(['mes', 'mes_nome']).agg(
        receita_total=('receita_total', 'sum'),
        quantidade=('quantidade', 'sum'),
        n_vendas=('id_venda', 'count'),
    ).reset_index()


def top_produtos(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Os `n` produtos com maior receita."""
    return df.groupby('produto')['receita_total'].sum().nlargest(n).reset_index()


def receita_por_categoria(df: pd.DataFrame) -> pd.DataFrame:
    """Receita de cada categoria, da maior para a menor."""
    return (df.groupby('categoria')['receita_total'].sum()
            .sort_values(ascending=False).reset_index())


def metricas_por_regiao(df: pd.DataFrame) -> pd.DataFrame:
    """Receita total e ticket médio (receita média por venda) de cada região."""
    return df.groupby('regiao').agg(
        receita_total=('receita_total', 'sum'),
        ticket_medio=('receita_total', 'mean'),
    ).sort_values('receita_total', ascending=False).reset_index()


def calcular_metricas(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Calcula e imprime todas as métricas.

    Returns:
        Dicionário {nome_da_metrica: tabela}, com as chaves
        'por_mes', 'top_produtos', 'por_categoria' e 'por_regiao'.
    """
    metricas = {
        'por_mes': metricas_por_mes(df),
        'top_produtos': top_produtos(df),
        'por_categoria': receita_por_categoria(df),
        'por_regiao': metricas_por_regiao(df),
    }
    for nome, tabela in metricas.items():
        # 'top_produtos' vira o título 'TOP PRODUTOS'
        print(f'\n=== {nome.upper().replace("_", " ")} ===')
        print(tabela.round(2).to_string(index=False))
    return metricas
