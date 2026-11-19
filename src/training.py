import pandas as pd




# Cria uma nova coluna chamada potencia no DataFrame
def potencia(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()  
    df['potencia'] = df['torque_nm'] * df['velocidade_rotacao_rpm']
    return df

