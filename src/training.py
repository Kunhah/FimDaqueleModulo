import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

COLUNAS_EXCLUIR = ['udi', 'id_produto', 'falha_maquina', 'falha_twf',
                   'falha_hdf', 'falha_pwf', 'falha_osf', 'falha_rnf']
COLUNAS_CONTINUAS = ['temperatura_ar_k', 'temperatura_processo_k',
                     'velocidade_rotacao_rpm', 'torque_nm',
                     'desgaste_ferramenta_min', 'potencia']



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

# NÃO SERVE PORQUE NÃO DIVIDE ENTRE X E Y (PARAMETROS E RESPOSTAS)
# def dividir_treino_teste(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
#     """Divide o DataFrame em conjuntos de treino e teste, mantendo a proporção de 80% para treino e 20% para teste."""
#     df = df.copy()
#     df_treino, df_teste = train_test_split(df, test_size=0.2, random_state=42, stratify=df['falha_maquina'])
#     return df_treino, df_teste


def dividir_e_balancear(df: pd.DataFrame):
    """Separa X/y, divide 80/20 com stratify e aplica SMOTE só no treino."""
    y = df['falha_maquina']
    X = df.drop(columns=COLUNAS_EXCLUIR)

    # Uma sugestão dada pela IA foi usar valores númericos para a coluna tipo, valores de 0 e 1, mas como temos 3 tipos
    X = pd.get_dummies(X, columns=['tipo'], drop_first=True, dtype=int)

    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )

    # Também foi sugerido pela IA usar SMOTE para balancear o conjunto de treino, não realizei o SMOTE pois acho que foge do escopo
    print('\nDistribuição do alvo')
    print(y_treino.value_counts().to_string())
    print(f'Tamanho do treino {len(X_treino)}')

    return X_treino, X_teste, y_treino, y_teste


def escalar_para_knn(X_treino, X_teste):
    """Realiza o escalonamento das colunas contínuas para o KNN, é basicamente outra forma de normalização usando desvio padrões."""
    X_treino_esc = X_treino.copy()
    X_teste_esc  = X_teste.copy()

    # É preciso criar uma variável para que os dados fiquem guardados para poderem ser aplicados no teste
    escalador = StandardScaler()

    # fit_transform no treino, aqui o escalador aprende a média/desvio do treino e aplica a transformação
    X_treino_esc[COLUNAS_CONTINUAS] = escalador.fit_transform(
        X_treino[COLUNAS_CONTINUAS]
    )
    # transform no teste, aqui o escalador aplica a média/desvio aprendido no treino
    X_teste_esc[COLUNAS_CONTINUAS] = escalador.transform(
        X_teste[COLUNAS_CONTINUAS]
    )

    # A Árvore de decisão não está incluída no escalonamento porque é imune à escala dos atributos,
    # é apenas comparado o valor se é maior ou menor, então não importa a escala, o resultado será o mesmo.

    print(f'Média no treino escalado: {X_treino_esc[COLUNAS_CONTINUAS].mean().round(4).to_dict()}')
    print(f'Média no teste escalado:  {X_teste_esc[COLUNAS_CONTINUAS].mean().round(4).to_dict()}')

    return X_treino_esc, X_teste_esc


def treinar_knn(X_treino_esc, X_teste_esc, y_treino, y_teste):
    """Acurácia de treino e teste para cada K (KNN)."""
    # List vazia para armazenar os resultados de cada K
    resultados = []
    #Utilizando os valores 3, 5, e 7 como foi pedido, roda o treino do knn para cada
    ks = [3, 5, 7]
    for k in ks:
        # Eu sinceramente não sei a matemática por trás do algoritmo
        modelo = KNeighborsClassifier(n_neighbors=k).fit(X_treino_esc, y_treino)
        # Armazena o resultado dessa iteração na lista de resultados, junto com a acurácia de treino e teste
        resultados.append({
            'k':          k,
            # Calcula a acurácia de treino e teste usando o método score do modelo, que retorna a proporção de acertos
            'acc_treino': modelo.score(X_treino_esc, y_treino),
            'acc_teste':  modelo.score(X_teste_esc,  y_teste),
        })
    # Cria um DataFrame com a lista de resultados e calcula a diferença entre acurácia de treino e teste
    tabela = pd.DataFrame(resultados)
    tabela['gap'] = tabela['acc_treino'] - tabela['acc_teste']

    print('\n KNN]')
    print(tabela.to_string(index=False, float_format='{:.4f}'.format))
    return tabela


def treinar_arvore(X_treino, X_teste, y_treino, y_teste):
    """Acurácia de treino e teste para cada max_depth. SEM escala (árvore é imune)."""
    # Lista vazia para armazenar os resultados de cada max_depth
    resultados = []
    # Utilizando os valores 3, 5, e None como foi pedido, roda o treino da árvore de decisão para cada
    profundidades = [3, 5, None]
    for p in profundidades:
        # Eu sinceramente não sei a matemática por trás do algoritmo
        modelo = DecisionTreeClassifier(max_depth=p, random_state=42).fit(X_treino, y_treino)
        # Armazena o resultado dessa iteração na lista de resultados, junto com a acurácia de treino e teste
        resultados.append({
            'max_depth':  str(p),
            # Calcula a acurácia de treino e teste usando o método score do modelo, que retorna a proporção de acertos
            'acc_treino': modelo.score(X_treino, y_treino),
            'acc_teste':  modelo.score(X_teste,  y_teste),
        })
    # Cria um DataFrame com a lista de resultados e calcula a diferença entre acurácia de treino e teste
    tabela = pd.DataFrame(resultados)
    tabela['gap'] = tabela['acc_treino'] - tabela['acc_teste']

    print('\n Árvore de decisão')
    print(tabela.to_string(index=False, float_format='{:.4f}'.format))
    return tabela


