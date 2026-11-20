# Manutenção Preditiva: prevendo falhas em máquinas

Projeto de encerramento do Módulo 1 (Desenvolvimento de IA para Análise Preditiva). A ideia é montar um pipeline completo de ciência de dados, da análise dos dados até a escolha do modelo final.

## Qual problema isso resolve

Uma fábrica tem máquinas monitoradas por sensores e quer saber **antes** se uma máquina vai quebrar, para não parar a linha de produção. A variável que eu quero prever é a `falha_maquina`: 1 quando a máquina falhou e 0 quando funcionou normalmente.

A base (`data/manutencao_preditiva.csv`) tem 10.000 máquinas e 14 colunas: temperatura do ar e do processo, velocidade de rotação, torque, desgaste da ferramenta, o tipo da máquina (L, M ou H) e as colunas de falha. Só **3,4%** das máquinas falharam, então a base é bem desbalanceada, e isso pesou em várias decisões do projeto.

## O que o projeto faz

Tudo está no notebook `manutencao_preditiva.ipynb`, dividido nas 7 fases do enunciado. O código das funções fica na pasta `src/` e o notebook só chama essas funções e explica as decisões.

1. **EDA:** dimensões, tipos, `describe()` e três gráficos (barras da classe alvo, histogramas e mapa de calor da correlação de Pearson).
2. **Limpeza:** remove duplicados (não havia nenhum), preenche os 500 nulos de cada sensor com a média e faz boxplots para olhar os outliers.
3. **Feature engineering:** cria a coluna `potencia = torque_nm * velocidade_rotacao_rpm`.
4. **Divisão e balanceamento:** separa X e y, divide em 80% treino e 20% teste com `stratify=y` e aplica o SMOTE **só no treino**.
5. **Escalonamento:** `StandardScaler` só para o KNN. A árvore fica sem escala.
6. **Overfitting:** KNN com K = 3, 5 e 7 e árvore com `max_depth` = 3, 5 e `None`, comparando a acurácia de treino e de teste.
7. **Veredito:** compara o melhor KNN com a melhor árvore na base de teste.

## Estrutura do projeto

```
FimDaqueleModulo/
├── manutencao_preditiva.ipynb   # notebook principal, com as 7 fases e as explicações
├── main_temp.py                 # script de teste rápido: só gera os gráficos da EDA
├── requirements.txt             # bibliotecas e versões usadas
├── data/
│   └── manutencao_preditiva.csv # base de dados (10.000 máquinas)
├── src/
│   ├── data.py                  # carga, inspeção e limpeza
│   ├── graphs.py                # gráficos da EDA e boxplots
│   └── training.py              # feature engineering, divisão, SMOTE, escala e modelos
└── ExercicioMeioDoModulo/       # a outra atividade (ver o final deste README)
```

### O que cada arquivo em `src/` faz

**`src/data.py`: carga, inspeção e limpeza (Fases 1 e 2)**

| Função | O que faz |
|---|---|
| `carregar_dados()` | Lê o `data/manutencao_preditiva.csv` usando um caminho relativo à pasta do projeto. |
| `explorar(df)` | Mostra as primeiras linhas, o formato (linhas × colunas), os tipos, o `describe()` e a contagem de nulos. |
| `contar_espacos_extras(df)` | Conta quantos valores de `id_produto` e `tipo` têm espaços sobrando no início ou no fim. |
| `remover_espacos(df)` | Aplica `strip()` nessas duas colunas e mostra a contagem antes e depois. |
| `remover_duplicados(df)` | Remove linhas que são cópias exatas de outra (`drop_duplicates`). |
| `imputar_nulos(df)` | Preenche os nulos dos quatro sensores (temperaturas, torque e rotação) com a média de cada coluna. |
| `limpar_dados(df)` | Roda as três etapas acima, em ordem, e devolve os dados limpos e um relatório (linhas iniciais e finais, duplicados removidos, nulos preenchidos por coluna). |

**`src/graphs.py`: gráficos (Fases 1 e 2)**

Todos os gráficos usam as mesmas cores: azul para máquinas normais e vermelho para máquinas com falha.

| Função | O que faz |
|---|---|
| `plotar_grafico_barras(df)` | Barras com a quantidade e a porcentagem de máquinas normais e com falha, para mostrar o desbalanceamento. |
| `plotar_histogramas(df)` | Um histograma por sensor, com as barras de normal e falha lado a lado, para comparar as distribuições. |
| `plotar_heatmap(df)` | Mapa de calor da correlação de Pearson entre os sensores e a `falha_maquina`. |
| `plotar_boxplots(df)` | Um boxplot por sensor, para identificar outliers. |

**`src/training.py`: preparação e modelos (Fases 3 a 7)**

| Função | Fase | O que faz |
|---|---|---|
| `potencia(df)` | 3 | Cria a coluna `potencia = torque_nm * velocidade_rotacao_rpm`. |
| `dividir_e_balancear(df)` | 4 | Separa X e y, transforma o `tipo` (L/M/H) em colunas numéricas, divide em 80/20 com `stratify=y` e aplica o SMOTE só no treino. Tira do X o `udi`, o `id_produto` e todas as colunas de falha, para o modelo não "ver a resposta". |
| `escalar_para_knn(X_treino, X_teste)` | 5 | Aplica o `StandardScaler` nas colunas contínuas: `fit_transform` no treino e `transform` no teste. Devolve cópias, então os dados da árvore continuam sem escala. |
| `testar_knn(...)` | 6 | Treina o KNN com K = 3, 5 e 7 e devolve uma tabela com a acurácia de treino, a de teste e a diferença entre elas (`gap`). |
| `testar_arvore(...)` | 6 | Faz o mesmo com a árvore, usando `max_depth` = 3, 5 e `None`. |
| `veredito(tabela_knn, tabela_arvore)` | 7 | Escolhe a melhor configuração de cada modelo pela acurácia no teste, compara as duas e diz qual venceu. |

## Resultados

Todos os números abaixo saem do notebook e podem ser reproduzidos, porque a divisão, o SMOTE e a árvore usam `random_state=42`.

### O que a EDA mostrou

- **Base desbalanceada:** 9.661 máquinas normais (96,6%) e só 339 com falha (3,4%).
- **Nulos:** 500 em cada um dos quatro sensores (temperatura do ar, temperatura do processo, torque e rotação), ou seja, 5% de cada coluna.
- **Correlação com a falha:** todas são fracas. As mais altas são o torque (0,18), a potência (0,17) e o desgaste da ferramenta (0,11). Nenhum sensor sozinho explica a falha, então faz sentido usar todos juntos no modelo.
- **Tipos de máquina:** 6.000 do tipo L, 2.997 do tipo M e 1.003 do tipo H.

### Limpeza e preparação

| Etapa | Resultado |
|---|---|
| Duplicados | Nenhum encontrado (continuaram 10.000 linhas). |
| Nulos | 2.000 valores preenchidos com a média (500 por sensor). Nenhuma linha foi descartada. |
| Divisão 80/20 | 8.000 no treino e 2.000 no teste, os dois com cerca de 3,4% de falhas graças ao `stratify=y`. |
| SMOTE (só no treino) | O treino foi de 7.729 normais e 271 falhas para 7.729 de cada (15.458 linhas). |
| Teste | Ficou como estava: 1.932 normais e 68 falhas. |

### KNN (dados escalados)

| K | Acurácia no treino | Acurácia no teste | Gap |
|---|---|---|---|
| **3** | 96,8% | **90,5%** | 6,3 p.p. |
| 5 | 95,8% | 89,5% | 6,3 p.p. |
| 7 | 95,2% | 88,8% | 6,4 p.p. |

As três versões têm um gap de cerca de 6 pontos, um overfitting moderado. Aumentar o K diminuiu a acurácia no treino e no teste sem reduzir o gap. O K = 3 foi o melhor no teste.

### Árvore de Decisão (dados sem escala)

| `max_depth` | Acurácia no treino | Acurácia no teste | Gap |
|---|---|---|---|
| 3 | 85,6% | 84,7% | 0,9 p.p. |
| 5 | 90,1% | 90,2% | -0,1 p.p. |
| **None** | 99,6% | **93,0%** | 6,6 p.p. |

- **`max_depth=3`:** a árvore é rasa demais e erra mais que as outras, tanto no treino quanto no teste (underfitting).
- **`max_depth=5`:** é a configuração mais estável. O treino e o teste dão praticamente o mesmo resultado.
- **`max_depth=None`:** a árvore cresce sem limite e quase decora o treino (99,6%), o que é sinal claro de overfitting. Mesmo assim, teve a maior acurácia no teste.

### Veredito

| Modelo | Melhor configuração | Acurácia no teste |
|---|---|---|
| KNN | K = 3 | 90,5% |
| Árvore de Decisão | `max_depth=None` | **93,0%** |

Pelo critério do enunciado, que é a maior acurácia no teste, **o modelo indicado é a Árvore de Decisão**, 2,5 pontos acima do melhor KNN. Se a prioridade for um modelo mais previsível, que não decore o treino, a árvore com `max_depth=5` é a alternativa: perde 2,8 pontos de acurácia, mas tem o mesmo desempenho no treino e no teste.

**Um cuidado importante:** todas as acurácias ficaram abaixo de 96,6%, que é o quanto acertaria um modelo que sempre responde "não falha". Isso acontece porque o SMOTE faz o modelo dar mais atenção às falhas, e ele passa a dar alguns alarmes falsos em máquinas normais. Para esse problema, a acurácia sozinha não mostra se o modelo realmente encontra as máquinas que vão falhar. Por isso a primeira melhoria da lista abaixo é olhar outras métricas. A análise completa está no notebook.

## Tecnologias

- Python 3 (testei com a versão 3.14)
- pandas e numpy para os dados
- matplotlib e seaborn para os gráficos
- scikit-learn para os modelos (KNN e Árvore de Decisão), a divisão e o `StandardScaler`
- imbalanced-learn para o SMOTE

## Como executar

```bash
git clone <link do repositório>
cd FimDaqueleModulo

python -m venv .venv
source .venv/bin/activate        # no Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install ipykernel            # para abrir o notebook no VS Code ou no Jupyter
```

Depois é só abrir o `manutencao_preditiva.ipynb` e rodar todas as células, na ordem. Os dados são lidos com caminho relativo (`data/manutencao_preditiva.csv`), então não precisa configurar nada.

## Vídeo de demonstração



---

# DISCLAIMER SOBRE O USO DE IA

A IA foi utilizada da seguinte forma no projeto:
- Para corrigir eventuais erros, formatações errôneas nos gráficos
- Gerar exemplos genéricos de sintaxe como foi dito que é permitido
- Para me ajudar em algumas chamadas de funções as quais eu não sei todos os paramêtros, por exemplo:

```python
    sns.histplot(data=df, x=col, hue='falha_maquina',
        palette=list(CORES.values()), multiple='', bins=30,
        alpha=0.8, legend=False, ax=ax)

```

Admito, sem me basear em código de outros desenvolvedores, e sem usar IA, eu **NÃO** conseguiria desenvolver isso,
**NÃO** possuo todo o conhecimento de python memorizado de cada função que usei, porém considero que esse é o padrão normal
para o desenvolvimento de software
O arquivo ipynb foi feit com auxílio de IA pois me faltou tempo para finalizar

# NÃO ENTREGUEI A OUTRA ATIVIDADE

Por causa disso, está no mesmo repositório, na pasta ExercícioMeioDoModulo. O uso de IA foi maior neste, mas mesmo assim não fiz "vibe code" e realizei parte por parte mantendo controle de cada linha
