"""Configurações centrais do projeto.

Tudo que é "constante" (caminhos, nomes de colunas, formatos e padrões)
fica aqui, para que os outros módulos não tenham valores soltos no código.
Se algo precisar mudar (por exemplo, o nome do CSV), basta mudar neste arquivo.
"""

from pathlib import Path

# Pasta raiz do projeto (a pasta que contém salesinsight.py).
# __file__ é src/config.py, então subimos dois níveis.
DIR_BASE = Path(__file__).resolve().parent.parent

# Arquivo de dados lido pelo programa (gerado automaticamente se não existir).
CSV_VENDAS = DIR_BASE / 'vendas.csv'

# Ordem das colunas do CSV.
COLUNAS = ['id_venda', 'data_venda', 'cliente', 'produto',
           'categoria', 'regiao', 'quantidade', 'preco_unitario']

# Colunas de texto que podem vir com espaços sobrando no início/fim.
COLUNAS_TEXTO = ['cliente', 'produto', 'categoria', 'regiao']

# Colunas sem as quais não dá para calcular a receita.
# Linhas com valor ausente nelas são descartadas.
COLUNAS_CRITICAS = ['quantidade', 'preco_unitario']

# Formato esperado da data no CSV: ano-mês-dia (ex.: 2025-03-23).
FORMATO_DATA = '%Y-%m-%d'

# Formato correto do nome do cliente: "Cliente_" seguido de exatamente 3 dígitos.
PADRAO_CLIENTE = r'^Cliente_\d{3}$'

# Nomes dos meses em português (sem acento, para evitar problemas no terminal).
MESES_PT = {
    1: 'Janeiro', 2: 'Fevereiro', 3: 'Marco', 4: 'Abril',
    5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
    9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro',
}

# Limites (em R$ de gasto total) para classificar os clientes.
LIMITE_OURO = 15000   # acima disso: Ouro
LIMITE_PRATA = 5000   # a partir disso: Prata; abaixo: Bronze
