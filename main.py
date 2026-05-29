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

print()
print("ESTATÍSTICAS")
# CL_FHL (Número de Filhos)
filhos = df["CL_FHL"]
print("media:", filhos.mean())
print("mediana:", filhos.median())
print("desvio:", filhos.std())
print("moda:", filhos.mode()[0])
print("min:", filhos.min())
print("max:", filhos.max())
print("contagem:", filhos.count())
print("Q1:", filhos.quantile(0.25))
print("Q2:", filhos.quantile(0.50))
print("Q3:", filhos.quantile(0.75))
print()

print("AGRUPAMENTOS")
# Compras por Gênero
print(df.groupby("CL_GENERO")["CO_ID"].count())
print()
# Vendas por Categoria de Produto
print(df.groupby("PR_CAT")["PR_ID"].count().sort_values(ascending=False))
print()
# Pivot: Gênero × Segmento
pivot = pd.pivot_table(df, values="CO_ID", index="CL_GENERO", columns="CL_SEG", aggfunc="count")
print(pivot)