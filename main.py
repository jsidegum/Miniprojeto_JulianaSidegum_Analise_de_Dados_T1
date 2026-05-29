import pandas as pd

print("CARREGAMENTO DA BASE")
df = pd.read_csv("varejo.csv", sep=None, engine="python")

print("registros:", df.shape[0])
print("colunas:", df.shape[1])
print()
print(df.dtypes)

print("head:")
print(df.head())

print("tail:")
print(df.tail())
print(df.info())
print(df.describe())
print()

print("QUALIDADE")
print("nulos:")
print(df.isnull().sum())
print("duplicatas:", df.duplicated().sum())
print("registros com #N/D:", (df["PR_CAT"] == "#N/D").sum())

colunas_sem_nome = [c for c in df.columns if "Unnamed" in c]
print("colunas sem nome:", colunas_sem_nome)
print()