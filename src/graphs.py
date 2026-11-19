import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Estilo visual padrão para todos os gráficos
sns.set_theme(style='whitegrid')


def plotar_correlacao(df, colunas, dir_saida=None, mostrar=True, sufixo=''):

def plotar_boxplots(df, colunas):
    """Plota o boxplot para cada coluna informada do DataFrame."""
    for coluna in colunas:
        plt.figure(figsize=(8, 3))
        sns.boxplot(x=df[coluna])
        plt.title(f'Boxplot - {coluna}')
        plt.tight_layout()
        plt.show()

