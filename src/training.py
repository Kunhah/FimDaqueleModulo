import pandas as pd
from sklearn.model_selection import train_test_split



# Cria uma nova coluna chamada potencia no DataFrame
def potencia(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()  
    df['potencia'] = df['torque_nm'] * df['velocidade_rotacao_rpm']
    return df

