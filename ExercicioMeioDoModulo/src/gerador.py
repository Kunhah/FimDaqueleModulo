"""Geração de um dataset sintético de vendas.

Cria um CSV com vendas fictícias de produtos de informática ao longo de 2025.
De propósito, uma parte dos registros vem com "sujeira" (valores ausentes,
espaços extras, datas inválidas e nomes de cliente fora do padrão), para que
a etapa de limpeza em data.py tenha o que corrigir.
"""

import csv
import random
from datetime import datetime, timedelta

from .config import COLUNAS, CSV_VENDAS

# Catálogo: produto -> (categoria, preço base em R$).
# Obs.: a ordem importa para a reprodutibilidade (random.choice usa essa ordem).
CATALOGO = {
    'Notebook': ('Computadores', 3500),
    'Smartphone': ('Celulares', 2200),
    'Tablet': ('Celulares', 1800),
    'Monitor': ('Computadores', 1200),
    'Teclado': ('Perifericos', 250),
    'Mouse': ('Perifericos', 120),
    'Headset': ('Perifericos', 350),
}

REGIOES = ['Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste', 'Norte']


def sujar_cliente(cliente: str) -> str:
    """Devolve o nome do cliente com algum "erro de digitação" aleatório."""
    return random.choice([
        cliente.upper().replace('_', '-'),         # CLIENTE-016
        cliente + '!!',                            # Cliente_016!!
        ' ' + cliente,                             # " Cliente_016"
        cliente.replace('Cliente_', 'cliente#'),   # cliente#016
    ])


def gerar_dataset_vendas(caminho_csv=CSV_VENDAS, n_registros: int = 200, seed: int = 42) -> None:
    """Gera o CSV de vendas e salva em `caminho_csv`.

    Args:
        caminho_csv: onde salvar o arquivo.
        n_registros: quantidade de vendas a gerar.
        seed: semente do gerador aleatório. Com a mesma semente,
            o arquivo gerado é sempre o mesmo (resultado reproduzível).
    """
    random.seed(seed)
    produtos = list(CATALOGO)
    data_inicio = datetime(2025, 1, 1)

    with open(caminho_csv, 'w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()

        for i in range(n_registros):
            # --- Venda "limpa" ---
            produto = random.choice(produtos)
            categoria, preco_base = CATALOGO[produto]
            quantidade = random.randint(1, 10)
            preco = round(preco_base * random.uniform(0.85, 1.15), 2)  # varia ±15%
            data_txt = (data_inicio + timedelta(days=random.randint(0, 364))).strftime('%Y-%m-%d')
            cliente = f'Cliente_{random.randint(1, 50):03d}'

            # --- Sujeira proposital (cada uma com sua probabilidade) ---
            if random.random() < 0.05:
                quantidade = ''                      # quantidade ausente
            if random.random() < 0.04:
                preco = ''                           # preço ausente
            if random.random() < 0.06:
                produto = ' ' + produto + ' '        # espaços extras
            if random.random() < 0.03:
                data_txt = 'DATA INVALIDA'           # data que não pode ser lida
            if random.random() < 0.10:
                cliente = sujar_cliente(cliente)     # nome fora do padrão

            escritor.writerow({
                'id_venda': i + 1,
                'data_venda': data_txt,
                'cliente': cliente,
                'produto': produto,
                'categoria': categoria,
                'regiao': random.choice(REGIOES),
                'quantidade': quantidade,
                'preco_unitario': preco,
            })

    print(f'Dataset gerado com {n_registros} registros em {caminho_csv}.')
