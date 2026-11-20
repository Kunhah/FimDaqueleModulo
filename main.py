import pandas as pd

from src.data import carregar_dados, explorar, limpar_dados
from src.graphs import (
    plotar_boxplots,
    plotar_grafico_barras,
    plotar_heatmap,
    plotar_histogramas,
)
from src.training import (
    dividir_e_balancear,
    escalar_para_knn,
    potencia,
    treinar_arvore,
    treinar_knn,
    veredito,
)


def main() -> None:
    # Fase 1: análise exploratória (gráficos salvos em outputs/)
    df = carregar_dados()
    explorar(df)
    plotar_grafico_barras(df)
    plotar_histogramas(df)
    plotar_heatmap(df)

    # Fase 2: limpeza e boxplots dos dados já tratados
    df, _ = limpar_dados(df)
    plotar_boxplots(df)

    # Fase 3: feature engineering (após tratar os nulos)
    df = potencia(df)

    # Fases 4 e 5: divisão estratificada e escalonamento para o KNN
    X_treino, X_teste, y_treino, y_teste = dividir_e_balancear(df)
    X_treino_esc, X_teste_esc = escalar_para_knn(X_treino, X_teste)

    # Fase 6: ajuste de hiperparâmetros
    tabela_knn = treinar_knn(X_treino_esc, X_teste_esc, y_treino, y_teste)
    tabela_arvore = treinar_arvore(X_treino, X_teste, y_treino, y_teste)

    # Fase 7: veredito final
    veredito(tabela_knn, tabela_arvore)


if __name__ == '__main__':
    main()
