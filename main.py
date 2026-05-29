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
# Valores nulos por coluna
print("nulos:")
# Duplicatas
print(df.isnull().sum())
print("duplicatas:", df.duplicated().sum())
# Categoria inválida '#N/D' em PR_CAT
print("registros com #N/D:", (df["PR_CAT"] == "#N/D").sum())
# Colunas sem nome
colunas_sem_nome = [c for c in df.columns if "Unnamed" in c]
print("colunas sem nome:", colunas_sem_nome)
print()


print("LIMPEZA")
# Remover colunas Unnamed
df.drop(columns=colunas_sem_nome, inplace=True)
df["PR_CAT"] = df["PR_CAT"].replace("#N/D", "Sem Categoria")

# Remover duplicatas
antes = len(df)
df.drop_duplicates(inplace=True)
print(f"duplicatas removidas: {antes - len(df)}")

# Converter DATA para datetime
df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True)

# Como o dataframe ficou após a limpeza
print(df.dtypes)
print(df.head())