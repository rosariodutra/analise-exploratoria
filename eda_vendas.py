# =============================================================
#  🔍 ANÁLISE EXPLORATÓRIA DE DADOS (EDA)
#  Autor: Rosário Dutra
#  GitHub: github.com/rosariodutra
#  Descrição: EDA completa sobre dataset de vendas com Python
#             e SQL. Identificação de padrões, insights e KPIs.
# =============================================================

import os
import json
import sqlite3
import random
from datetime import datetime, timedelta
from collections import defaultdict

# ── Cores ─────────────────────────────────────────────────────
ROXO     = "\033[35m"
VERDE    = "\033[32m"
AMARELO  = "\033[33m"
VERMELHO = "\033[31m"
CIANO    = "\033[36m"
RESET    = "\033[0m"
NEGRITO  = "\033[1m"

DB = "vendas.db"

# ── Utilitários ───────────────────────────────────────────────

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def cabecalho():
    print(f"{ROXO}")
    print("╔══════════════════════════════════════════╗")
    print("║     🔍  ANÁLISE EXPLORATÓRIA (EDA)  🔍    ║")
    print("║        github.com/rosariodutra            ║")
    print("╚══════════════════════════════════════════╝")
    print(f"{RESET}")

def barra(valor, maximo, largura=30):
    filled = int((valor / maximo) * largura) if maximo > 0 else 0
    return f"{ROXO}{'█' * filled}{'░' * (largura - filled)}{RESET}"

def formatar(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

# ── Geração do dataset ────────────────────────────────────────

def gerar_dataset(conn):
    conn.execute("DROP TABLE IF EXISTS vendas")
    conn.execute("""
        CREATE TABLE vendas (
            id          INTEGER PRIMARY KEY,
            data        TEXT,
            produto     TEXT,
            categoria   TEXT,
            regiao      TEXT,
            vendedor    TEXT,
            quantidade  INTEGER,
            valor_unit  REAL,
            total       REAL
        )
    """)

    produtos = {
        "Software BI":      ("Tecnologia",  1200.0),
        "Consultoria":      ("Serviços",     850.0),
        "Licença ERP":      ("Tecnologia",  2300.0),
        "Treinamento":      ("Educação",     400.0),
        "Suporte Anual":    ("Serviços",     600.0),
        "Dashboard Custom": ("Tecnologia",   950.0),
        "Automação RPA":    ("Tecnologia",  1800.0),
        "Análise de Dados": ("Consultoria", 1100.0),
    }
    regioes   = ["Sul", "Sudeste", "Norte", "Nordeste", "Centro-Oeste"]
    vendedores= ["Ana", "Bruno", "Carol", "Diego", "Elena"]

    registros = []
    base_date = datetime(2024, 1, 1)
    for i in range(1, 201):
        prod, (cat, preco) = random.choice(list(produtos.items()))
        qtd   = random.randint(1, 5)
        var   = random.uniform(0.85, 1.15)
        vu    = round(preco * var, 2)
        total = round(vu * qtd, 2)
        data  = (base_date + timedelta(days=random.randint(0, 364))).strftime("%Y-%m-%d")
        registros.append((i, data, prod, cat, random.choice(regioes),
                          random.choice(vendedores), qtd, vu, total))

    conn.executemany(
        "INSERT INTO vendas VALUES (?,?,?,?,?,?,?,?,?)", registros)
    conn.commit()
    print(f"  {VERDE}✅ Dataset gerado: 200 registros de vendas (2024){RESET}\n")

def conectar():
    return sqlite3.connect(DB)

# ── 1. Visão geral ────────────────────────────────────────────

def visao_geral(conn):
    limpar(); cabecalho()
    print(f"  {NEGRITO}── 1. VISÃO GERAL DO DATASET ──{RESET}\n")

    cur = conn.execute("SELECT COUNT(*), SUM(total), AVG(total), MIN(total), MAX(total) FROM vendas")
    count, total, media, minv, maxv = cur.fetchone()

    cur2 = conn.execute("SELECT COUNT(DISTINCT produto), COUNT(DISTINCT regiao), COUNT(DISTINCT vendedor) FROM vendas")
    prods, regs, vends = cur2.fetchone()

    print(f"  {'─'*44}")
    print(f"  {'Registros':<28} {ROXO}{count:>14}{RESET}")
    print(f"  {'Receita Total':<28} {VERDE}{formatar(total):>14}{RESET}")
    print(f"  {'Ticket Médio':<28} {formatar(media):>14}")
    print(f"  {'Menor venda':<28} {formatar(minv):>14}")
    print(f"  {'Maior venda':<28} {formatar(maxv):>14}")
    print(f"  {'─'*44}")
    print(f"  {'Produtos únicos':<28} {prods:>14}")
    print(f"  {'Regiões':<28} {regs:>14}")
    print(f"  {'Vendedores':<28} {vends:>14}")
    print(f"  {'─'*44}\n")
    input("  [Enter para continuar]")

# ── 2. Análise por categoria ──────────────────────────────────

def por_categoria(conn):
    limpar(); cabecalho()
    print(f"  {NEGRITO}── 2. RECEITA POR CATEGORIA ──{RESET}\n")

    rows = conn.execute("""
        SELECT categoria, COUNT(*) as qtd, SUM(total) as receita
        FROM vendas GROUP BY categoria ORDER BY receita DESC
    """).fetchall()

    max_rec = rows[0][2] if rows else 1
    print(f"  {'Categoria':<18} {'Vendas':>7} {'Receita':>14}  Distribuição")
    print(f"  {'─'*65}")
    for cat, qtd, rec in rows:
        print(f"  {cat:<18} {qtd:>7} {formatar(rec):>14}  {barra(rec, max_rec, 20)}")
    print()
    input("  [Enter para continuar]")

# ── 3. Top vendedores ─────────────────────────────────────────

def top_vendedores(conn):
    limpar(); cabecalho()
    print(f"  {NEGRITO}── 3. RANKING DE VENDEDORES ──{RESET}\n")

    rows = conn.execute("""
        SELECT vendedor, COUNT(*) as qtd, SUM(total) as receita, AVG(total) as ticket
        FROM vendas GROUP BY vendedor ORDER BY receita DESC
    """).fetchall()

    medals = ["🥇", "🥈", "🥉", "  4.", "  5."]
    max_rec = rows[0][2] if rows else 1

    print(f"  {'#':<4} {'Vendedor':<12} {'Vendas':>7} {'Receita':>14} {'Ticket Médio':>14}")
    print(f"  {'─'*58}")
    for i, (vend, qtd, rec, ticket) in enumerate(rows):
        medal = medals[i] if i < len(medals) else f"  {i+1}."
        print(f"  {medal} {vend:<12} {qtd:>7} {formatar(rec):>14} {formatar(ticket):>14}")
    print()

    top = rows[0]
    print(f"  {AMARELO}🏆 Destaque: {top[0]} com {formatar(top[2])} em receita!{RESET}\n")
    input("  [Enter para continuar]")

# ── 4. Tendência mensal ───────────────────────────────────────

def tendencia_mensal(conn):
    limpar(); cabecalho()
    print(f"  {NEGRITO}── 4. TENDÊNCIA MENSAL (2024) ──{RESET}\n")

    rows = conn.execute("""
        SELECT strftime('%m', data) as mes, SUM(total) as receita, COUNT(*) as qtd
        FROM vendas GROUP BY mes ORDER BY mes
    """).fetchall()

    meses = {"01":"Jan","02":"Fev","03":"Mar","04":"Abr","05":"Mai","06":"Jun",
             "07":"Jul","08":"Ago","09":"Set","10":"Out","11":"Nov","12":"Dez"}

    max_rec = max(r[1] for r in rows) if rows else 1
    print(f"  {'Mês':<6} {'Receita':>14} {'Vendas':>7}  Gráfico")
    print(f"  {'─'*60}")
    for mes, rec, qtd in rows:
        print(f"  {meses.get(mes, mes):<6} {formatar(rec):>14} {qtd:>7}  {barra(rec, max_rec, 22)}")

    # Crescimento
    if len(rows) >= 2:
        primeira = rows[0][1]
        ultima   = rows[-1][1]
        cresc    = ((ultima - primeira) / primeira * 100) if primeira > 0 else 0
        cor      = VERDE if cresc >= 0 else VERMELHO
        sinal    = "+" if cresc >= 0 else ""
        print(f"\n  {cor}📈 Variação Jan→Dez: {sinal}{cresc:.1f}%{RESET}\n")
    input("  [Enter para continuar]")

# ── 5. Análise por região ─────────────────────────────────────

def por_regiao(conn):
    limpar(); cabecalho()
    print(f"  {NEGRITO}── 5. RECEITA POR REGIÃO ──{RESET}\n")

    rows = conn.execute("""
        SELECT regiao, COUNT(*) as qtd, SUM(total) as receita
        FROM vendas GROUP BY regiao ORDER BY receita DESC
    """).fetchall()

    max_rec = rows[0][2] if rows else 1
    total   = sum(r[2] for r in rows)

    print(f"  {'Região':<16} {'Vendas':>7} {'Receita':>14} {'%':>6}  Mapa")
    print(f"  {'─'*62}")
    for reg, qtd, rec in rows:
        pct = rec / total * 100
        print(f"  {reg:<16} {qtd:>7} {formatar(rec):>14} {pct:>5.1f}%  {barra(rec, max_rec, 15)}")
    print()

    top = rows[0]
    print(f"  {VERDE}📍 Região líder: {top[0]} ({formatar(top[2])}){RESET}\n")
    input("  [Enter para continuar]")

# ── 6. Insights automáticos ───────────────────────────────────

def insights(conn):
    limpar(); cabecalho()
    print(f"  {NEGRITO}── 6. INSIGHTS AUTOMÁTICOS ──{RESET}\n")

    # Produto mais vendido
    prod = conn.execute(
        "SELECT produto, SUM(total) FROM vendas GROUP BY produto ORDER BY SUM(total) DESC LIMIT 1"
    ).fetchone()

    # Melhor mês
    mes = conn.execute(
        "SELECT strftime('%m', data), SUM(total) FROM vendas GROUP BY strftime('%m', data) ORDER BY SUM(total) DESC LIMIT 1"
    ).fetchone()

    meses = {"01":"Janeiro","02":"Fevereiro","03":"Março","04":"Abril","05":"Maio",
             "06":"Junho","07":"Julho","08":"Agosto","09":"Setembro","10":"Outubro",
             "11":"Novembro","12":"Dezembro"}

    # Ticket médio por categoria
    cats = conn.execute(
        "SELECT categoria, AVG(total) FROM vendas GROUP BY categoria ORDER BY AVG(total) DESC LIMIT 1"
    ).fetchone()

    # % receita top vendedor
    top_vend = conn.execute(
        "SELECT vendedor, SUM(total) FROM vendas GROUP BY vendedor ORDER BY SUM(total) DESC LIMIT 1"
    ).fetchone()
    total_geral = conn.execute("SELECT SUM(total) FROM vendas").fetchone()[0]
    pct_top = top_vend[1] / total_geral * 100

    print(f"  {CIANO}💡 INSIGHTS IDENTIFICADOS:{RESET}\n")
    print(f"  🏆 Produto estrela  : {prod[0]} ({formatar(prod[1])})")
    print(f"  📅 Melhor mês       : {meses.get(mes[0], mes[0])} ({formatar(mes[1])})")
    print(f"  💎 Categoria premium: {cats[0]} (ticket médio {formatar(cats[1])})")
    print(f"  👤 Top vendedor     : {top_vend[0]} representa {pct_top:.1f}% da receita total")
    print(f"\n  {AMARELO}📌 RECOMENDAÇÕES:{RESET}\n")
    print(f"  → Priorizar {prod[0]} em campanhas de venda")
    print(f"  → Replicar estratégias do mês de {meses.get(mes[0], mes[0])}")
    print(f"  → Investir em {cats[0]} pelo alto ticket médio")
    print(f"  → Analisar práticas do vendedor {top_vend[0]} para treinamento\n")
    input("  [Enter para continuar]")

# ── Menu principal ────────────────────────────────────────────

def main():
    limpar(); cabecalho()
    print("  Inicializando banco de dados SQLite...\n")
    conn = conectar()

    tabela_existe = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='vendas'"
    ).fetchone()

    if not tabela_existe:
        gerar_dataset(conn)
        input("  [Enter para continuar]")

    while True:
        limpar(); cabecalho()
        print("  1. Visão geral do dataset")
        print("  2. Receita por categoria")
        print("  3. Ranking de vendedores")
        print("  4. Tendência mensal")
        print("  5. Receita por região")
        print("  6. Insights automáticos")
        print("  7. Regenerar dataset")
        print("  0. Sair\n")

        op = input("  Opção: ").strip()

        if op == "1":   visao_geral(conn)
        elif op == "2": por_categoria(conn)
        elif op == "3": top_vendedores(conn)
        elif op == "4": tendencia_mensal(conn)
        elif op == "5": por_regiao(conn)
        elif op == "6": insights(conn)
        elif op == "7":
            gerar_dataset(conn)
            input("  [Enter para continuar]")
        elif op == "0":
            conn.close()
            limpar(); cabecalho()
            print("  Até logo! 💜\n"); break
        else:
            print("  ⚠️  Opção inválida!"); input("  [Enter]")

if __name__ == "__main__":
    main()
