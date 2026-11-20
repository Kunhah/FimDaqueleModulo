from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # backend sem janela: os gráficos só são salvos em arquivo
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch

PASTA_SAIDA = Path(__file__).resolve().parent.parent / 'outputs'

# Estilo visual padrão para todos os gráficos
sns.set_theme(style='whitegrid')

CORES = {'Normal': 'steelblue', 'Falha': 'crimson'}
COLUNAS = ['temperatura_ar_k', 'temperatura_processo_k',
            'velocidade_rotacao_rpm', 'torque_nm',
            'desgaste_ferramenta_min']


def salvar(nome):
    """Salva a figura atual em outputs/<nome>.png e a fecha."""
    PASTA_SAIDA.mkdir(exist_ok=True)
    plt.savefig(PASTA_SAIDA / f'{nome}.png', dpi=150)
    plt.close()


def plotar_grafico_barras(df):
    """Plota a quantidade e a porcentagem de máquinas normais e com falha."""
    # Conta a quantidade de máquinas normais e com falha
    contagem = df['falha_maquina'].value_counts().sort_index()
    # Cria a figura e o eixo do gráfico
    _, ax = plt.subplots(figsize=(6, 4))
    # Plota o gráfico de barras com as cores definidas (azul para normal e vermelho para falha)
    barras = ax.bar(CORES.keys(), contagem, color=CORES.values())
    # Adiciona os rótulos de contagem e porcentagem acima das barras, funciona da seguinte forma: para cada barra, pega o valor da contagem e calcula a porcentagem em relação ao total de registros no DataFrame, formatando como "n (x%)"
    ax.bar_label(barras, labels=[f'{n} ({n / len(df):.1%})' for n in contagem])
    # Define o título
    ax.set_title('Máquinas normais x com falha')
    # Define o rótulo do eixo y
    ax.set_ylabel('Quantidade de máquinas')

    plt.tight_layout()
    salvar('grafico_barras')

def plotar_histogramas(df):
    """Plota histogramas empilhados: a parte vermelha são as máquinas com falha."""
    # Cria uma figura com 2 linhas e 3 colunas de subplots (gráfico), com tamanho total de 15x8
    _, axes = plt.subplots(2, 3, figsize=(15, 8))
    # Achata a matriz de eixos para que retorne uma lista de eixos, facilitando a iteração sobre eles
    axes = axes.flatten()
    # Para cada eixo (gráfico) e coluna na lista de COLUNAS, plota dois histogramas usando seaborn, 
    # com a coluna atual do DataFrame no eixo x, a falha da máquina como hue 
    # (isso indica para a função que esta coluna deve ser usada para diferenciar as cores),
    # cores definidas no dicionário CORES, e o método o qual os histogramas vão ser mostrados juntos
    for ax, col in zip(axes, COLUNAS):
        sns.histplot(data=df, x=col, hue='falha_maquina',
                     palette=list(CORES.values()), multiple='dodge', bins=30,
                     alpha=0.8, legend=False, ax=ax)
        ax.set_title(col)
        ax.set_ylabel('Quantidade de máquinas')
    # Realiza a contagem de máquinas normais e com falha, ordenando pelo índice (Normal, Falha) 
    contagem = df['falha_maquina'].value_counts().sort_index()
    # Cria uma legenda personalizada para o último eixo (gráfico) com as cores e a contagem de cada categoria
    legenda = [Patch(color=cor, label=f'{nome} ({n} máquinas)')
               for (nome, cor), n in zip(CORES.items(), contagem)]
    # Desliga o eixo do último gráfico (não é para mostrar um histograma ali pois são apenas 5 gráficos para 6 subplots)
    axes[-1].axis('off')
    axes[-1].legend(handles=legenda, loc='center', fontsize=12)

    plt.tight_layout()
    salvar('histogramas')

def plotar_heatmap(df):
    """Plota um heatmap de correlação entre as COLUNAS e a falha."""
    # Calcula a correlação de Pearson entre as COLUNAS e a coluna 'falha_maquina' do DataFrame, criando uma matriz de correlação
    corr = df[COLUNAS + ['falha_maquina']].corr(method='pearson')
    # Cria uma figura e um eixo para o heatmap, com tamanho de 9x7
    _, ax = plt.subplots(figsize=(9, 7))
    # Plota o heatmap usando seaborn, com a matriz de correlação, anotando os valores dentro das células
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r',
                center=0, vmin=-1, vmax=1,
                square=True, linewidths=0.5, ax=ax)
    ax.set_title('Correlação de Pearson — COLUNAS × falha')
    plt.tight_layout()
    salvar('heatmap_correlacao')

def plotar_boxplots(df):
    """Plota o boxplot para cada coluna informada do DataFrame."""
    # Para cada coluna na lista de colunas fornecida, cria um boxplot
    # Eu poderia por todos os boxplots em uma única figura da mesma forma que fiz com os histogramas, 
    # porém, preferi mostrar um por vez para melhor visualização
    for coluna in COLUNAS:
        # Cria uma figura para o boxplot da coluna atual
        plt.figure(figsize=(8, 3))
        # Plota o boxplot usando seaborn, com a coluna atual do DataFrame
        sns.boxplot(x=df[coluna])
        # Define o título do boxplot com o nome da coluna
        plt.title(f'Boxplot - {coluna}')

        plt.tight_layout()
        salvar(f'boxplot_{coluna}')
