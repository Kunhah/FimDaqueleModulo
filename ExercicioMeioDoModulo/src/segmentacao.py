"""Segmentação de clientes pelo total gasto.

Regras (limites definidos em config.py):
    Ouro    total gasto acima de R$ 15.000
    Prata   total gasto entre R$ 5.000 e R$ 15.000
    Bronze  total gasto abaixo de R$ 5.000
"""

import pandas as pd

from .config import LIMITE_OURO, LIMITE_PRATA


def segmentar_clientes(df: pd.DataFrame) -> pd.DataFrame:
    """Soma o gasto de cada cliente e o classifica em Ouro, Prata ou Bronze.

    Returns:
        DataFrame com as colunas `cliente`, `total_gasto` e `segmento`,
        ordenado do cliente que mais gastou para o que menos gastou.
    """
    # Função anônima (lambda) com if/else encadeado: recebe o total e devolve o segmento.
    classificar = lambda total: (
        'Ouro' if total > LIMITE_OURO else 'Prata' if total >= LIMITE_PRATA else 'Bronze'
    )

    clientes = (df.groupby('cliente')['receita_total'].sum()
                .rename('total_gasto').sort_values(ascending=False).reset_index())
    clientes['segmento'] = clientes['total_gasto'].map(classificar)

    print('\n=== TOP 10 CLIENTES ===')
    print(clientes.head(10).round(2).to_string(index=False))
    print('\n=== CLIENTES POR SEGMENTO ===')
    print(clientes['segmento'].value_counts().to_string())
    return clientes
