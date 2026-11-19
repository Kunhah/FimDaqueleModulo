from pathlib import Path

DIR_BASE = Path(__file__).resolve().parent.parent
DIR_SAIDAS = DIR_BASE / 'outputs'

CSV_VENDAS = DIR_BASE / 'vendas.csv'

COLUNAS = ['id_venda', 'data_venda', 'cliente', 'produto',
           'categoria', 'regiao', 'quantidade', 'preco_unitario']
COLUNAS_TEXTO = ['cliente', 'produto', 'categoria', 'regiao']
COLUNAS_CRITICAS = ['quantidade', 'preco_unitario']

FORMATO_DATA = '%Y-%m-%d'

PADRAO_CLIENTE = r'^Cliente_\d{3}$'
PADRAO_CLIENTE_RUIDOSO = r'^cliente_?(\d+)$'

MESES_PT = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Marco', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro',
}
