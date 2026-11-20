"""Carga, inspeção e limpeza dos dados de vendas.

A limpeza acontece em etapas, sempre nesta ordem:

1. remover espaços extras das colunas de texto;
2. descartar vendas com data inválida (usa `datetime`);
3. descartar vendas sem quantidade ou sem preço;
4. converter quantidade para int e preço para float;
5. padronizar o nome dos clientes para "Cliente_NNN" (usa `re`).

Cada etapa imprime um "antes e depois" para mostrar o que mudou.
No final, `limpar_dados` devolve o DataFrame limpo e um relatório
com tudo o que foi removido e o motivo.
"""

import re
from datetime import datetime

import pandas as pd

from .config import (
    COLUNAS_CRITICAS,
    COLUNAS_TEXTO,
    CSV_VENDAS,
    FORMATO_DATA,
    PADRAO_CLIENTE,
)


# ---------------------------------------------------------------------------
# Carga e inspeção
# ---------------------------------------------------------------------------

def carregar_dados() -> pd.DataFrame:
    """Lê o CSV de vendas e devolve um DataFrame (ainda "sujo")."""
    return pd.read_csv(CSV_VENDAS)


def explorar(df: pd.DataFrame) -> None:
    """Mostra uma visão geral do dataset: primeiras linhas, tipos, estatísticas e nulos."""
    print('\n=== INSPECAO INICIAL DO DATASET ===')
    print(df.head())
    print('Formato (linhas, colunas):', df.shape)
    print('Colunas:', list(df.columns))
    df.info()
    print(df.describe())
    print('\nValores nulos por coluna:')
    print(df.isnull().sum().sort_values(ascending=False))


# ---------------------------------------------------------------------------
# Etapas da limpeza
# ---------------------------------------------------------------------------

def remover_espacos(df: pd.DataFrame) -> pd.DataFrame:
    """Etapa 1: tira espaços do início e do fim das colunas de texto.

    Ex.: " Notebook " -> "Notebook".
    """
    def contar_com_espacos() -> pd.Series:
        # Conta, por coluna, quantos valores mudam quando aplicamos strip().
        return pd.Series({c: (df[c] != df[c].str.strip()).sum() for c in COLUNAS_TEXTO})

    print('\n[Espacos] Campos com espacos extras antes:')
    print(contar_com_espacos())
    for coluna in COLUNAS_TEXTO:
        df[coluna] = df[coluna].str.strip()
    print('[Espacos] Campos com espacos extras depois:')
    print(contar_com_espacos())
    return df


def converter_data(texto: str) -> datetime | None:
    """Converte um texto "AAAA-MM-DD" em datetime.

    Devolve None se o texto não for uma data válida (ex.: "DATA INVALIDA").
    """
    try:
        return datetime.strptime(texto, FORMATO_DATA)
    except ValueError:
        return None


def remover_datas_invalidas(df: pd.DataFrame) -> pd.DataFrame:
    """Etapa 2: converte `data_venda` para data e descarta as que não puderam ser lidas."""
    df['data_venda'] = pd.to_datetime(df['data_venda'].apply(converter_data))
    invalidas = df['data_venda'].isnull()
    print(f'\n[Datas] Datas invalidas removidas: {invalidas.sum()} '
          f'(id_venda: {df.loc[invalidas, "id_venda"].tolist()})')
    return df[~invalidas]


def remover_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """Etapa 3: descarta vendas sem quantidade ou sem preço (não dá para calcular a receita)."""
    print('\n[Nulos] Ausentes antes:')
    print(df[COLUNAS_CRITICAS].isnull().sum())
    df_limpo = df.dropna(subset=COLUNAS_CRITICAS)
    print(f'[Nulos] Registros removidos: {len(df) - len(df_limpo)}')
    return df_limpo


def converter_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """Etapa 4: ajusta os tipos numéricos.

    O pandas lê `quantidade` como float porque a coluna tinha valores vazios.
    Depois de remover os nulos, ela pode virar int.
    """
    df = df.copy()  # evita o aviso SettingWithCopyWarning do pandas
    df['quantidade'] = df['quantidade'].astype(int)
    df['preco_unitario'] = df['preco_unitario'].astype(float)
    print('\n[Tipos] Tipos depois da conversao:')
    print(df[['data_venda'] + COLUNAS_CRITICAS].dtypes)
    return df


def padronizar_cliente(nome: str) -> str:
    """Reescreve um nome de cliente no formato "Cliente_NNN".

    Pega o número que aparece no nome (com uma expressão regular) e monta
    o nome de novo. Exemplos:

        "CLIENTE-016"   -> "Cliente_016"
        "Cliente_016!!" -> "Cliente_016"
        "cliente#016"   -> "Cliente_016"

    Se não houver número no nome, ele é devolvido sem alteração.
    """
    numero = re.search(r'\d+', nome)
    if numero is None:
        return nome
    return f'Cliente_{int(numero.group()):03d}'


def padronizar_clientes(df: pd.DataFrame) -> pd.DataFrame:
    """Etapa 5: aplica `padronizar_cliente` em toda a coluna `cliente`.

    Também cria a coluna `cliente_fora_do_padrao` (True/False) para registrar
    quais nomes vieram errados no arquivo original.
    """
    original = df['cliente']
    df['cliente_fora_do_padrao'] = ~original.str.fullmatch(PADRAO_CLIENTE)
    df['cliente'] = original.apply(padronizar_cliente)

    corrigidos = df.loc[df['cliente_fora_do_padrao'], 'cliente']
    print(f'\n[Clientes] Nomes fora do padrao Cliente_NNN: {len(corrigidos)}')
    print(pd.DataFrame({'antes': original[corrigidos.index], 'depois': corrigidos}).head())

    ainda_fora = ~df['cliente'].str.fullmatch(PADRAO_CLIENTE)
    if ainda_fora.any():
        print(f'[Clientes] Nao foi possivel padronizar: {df.loc[ainda_fora, "cliente"].tolist()}')
    return df


# ---------------------------------------------------------------------------
# Função principal da limpeza
# ---------------------------------------------------------------------------

def limpar_dados(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Executa todas as etapas da limpeza, em ordem.

    Returns:
        (df_limpo, relatorio), em que `relatorio` é um dicionário com:
            - iniciais: número de linhas antes da limpeza;
            - finais: número de linhas depois da limpeza;
            - clientes_sinalizados: quantos nomes de cliente foram corrigidos;
            - removidos: DataFrame com as linhas descartadas e a coluna `motivo`.
    """
    print('\n=== LIMPEZA DOS DADOS ===')
    bruto = df.copy()  # guarda o original para montar o relatório

    df = remover_espacos(df.copy())

    df = remover_datas_invalidas(df)
    sem_data = bruto.index.difference(df.index)

    df = remover_nulos(df)
    sem_valor = bruto.index.difference(df.index).difference(sem_data)

    df = converter_tipos(df)
    df = padronizar_clientes(df)

    removidos = pd.concat([
        bruto.loc[sem_data].assign(motivo='data invalida'),
        bruto.loc[sem_valor].assign(motivo='valor ausente'),
    ])
    relatorio = {
        'iniciais': len(bruto),
        'finais': len(df),
        'clientes_sinalizados': int(df['cliente_fora_do_padrao'].sum()),
        'removidos': removidos,
    }
    return df, relatorio


def mostrar_relatorio_limpeza(relatorio: dict) -> None:
    """Imprime o resumo da limpeza: quantas linhas entraram, saíram e por quê."""
    removidos = relatorio['removidos']
    print('\n=== RELATORIO DE LIMPEZA ===')
    print(f'Registros iniciais: {relatorio["iniciais"]}')
    print(f'Total removido: {len(removidos)}')
    print(f'Registros finais: {relatorio["finais"]}')
    print(f'Clientes corrigidos (estavam fora do padrao): {relatorio["clientes_sinalizados"]}')
    print('\nRemovidos por motivo:')
    print(removidos['motivo'].value_counts().to_string())
    print('\nRegistros removidos:')
    print(removidos.to_string(index=False))
