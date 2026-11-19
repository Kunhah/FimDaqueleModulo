from src.config import CSV_VENDAS
from src.data import carregar_dados, explorar, limpar_dados
from src.gerador import gerar_dataset_vendas
from src.metricas import calcular_metricas
from src.relatorio import mostrar_relatorio_limpeza
from src.segmentacao import segmentar_clientes
from src.transformacoes import criar_colunas_derivadas


def main() -> None:
    print('=' * 60)
    print(' SALESINSIGHT PY - Analise de Dados de Vendas')
    print('=' * 60)

    if not CSV_VENDAS.exists():
        gerar_dataset_vendas()

    df = carregar_dados()
    explorar(df)
    df, relatorio = limpar_dados(df)
    mostrar_relatorio_limpeza(relatorio)
    df = criar_colunas_derivadas(df)
    metricas = calcular_metricas(df)
    clientes = segmentar_clientes(df)


if __name__ == '__main__':
    main()
