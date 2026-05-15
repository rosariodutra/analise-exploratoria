# 🔍 Análise Exploratória de Dados (EDA) — Dataset de Vendas

> EDA completa sobre dataset de vendas B2B utilizando Python e SQL (SQLite). Identificação de padrões, tendências sazonais, ranking de performance e geração automática de insights e recomendações.

---

## 🧩 Contexto de Negócio

Equipes comerciais e de dados frequentemente precisam responder perguntas como: *Qual produto gera mais receita? Qual região está abaixo do esperado? Qual vendedor merece atenção?* Sem uma análise estruturada, essas respostas ficam presas em planilhas desconexas.

Este projeto demonstra o fluxo completo de uma análise exploratória — desde a criação do banco de dados até a geração automática de insights acionáveis — usando apenas Python e SQL, sem dependências externas.

**Problema resolvido:** transformar 200 registros de vendas brutas em inteligência de negócio: rankings, tendências, anomalias e recomendações estratégicas geradas via queries SQL.

---

## 🎯 Análises disponíveis

| # | Análise                  | O que responde                                          |
|---|--------------------------|--------------------------------------------------------|
| 1 | Visão geral              | Volume, receita total, ticket médio, amplitude         |
| 2 | Receita por categoria    | Quais segmentos geram mais valor                       |
| 3 | Ranking de vendedores    | Performance individual com ticket médio                |
| 4 | Tendência mensal         | Sazonalidade e variação percentual Jan→Dez             |
| 5 | Receita por região       | Distribuição geográfica e concentração                 |
| 6 | Insights automáticos     | Padrões e recomendações gerados via SQL                |

---

## 🗂️ Dicionário de Dados

Dataset gerado automaticamente com 200 registros de vendas B2B (2024):

| Campo        | Tipo    | Descrição                                              |
|-------------|---------|--------------------------------------------------------|
| `id`         | int     | Identificador único do registro                        |
| `data`       | date    | Data da venda (YYYY-MM-DD)                             |
| `produto`    | string  | Nome do produto/serviço vendido                        |
| `categoria`  | string  | Segmento: Tecnologia, Serviços, Educação, Consultoria  |
| `regiao`     | string  | Região do Brasil: Sul, Sudeste, Norte, Nordeste, CO    |
| `vendedor`   | string  | Nome do vendedor responsável                           |
| `quantidade` | int     | Quantidade de unidades vendidas (1–5)                  |
| `valor_unit` | float   | Valor unitário com variação de ±15% sobre o base       |
| `total`      | float   | Receita total da venda (quantidade × valor_unit)       |

**Produtos e preços base:**

| Produto          | Categoria   | Preço base   |
|-----------------|-------------|--------------|
| Licença ERP     | Tecnologia  | R$ 2.300,00  |
| Automação RPA   | Tecnologia  | R$ 1.800,00  |
| Software BI     | Tecnologia  | R$ 1.200,00  |
| Dashboard Custom| Tecnologia  | R$ 950,00    |
| Análise de Dados| Consultoria | R$ 1.100,00  |
| Consultoria     | Serviços    | R$ 850,00    |
| Suporte Anual   | Serviços    | R$ 600,00    |
| Treinamento     | Educação    | R$ 400,00    |

---

## 💡 Exemplos de Insights Gerados

```
💡 INSIGHTS IDENTIFICADOS:

🏆 Produto estrela  : Licença ERP (R$ 28.450,00)
📅 Melhor mês       : Março (R$ 42.300,00)
💎 Categoria premium: Tecnologia (ticket médio R$ 1.850,00)
👤 Top vendedor     : Ana representa 23.4% da receita total

📌 RECOMENDAÇÕES:

→ Priorizar Licença ERP em campanhas de venda
→ Replicar estratégias do mês de Março
→ Investir em Tecnologia pelo alto ticket médio
→ Analisar práticas da vendedora Ana para treinamento
```

---

## 🔬 Técnicas utilizadas

- **SQL com SQLite:** `GROUP BY`, `ORDER BY`, `strftime`, `COUNT`, `SUM`, `AVG`, subqueries
- **Python:** geração de dataset com `random`, manipulação de datas com `datetime`, formatação de output
- **EDA:** análise de distribuição, tendência temporal, ranking e concentração de receita
- **Visualização no terminal:** gráficos de barras com caracteres Unicode

---

## 🚀 Como executar

```bash
# Clone o repositório
git clone https://github.com/rosariodutra/analise-exploratoria.git
cd analise-exploratoria

# Sem dependências externas — Python 3.6+ puro
python eda_vendas.py
```

> O banco `vendas.db` é criado automaticamente na primeira execução.

---

## 🛠️ Tecnologias

![Python](https://img.shields.io/badge/Python-7c3aed?style=flat-square&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-6d28d9?style=flat-square&logo=sqlite&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-5b21b6?style=flat-square&logo=sqlite&logoColor=white)

---

## 👩‍💻 Autora

Feito com 💜 por [Rosário Dutra](https://github.com/rosariodutra) · Analista de Dados & BI
