import pandas as pd

print("CARREGAMENTO DA BASE")
df = pd.read_csv("varejo.csv", sep=None, engine="python")

print("registros:", df.shape[0])
print("colunas:", df.shape[1])
print()
print(df.dtypes)