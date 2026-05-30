# Mini Projeto — Análise Exploratória de Dados (Varejo)

## Como executar

Abra a pasta do projeto no VS Code e execute no terminal:

```bash
python -m venv .venv
```

Ative o ambiente virtual:

```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

Instale as dependências e execute:

```bash
pip install -r requirements.txt
python main.py
```

O relatório completo será exibido no terminal.

---

# Estrutura do Projeto

```
📁 Miniprojeto_JulianaSidegum_Analise_de_Dados_T1/
 ├── .gitignore
 ├── LICENSE
 ├── README.md
 ├── main.py
 ├── requirements.txt
 └── varejo.csv
```

---

# Principais Insights

- A base possuía muitas linhas duplicadas, indicando possível problema no processo de carga dos dados.
- Clientes do gênero feminino apresentaram maior volume de compras.
- A categoria ALIMENTOS foi a mais vendida da base.
- A maioria dos clientes não possui filhos cadastrados.
- Registros com categoria `#N/D` foram substituídos por `Sem Categoria` para evitar perda de dados.
- Colunas vazias (`Unnamed`) foram removidas por não possuírem informação útil.

---

# Reflexão Teórica — ETL e Qualidade de Dados

ETL significa:

- **Extract** → Extrair os dados;
- **Transform** → Limpar e transformar os dados;
- **Load** → Carregar os dados para análise ou uso em sistemas.

Neste projeto foi realizada principalmente a etapa de transformação dos dados, incluindo:

- remoção de duplicatas;
- tratamento de categorias inválidas;
- conversão de datas;
- remoção de colunas sem uso.

A qualidade dos dados é importante porque dados incorretos podem gerar análises erradas e prejudicar tomadas de decisão.

Por isso, antes de qualquer análise, é necessário verificar:

- valores nulos;
- dados duplicados;
- tipos incorretos;
- inconsistências na base.
