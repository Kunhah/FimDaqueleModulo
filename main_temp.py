from pathlib import Path

import pandas as pd

from src.graphs import (
    plotar_boxplots,
    plotar_grafico_barras,
    plotar_heatmap,
    plotar_histogramas,
)


def main() -> None:
    df = pd.read_csv(Path(__file__).resolve().parent / 'data' / 'manutencao_preditiva.csv')

    plotar_grafico_barras(df)
    plotar_histogramas(df)
    plotar_heatmap(df)
    plotar_boxplots(df)


if __name__ == '__main__':
    main()
