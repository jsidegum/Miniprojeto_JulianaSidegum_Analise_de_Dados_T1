# =============================================================================
# ANÁLISE EXPLORATÓRIA DE DADOS — BASE VAREJO
# =============================================================================
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# SPRINT 1 - IMPORTAÇÃO DOS DADOS
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 65)
print("SPRINT 1 — CARREGAMENTO DA BASE")
print("=" * 65)

# Leitura do CSV com detecção automática de separador
df = pd.read_csv("varejo.csv", sep=None, engine="python")

print(f"Registros carregados : {df.shape[0]:,}")
print(f"Colunas encontradas  : {df.shape[1]}")
print()
print("Colunas e tipos de dados (originais):")
print(df.dtypes)

# Primeiras linhas — confirma visualmente que o arquivo foi lido corretamente
print("- Primeiras 5 linhas (df.head):")
print(df.head())
print()

# Últimas linhas — detecta possíveis lixos no final do arquivo
print("- Últimas 5 linhas (df.tail):")
print(df.tail())
print()

# info() mostra: colunas, tipo de cada uma E quantos valores não nulos existem
# É o comando mais completo para uma primeira inspeção — equivale a dtypes + contagem de nulos em uma linha só
print("- Resumo geral do dataframe (df.info):")
df.info()
print()

# describe() calcula automaticamente média, desvio, min, max e quartis
# para TODAS as colunas numéricas — útil para detectar outliers e escala dos dados
print("- Estatísticas das colunas numéricas (df.describe):")
print(df.describe())

# ─────────────────────────────────────────────────────────────────────────────
# SPRINT 2 - IDENTIFICAÇÃO DE PROBLEMAS (QUALIDADE DOS DADOS)
# ─────────────────────────────────────────────────────────────────────────────

print()
print("=" * 65)
print("SPRINT 2 — VERIFICAÇÃO DE QUALIDADE")
print("=" * 65)

# Problema 1: Valores nulos por coluna
print("- Problema 1 — Nulos por coluna:")
nulos = df.isnull().sum()
print(nulos[nulos > 0])

# Problema 2: Duplicatas
total_duplicados = df.duplicated().sum()
print(f"\n- Problema 2 — Duplicatas: {total_duplicados:,} linhas duplicadas "
      f"({total_duplicados / len(df) * 100:.1f}% do total)")

# Problema 3: Categoria inválida '#N/D' em PR_CAT
categoria_invalida = (df["PR_CAT"] == "#N/D").sum()
print(f"\n- Problema 3 — Categoria inválida '#N/D' em PR_CAT: {categoria_invalida:,} registros")

# Problema 4: Colunas sem nome
# O loop abaixo percorre todos os nomes e separa os que começam com "Unnamed".
colunas_sem_nome = []
for coluna in df.columns:
    if coluna.startswith("Unnamed"):
        colunas_sem_nome.append(coluna)

print(f"\n- Problema 4 — Colunas sem nome detectadas: {colunas_sem_nome}")


# ─────────────────────────────────────────────────────────────────────────────
# SPRINT 3 — LIMPEZA
# ─────────────────────────────────────────────────────────────────────────────

print()
print("=" * 65)
print("SPRINT 3 — LIMPEZA DOS DADOS")
print("=" * 65)

# Criado uma cópia do dataframe original.
# Isso preserva o df bruto para comparação.
df_limpo = df.copy()

# --- Remover colunas completamente nulas (Unnamed) ---------------
# Justificativa: 100% nulas, sem informação útil; removê-las libera memória.
df_limpo.drop(columns=colunas_sem_nome, inplace=True)
print(f"* Colunas {colunas_sem_nome} removidas (100% nulas).")

# --- Substituir categoria inválida '#N/D' por 'Sem Categoria' ----
# Justificativa: imputar em vez de remover para não perder registros da venda.
df_limpo["PR_CAT"] = df_limpo["PR_CAT"].replace("#N/D", "Sem Categoria")
print("* PR_CAT: '#N/D' substituído por 'Sem Categoria'.")

# --- Eliminar duplicatas -----------------------------------------
# Justificativa: linhas idênticas distorceriam contagens e médias.
antes = len(df_limpo)
df_limpo.drop_duplicates(inplace=True)
depois = len(df_limpo)
print(f"* Duplicatas removidas: {antes - depois:,} | Registros restantes: {depois:,}")

# --- Converter DATA para datetime
# Justificativa: como string não é possível filtrar por período nem ordenar.
# format="%d/%m/%Y" instrui o pandas a ler no padrão brasileiro dia/mês/ano.
# errors="coerce" transforma datas inválidas em NaT em vez de travar o script.
df_limpo["DATA"] = pd.to_datetime(df_limpo["DATA"], format="%d/%m/%Y", errors="coerce")

datas_invalidas = df_limpo["DATA"].isnull().sum()
if datas_invalidas:
    print(f"!!!  {datas_invalidas} datas inválidas após conversão (mantidas como NaT).")
else:
    print("* Coluna DATA convertida para datetime sem erros.")
print()

# Como o dataframe ficou após a limpeza
print("- Tipos de dados após limpeza (df_limpo.dtypes):")
print(df_limpo.dtypes)
print()
print("- Primeiras 5 linhas do df_limpo:")
print(df_limpo.head())
print()
print("- Resumo do df_limpo (df_limpo.info):")
df_limpo.info()

# ─────────────────────────────────────────────────────────────────────────────
# SPRINT 4 - ESTATÍSTICAS DESCRITIVAS: CL_FHL (Número de Filhos)
# ─────────────────────────────────────────────────────────────────────────────
print()
print("=" * 65)
print("SPRINT 4 — ESTATÍSTICAS DESCRITIVAS: CL_FHL (Número de Filhos)")
print("=" * 65)

filhos = df_limpo["CL_FHL"]


media    = filhos.mean()
mediana  = filhos.median()
desvio   = filhos.std()
moda     = filhos.mode()[0]          # mode() retorna Series; pegamos o primeiro
minimo   = filhos.min()
maximo   = filhos.max()
contagem = filhos.count()
q1       = filhos.quantile(0.25)
q2       = filhos.quantile(0.50)     # igual à mediana
q3       = filhos.quantile(0.75)

print(f"  Contagem  : {contagem:,}")
print(f"  Média     : {media:.4f}")
print(f"  Mediana   : {mediana:.1f}")
print(f"  Moda      : {moda:.1f}")
print(f"  Desvio-P  : {desvio:.4f}")
print(f"  Mínimo    : {minimo:.1f}")
print(f"  Máximo    : {maximo:.1f}")
print(f"  Q1 (25%)  : {q1:.1f}")
print(f"  Q2 (50%)  : {q2:.1f}")
print(f"  Q3 (75%)  : {q3:.1f}")


# ─────────────────────────────────────────────────────────────────────────────
# SPRINT 5 - PADRÕES DE AGRUPAMENTO
# ─────────────────────────────────────────────────────────────────────────────

print()
print("=" * 65)
print("SPRINT 5 — PADRÕES DE AGRUPAMENTO")
print("=" * 65)

# --- Agrupamento 1: Compras por Gênero --------------------------------------
print("\n- Agrupamento 1: Total de compras por Gênero (CL_GENERO)")
por_genero = (
    df_limpo.groupby("CL_GENERO")
    .agg(total_compras=("CO_ID", "count"),
         clientes_unicos=("CL_ID", "nunique"))
    .sort_values("total_compras", ascending=False)
)
# Adiciona percentual
por_genero["perc_compras"] = (
    por_genero["total_compras"] / por_genero["total_compras"].sum() * 100
).round(2)

print(por_genero)

# --- Agrupamento 2: Vendas por Categoria de Produto -------------------------
print("\n- Agrupamento 2: Total de itens vendidos por Categoria (PR_CAT)")
por_categoria = (
    df_limpo.groupby("PR_CAT")
    .agg(total_itens=("PR_ID", "count"),
         produtos_distintos=("PR_NOME", "nunique"))
    .sort_values("total_itens", ascending=False)
)
por_categoria["perc_itens"] = (
    por_categoria["total_itens"] / por_categoria["total_itens"].sum() * 100
).round(2)
print(por_categoria)

# --- Pivot: Gênero × Segmento -----------------------------------------------
print("\n- Pivot: Número de compras por Gênero × Segmento (CL_SEG)")
pivot = pd.pivot_table(
    df_limpo,
    values="CO_ID",
    index="CL_GENERO",
    columns="CL_SEG",
    aggfunc="count",
    fill_value=0
)
print(pivot)

# ─────────────────────────────────────────────────────────────────────────────
# RELATÓRIO FINAL - INSIGHTS
# ─────────────────────────────────────────────────────────────────────────────

print()
print("=" * 65)
print("RELATÓRIO FINAL — INSIGHTS E PROBLEMAS REMANESCENTES")
print("=" * 65)

# Calcula indicadores para o relatório
# Gênero com mais compras: ordena e pega a primeira linha
linha_genero = por_genero.sort_values("total_compras", ascending=False).iloc[0]
genero_lider = linha_genero.name
genero_pct   = linha_genero["perc_compras"]

# Categoria mais vendida: ordena e pega a primeira linha
linha_cat = por_categoria.sort_values("total_itens", ascending=False).iloc[0]
cat_top     = linha_cat.name
cat_top_pct = linha_cat["perc_itens"]

# Registros com categoria
if "Sem Categoria" in por_categoria.index:
    sem_cat_n = por_categoria.loc["Sem Categoria", "total_itens"]
else:
    sem_cat_n = 0

print(f"""
INSIGHTS:
  - COLUNAS FANTASMAS: As 4 colunas 'Unnamed' (100% nulas) eram artefatos de
     formatação do arquivo CSV e foram descartadas sem perda de informação útil.

  - QUALIDADE DOS DADOS: A base original continha {total_duplicados:,} linhas duplicadas
     ({total_duplicados / (depois + total_duplicados) * 100:.1f}% do total), indicando possível falha no processo
     de carga ou envio duplo de transações. Após remoção, restaram {depois:,} registros.

  - GÊNERO COM MAIS COMPRAS: Clientes do gênero '{genero_lider}' representam
     {genero_pct:.1f}% das compras totais, sendo o segmento mais ativo da base.

  - CATEGORIA MAIS VENDIDA: '{cat_top}' é a categoria com maior volume de itens,
     concentrando {cat_top_pct:.1f}% de todas as transações.

  - PERFIL DE FILHOS (CL_FHL): A mediana é 0, indicando que a maioria dos
     clientes não possui filhos registrados; a média de {media:.2f} é puxada por
     clientes com até {int(maximo)} filhos. Alta assimetria à direita (desvio={desvio:.2f}).

  - CATEGORIAS PROBLEMÁTICAS: {sem_cat_n:,} registros tiveram categoria substituída
     de '#N/D' para 'Sem Categoria', pois o valor original representa dados ausentes
     na fonte (provavelmente erro de preenchimento no sistema de origem).
""")

print("=" * 65)