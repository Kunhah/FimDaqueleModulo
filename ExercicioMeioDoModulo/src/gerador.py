import csv
import random
from datetime import datetime, timedelta

from .config import COLUNAS, CSV_VENDAS


def gerar_dataset_vendas(caminho_csv=CSV_VENDAS, n_registros: int = 200, seed: int = 42) -> None:
    random.seed(seed)
    produtos = ['Notebook', 'Smartphone', 'Tablet', 'Monitor',
                'Teclado', 'Mouse', 'Headset']
    categorias = {'Notebook': 'Computadores', 'Smartphone': 'Celulares',
                  'Tablet': 'Celulares', 'Monitor': 'Computadores',
                  'Teclado': 'Perifericos', 'Mouse': 'Perifericos',
                  'Headset': 'Perifericos'}
    precos = {'Notebook': 3500, 'Smartphone': 2200, 'Tablet': 1800,
              'Monitor': 1200, 'Teclado': 250, 'Mouse': 120,
              'Headset': 350}
    regioes = ['Sudeste', 'Sul', 'Nordeste', 'Centro-Oeste', 'Norte']
    data_inicio = datetime(2025, 1, 1)

    with open(caminho_csv, 'w', newline='', encoding='utf-8') as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()

        for i in range(n_registros):
            produto = random.choice(produtos)
            categoria = categorias[produto]
            quantidade = random.randint(1, 10)
            preco = round(precos[produto] * random.uniform(0.85, 1.15), 2)
            data = data_inicio + timedelta(days=random.randint(0, 364))
            data_txt = data.strftime('%Y-%m-%d')
            cliente = f'Cliente_{random.randint(1, 50):03d}'

            if random.random() < 0.05:
                quantidade = ''
            if random.random() < 0.04:
                preco = ''
            if random.random() < 0.06:
                produto = ' ' + produto + ' '
            if random.random() < 0.03:
                data_txt = 'DATA INVALIDA'
            if random.random() < 0.10:
                cliente = random.choice([
                    cliente.upper().replace('_', '-'),
                    cliente + '!!',
                    ' ' + cliente,
                    cliente.replace('Cliente_', 'cliente#'),
                ])

            escritor.writerow({
                'id_venda': i + 1,
                'data_venda': data_txt,
                'cliente': cliente,
                'produto': produto,
                'categoria': categoria,
                'regiao': random.choice(regioes),
                'quantidade': quantidade,
                'preco_unitario': preco,
            })

    print(f'Dataset gerado com {n_registros} registros em {caminho_csv}.')
