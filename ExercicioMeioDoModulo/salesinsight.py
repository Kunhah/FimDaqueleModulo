"""SalesInsight PY - ponto de entrada do programa.

Executa o pipeline completo de análise de vendas:

    gerar CSV (se não existir) -> carregar -> inspecionar -> limpar
    -> criar colunas derivadas -> calcular métricas -> segmentar clientes

Uso:
    python salesinsight.py
"""

from src.config import CSV_VENDAS
from src.data import carregar_dados, explorar, limpar_dados, mostrar_relatorio_limpeza
from src.gerador import gerar_dataset_vendas
from src.metricas import calcular_metricas
from src.segmentacao import segmentar_clientes
from src.transformacoes import criar_colunas_derivadas


def main() -> None:
    print('=' * 60)
    print(' SALESINSIGHT PY - Analise de Dados de Vendas')
    print('=' * 60)

    # 1. Garante que existe um arquivo de dados para analisar.
    if not CSV_VENDAS.exists():
        gerar_dataset_vendas()

    # 2. Carrega e mostra uma visão geral dos dados brutos.
    df = carregar_dados()
    explorar(df)

    # 3. Limpa os dados e mostra o que foi removido/corrigido.
    df, relatorio = limpar_dados(df)
    mostrar_relatorio_limpeza(relatorio)

    # 4. Cria colunas calculadas (receita, mês, trimestre...).
    df = criar_colunas_derivadas(df)

    # 5. Análises: métricas agregadas e segmentação de clientes.
    calcular_metricas(df)
    segmentar_clientes(df)


if __name__ == '__main__':
    main()
