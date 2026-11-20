# SalesInsight PY

Projeto em Python para analisar um arquivo de vendas de produtos de informática.

O programa lê um CSV, limpa os dados com problemas, cria colunas calculadas,
gera métricas por mês, produto, categoria e região e, por fim, classifica os
clientes em **Bronze**, **Prata** ou **Ouro** de acordo com quanto gastaram.

Todos os resultados são mostrados no terminal.

---

## Como executar

Requisitos: Python 3.10 ou mais recente.

```bash
pip install -r requirements.txt
python salesinsight.py
```

Se o arquivo `vendas.csv` não existir, o programa gera um automaticamente, com
200 vendas fictícias de 2025. A geração usa uma semente fixa (`seed=42`), então
o arquivo gerado é sempre o mesmo. Para gerar de novo, basta apagar o
`vendas.csv` e rodar o programa.

---

## Como o programa funciona

O `salesinsight.py` chama as etapas abaixo, nesta ordem:

```
 vendas.csv
     │
     ▼
 1. Geração (só se o CSV não existir) ......... src/gerador.py
 2. Carga e inspeção inicial .................. src/data.py
 3. Limpeza + relatório de limpeza ............ src/data.py
 4. Colunas derivadas ......................... src/transformacoes.py
 5. Métricas agregadas ........................ src/metricas.py
 6. Segmentação de clientes ................... src/segmentacao.py
```

### 1. Geração do dataset (`gerador.py`)

Cria vendas com produto, categoria, região, quantidade, preço e cliente
aleatórios. Para que a limpeza tenha o que fazer, uma parte dos registros é
"sujada" de propósito:

| Problema inserido               | Chance | Exemplo                       |
|---------------------------------|--------|-------------------------------|
| Quantidade vazia                | 5%     | `quantidade = ''`             |
| Preço vazio                     | 4%     | `preco_unitario = ''`         |
| Espaços extras no produto       | 6%     | `' Notebook '`                |
| Data inválida                   | 3%     | `'DATA INVALIDA'`             |
| Nome de cliente fora do padrão  | 10%    | `CLIENTE-016`, `cliente#016`, `Cliente_016!!` |

### 2. Carga e inspeção (`data.py`)

`carregar_dados()` lê o CSV com `pd.read_csv`. `explorar()` mostra as
primeiras linhas, o formato da tabela, os tipos de cada coluna, estatísticas
descritivas e a contagem de valores nulos.

### 3. Limpeza (`data.py`)

`limpar_dados()` executa cinco etapas, cada uma mostrando um "antes e depois":

1. **Espaços extras**: aplica `strip()` em `cliente`, `produto`, `categoria` e `regiao`.
2. **Datas inválidas**: converte `data_venda` com `datetime.strptime`. Linhas
   cuja data não pode ser lida são **removidas**.
3. **Valores ausentes**: linhas sem `quantidade` ou sem `preco_unitario` são
   **removidas**, porque sem esses valores não é possível calcular a receita.
4. **Tipos**: `quantidade` vira `int` e `preco_unitario` vira `float`.
5. **Nomes de clientes**: uma expressão regular (`re.search(r'\d+', ...)`) pega
   o número do cliente e o nome é reescrito como `Cliente_NNN`. Ex.:
   `cliente#016` → `Cliente_016`. A coluna `cliente_fora_do_padrao` guarda
   quais nomes vieram errados.

Depois, `mostrar_relatorio_limpeza()` imprime quantas linhas havia, quantas
foram removidas (e por qual motivo) e quantos nomes de clientes foram corrigidos.

### 4. Colunas derivadas (`transformacoes.py`)

| Coluna               | Como é calculada                                           |
|----------------------|------------------------------------------------------------|
| `receita_total`      | `quantidade * preco_unitario`                              |
| `mes`, `ano`         | extraídos de `data_venda`                                  |
| `mes_nome`           | nome do mês em português                                   |
| `trimestre`          | `Q1` (jan–mar), `Q2` (abr–jun), `Q3` (jul–set), `Q4` (out–dez) |
| `faixa_receita_item` | `Baixo Valor` (< R$ 500), `Medio Valor` (< R$ 5.000), `Alto Valor` |

### 5. Métricas (`metricas.py`)

Calculadas com `groupby`:

- **Por mês**: receita total, quantidade vendida e número de vendas;
- **Top 5 produtos** por receita;
- **Receita por categoria**;
- **Por região**: receita total e ticket médio (receita média por venda).

### 6. Segmentação de clientes (`segmentacao.py`)

Soma o gasto total de cada cliente e o classifica:

| Segmento | Total gasto                 |
|----------|-----------------------------|
| Ouro     | acima de R$ 15.000          |
| Prata    | de R$ 5.000 até R$ 15.000   |
| Bronze   | abaixo de R$ 5.000          |

Os limites ficam em `src/config.py` (`LIMITE_OURO` e `LIMITE_PRATA`).
O programa mostra os 10 clientes que mais gastaram e quantos clientes há em
cada segmento.

---

## Dicionário de dados (`vendas.csv`)

| Coluna           | Tipo    | Descrição                                   |
|------------------|---------|---------------------------------------------|
| `id_venda`       | inteiro | Identificador da venda (1, 2, 3...)         |
| `data_venda`     | texto   | Data no formato `AAAA-MM-DD`                |
| `cliente`        | texto   | Nome do cliente, padrão `Cliente_NNN`       |
| `produto`        | texto   | Notebook, Smartphone, Tablet, Monitor, Teclado, Mouse ou Headset |
| `categoria`      | texto   | Computadores, Celulares ou Perifericos      |
| `regiao`         | texto   | Sudeste, Sul, Nordeste, Centro-Oeste ou Norte |
| `quantidade`     | inteiro | Unidades vendidas (1 a 10)                  |
| `preco_unitario` | decimal | Preço de uma unidade, em R$                 |

---

## Estrutura do projeto

```
ExercicioMeioDoModulo/
├── salesinsight.py        # ponto de entrada: executa todas as etapas
├── vendas.csv             # dados de entrada
├── requirements.txt       # dependências (pandas)
├── planejamento-kanban.md # planejamento das tarefas
└── src/
    ├── config.py          # caminhos, nomes de colunas e constantes
    ├── gerador.py         # geração do dataset sintético
    ├── data.py            # carga, inspeção, limpeza e relatório de limpeza
    ├── transformacoes.py  # colunas derivadas
    ├── metricas.py        # métricas agregadas
    └── segmentacao.py     # segmentação de clientes
```

Para alterar algum comportamento, o ponto de partida costuma ser o
`src/config.py`: nome do arquivo, colunas, formato de data, padrão do nome do
cliente e limites dos segmentos estão todos lá.

---

## Conceitos de Python usados

| Conceito                     | Onde aparece                                          |
|------------------------------|-------------------------------------------------------|
| pandas (`read_csv`, `dropna`, `groupby`, `agg`) | `data.py`, `metricas.py`           |
| `datetime` (`strptime`, `timedelta`) | `data.py` (conversão de datas), `gerador.py` |
| Expressões regulares (`re`)  | `data.py` (`padronizar_cliente`)                      |
| `try/except`                 | `data.py` (`converter_data`)                          |
| `if/elif/else`               | `transformacoes.py` (trimestre e faixa de receita)    |
| `lambda`                     | `segmentacao.py` (classificação dos clientes)         |
| Módulo `csv` e `random`      | `gerador.py`                                          |
| `pathlib`                    | `config.py` (caminhos dos arquivos)                   |
