import pandas as pd
from sklearn.model_selection import train_test_split



def potencia(df: pd.DataFrame) -> pd.DataFrame:
    """Cria uma nova coluna chamada potencia no DataFrame."""
    df = df.copy()  
    df['potencia'] = df['torque_nm'] * df['velocidade_rotacao_rpm']
    return df

# NÃO SERVE, DE FATO DIVIDE EM 80/20 COM df.iloc MAS NÃO ESTÁ USANDO stratify=y
# def dividir_treino_teste(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
#     """"Divide o DataFrame em conjuntos de treino e teste, mantendo a proporção de 80% para treino e 20% para teste."""
#     df = df.copy()
#     limite_treino = int(len(df) * 0.8)
#     df_treino = df.iloc[:limite_treino]
#     df_teste = df.iloc[limite_treino:]
#     return df_treino, df_teste

def dividir_treino_teste(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Divide o DataFrame em conjuntos de treino e teste, mantendo a proporção de 80% para treino e 20% para teste."""
    df = df.copy()
    df_treino, df_teste = train_test_split(df, test_size=0.2, random_state=42, stratify=df['falha_maquina'])
    return df_treino, df_teste