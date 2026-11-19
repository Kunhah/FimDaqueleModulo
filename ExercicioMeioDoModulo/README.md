# SalesInsight PY

Projeto em Python para analisar vendas. Ele lê um CSV, limpa os dados inválidos, cria colunas derivadas, calcula métricas por mês, produto, categoria e região e classifica clientes em Bronze, Prata ou Ouro.

## Executar

```bash
pip install -r requirements.txt
python salesinsight.py
```

Se `vendas.csv` não existir, o programa gera um dataset sintético com 200 registros.

## Estrutura

```
ExercicioMeioDoModulo/
├── salesinsight.py        # ponto de entrada
├── vendas.csv
├── requirements.txt
└── src/
    ├── config.py          # caminhos e constantes
    ├── gerador.py         # geração do dataset
    ├── data.py            # carga, inspeção e limpeza
    ├── relatorio.py       # relatório de limpeza
    ├── transformacoes.py  # colunas derivadas
    ├── metricas.py        # métricas agregadas
    └── segmentacao.py     # segmentação de clientes
```

## Conceitos usados

- pandas (leitura, limpeza, groupby)
- `datetime` e expressões regulares (`re`)
- funções, `if/elif/else` e `lambda`
