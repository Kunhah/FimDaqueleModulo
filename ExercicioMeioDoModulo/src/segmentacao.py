import pandas as pd


def segmentar_clientes(df: pd.DataFrame) -> pd.DataFrame:
    classificar = lambda total: (
        'Ouro' if total > 15000 else 'Prata' if total >= 5000 else 'Bronze'
    )
    clientes = (df.groupby('cliente')['receita_total'].sum()
                .rename('total_gasto').sort_values(ascending=False).reset_index())
    clientes['segmento'] = clientes['total_gasto'].map(classificar)

    print('\n=== TOP 10 CLIENTES ===')
    print(clientes.head(10).round(2).to_string(index=False))
    print('\n=== CLIENTES POR SEGMENTO ===')
    print(clientes['segmento'].value_counts().to_string())
    return clientes
