"""
Autoconferência — Loja de Papelaria (Algoritmos II · Univille)

Uso (na mesma pasta do seu solucao.py):
    python testes.py                 # confere o arquivo solucao.py
    python testes.py outro_nome.py   # confere outro arquivo

O que este programa faz:
  1) roda o seu código com os DADOS OFICIAIS e compara cada variável pedida;
  2) roda de novo com DADOS ALTERNATIVOS (outro tamanho, outros valores) para
     verificar que a sua lógica não depende de números fixos.

Ele só LÊ o seu arquivo; não altera nada. Se uma etapa dá erro, as etapas
anteriores continuam sendo avaliadas.
"""
import os
import sys
import threading
import traceback

INI = "# ===== DADOS"
FIM = "# ===== FIM DOS DADOS"
TEMPO_MAX = 5  # segundos por execução

# ---------------------------------------------------------------- dados alternativos
DADOS_ALTERNATIVOS = '''
codigos = ["X1", "X2", "X3", "X4", "X5"]
meses = ["Out", "Nov", "Dez", "Jan", "Fev"]
vendas = [
    [50, 50, 40, 30, 20],
    [10, 12, 9, 15, 15],
    [314, 280, 310, 305, 290],
    [5, 5, 5, 5, 5],
    [70, 90, 85, 60, 100],
]
catalogo = {
    "X1": {"nome": "Borracha",   "preco": 12.00,   "estoque": 90},
    "X2": {"nome": "Tablet",     "preco": 250.00,  "estoque": 20},
    "X3": {"nome": "Clipe",      "preco": 3.10,    "estoque": 1000},
    "X4": {"nome": "Notebook",   "preco": 1000.00, "estoque": 10},
    "X5": {"nome": "Fone",       "preco": 45.50,   "estoque": 100},
}
'''

# ---------------------------------------------------------------- referência independente
def calcular_esperado(codigos, meses, vendas, catalogo):
    """Implementação de referência (estilo diferente do gabarito: zip, sum, max)."""
    e = {}
    e["total_por_produto"] = [sum(linha) for linha in vendas]
    e["total_por_mes"] = [sum(col) for col in zip(*vendas)]
    e["mes_mais_vendido"] = meses[e["total_por_mes"].index(max(e["total_por_mes"]))]
    precos = [catalogo[c]["preco"] for c in codigos]
    e["faturamento"] = {c: t * p for c, t, p in zip(codigos, e["total_por_produto"], precos)}
    e["faturamento_total"] = sum(e["faturamento"].values())
    fat_mes = [sum(v * p for v, p in zip(col, precos)) for col in zip(*vendas)]
    e["mes_maior_faturamento"] = meses[fat_mes.index(max(fat_mes))]
    e["reposicao"] = {}
    for c, linha in zip(codigos, vendas):
        falta = sum(linha[-3:]) - catalogo[c]["estoque"]
        if falta > 0:
            e["reposicao"][c] = falta
    ordem = sorted(codigos, key=lambda c: -e["faturamento"][c])
    e["top3"] = ordem[:3]
    e["maior_queda"] = {}
    for c, linha in zip(codigos, vendas):
        maior = atual = 0
        for a, b in zip(linha, linha[1:]):
            atual = atual + 1 if b < a else 0
            maior = max(maior, atual)
        e["maior_queda"][c] = maior
    e["em_alerta"] = [catalogo[c]["nome"] for c in codigos if e["maior_queda"][c] >= 3]
    return e


ETAPAS = [
    ("Etapa 1 - vetores a partir da matriz", ["total_por_produto", "total_por_mes", "mes_mais_vendido"]),
    ("Etapa 2 - faturamento", ["faturamento", "faturamento_total", "mes_maior_faturamento"]),
    ("Etapa 3 - reposicao de estoque", ["reposicao"]),
    ("Etapa 4 - top 3 por faturamento", ["top3"]),
    ("Etapa 5 (desafio) - sequencias de queda", ["maior_queda", "em_alerta"]),
]


# ---------------------------------------------------------------- comparação
def numero(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def igual(a, b):
    if numero(a) and numero(b):
        return abs(a - b) < 0.01
    if isinstance(b, dict):
        return isinstance(a, dict) and set(a) == set(b) and all(igual(a[k], b[k]) for k in b)
    if isinstance(b, (list, tuple)):
        return isinstance(a, (list, tuple)) and len(a) == len(b) and all(igual(x, y) for x, y in zip(a, b))
    return a == b


def resumo(x, limite=140):
    if isinstance(x, float):
        x = round(x, 2)
    if isinstance(x, dict):
        x = {k: (round(v, 2) if isinstance(v, float) else v) for k, v in x.items()}
    if isinstance(x, list):
        x = [round(v, 2) if isinstance(v, float) else v for v in x]
    s = repr(x)
    return s if len(s) <= limite else s[: limite - 3] + "..."


def dica(nome, obtido, esperado):
    if type(obtido).__name__ != type(esperado).__name__ and not (numero(obtido) and numero(esperado)):
        return f"tipo esperado: {type(esperado).__name__}; o seu e {type(obtido).__name__}"
    if isinstance(esperado, list) and isinstance(obtido, list) and len(obtido) != len(esperado):
        return f"esperados {len(esperado)} elementos; o seu tem {len(obtido)}"
    if isinstance(esperado, dict) and isinstance(obtido, dict):
        if set(obtido) != set(esperado):
            sobra = sorted(set(obtido) - set(esperado))
            falta = sorted(set(esperado) - set(obtido))
            partes = []
            if falta:
                partes.append(f"faltam as chaves {falta}")
            if sobra:
                partes.append(f"sobram as chaves {sobra}")
            return "; ".join(partes)
    return ""


# ---------------------------------------------------------------- execução isolada
def separar(src):
    linhas = src.splitlines(keepends=True)
    ini = next((k for k, l in enumerate(linhas) if l.startswith(INI)), None)
    fim = next((k for k, l in enumerate(linhas) if l.startswith(FIM)), None)
    if ini is None or fim is None or fim < ini:
        return None
    return "".join(linhas[: ini + 1]), "".join(linhas[fim:])


def executar(codigo, nome_arquivo):
    """Roda 'codigo' num espaço de nomes novo. Devolve (namespace, erro|None)."""

    def sem_input(*a, **k):
        raise RuntimeError("nao use input() neste exercicio")

    # print/input sao substituidos so dentro do codigo do aluno (nada global e alterado)
    ns = {"__name__": "__aluno__", "print": lambda *a, **k: None, "input": sem_input}
    estado = {"erro": None}

    def alvo():
        try:
            exec(compile(codigo, nome_arquivo, "exec"), ns)
        except BaseException as exc:  # noqa: BLE001
            linha = None
            for fr in traceback.extract_tb(exc.__traceback__):
                if fr.filename == nome_arquivo:
                    linha = fr.lineno
            estado["erro"] = (type(exc).__name__, str(exc), linha)

    t = threading.Thread(target=alvo, daemon=True)
    t.start()
    t.join(TEMPO_MAX)
    if t.is_alive():
        return ns, ("Timeout", f"mais de {TEMPO_MAX}s de execucao (laco infinito?)", None)
    return ns, estado["erro"]


def avaliar(ns, esperado):
    """Devolve {variavel: (ok, obtido, esperado, dica)}."""
    res = {}
    for _, nomes in ETAPAS:
        for n in nomes:
            if n not in ns:
                res[n] = (False, None, esperado[n], "variavel nao definida")
            else:
                ok = igual(ns[n], esperado[n])
                res[n] = (ok, ns[n], esperado[n], "" if ok else dica(n, ns[n], esperado[n]))
    return res


def dados_do_codigo(codigo):
    ns, erro = executar(codigo, "<dados>")
    return ns["codigos"], ns["meses"], ns["vendas"], ns["catalogo"]


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    caminho = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, "solucao.py")
    if not os.path.exists(caminho):
        caminho = os.path.join(base, caminho)
    if not os.path.exists(caminho):
        print(f"Arquivo nao encontrado: {caminho}")
        return 2
    with open(caminho, encoding="utf-8") as f:
        fonte = f.read()
    nome = os.path.basename(caminho)

    partes = separar(fonte)
    # --- dados oficiais
    ns_a, erro_a = executar(fonte, nome)
    if partes is None:
        print("AVISO: nao encontrei as linhas '# ===== DADOS' e '# ===== FIM DOS DADOS'.")
        print("       O teste com dados alternativos foi pulado.\n")
        esp_a = None
    try:
        esp_a = calcular_esperado(ns_a["codigos"], ns_a["meses"], ns_a["vendas"], ns_a["catalogo"])
    except Exception:  # dados oficiais foram danificados
        print("Os DADOS foram alterados/apagados. Restaure o bloco de dados original.")
        return 2
    res_a = avaliar(ns_a, esp_a)

    # --- dados alternativos
    res_b = erro_b = None
    if partes is not None:
        ini, fim = partes
        codigo_b = ini + DADOS_ALTERNATIVOS + "\n" + fim
        ns_b, erro_b = executar(codigo_b, nome)
        esp_b = calcular_esperado(*dados_do_codigo(DADOS_ALTERNATIVOS))
        res_b = avaliar(ns_b, esp_b)

    # --- relatório
    print("=" * 66)
    print(f" Conferindo {nome}")
    print("=" * 66)
    if erro_a:
        tipo, msg, linha = erro_a
        onde = f" (linha {linha})" if linha else ""
        print(f"\nERRO ao executar{onde}: {tipo}: {msg}")
        print("As etapas acima do erro ainda foram avaliadas.\n")

    total_ok = total = 0
    for titulo, nomes in ETAPAS:
        print(f"\n{titulo}")
        etapa_ok = True
        for n in nomes:
            ok, obt, esp, d = res_a[n]
            total += 1
            total_ok += ok
            etapa_ok &= ok
            print(f"  [{'OK' if ok else ' X'}] {n}")
            if not ok:
                if d:
                    print(f"        {d}")
                if n in ns_a:
                    print(f"        seu valor : {resumo(obt)}")
                print(f"        esperado  : {resumo(esp)}")
        if res_b is not None:
            ok_b = all(res_b[n][0] for n in nomes)
            if etapa_ok and not ok_b:
                print("  [ X] com DADOS ALTERNATIVOS: resultado diferente do esperado")
                for n in nomes:
                    ok, obt, esp, d = res_b[n]
                    if not ok:
                        print(f"        {n}: seu {resumo(obt, 90)} | esperado {resumo(esp, 90)}")
                print("        Dica: o codigo pode depender de numeros fixos (use len())")
                print("        ou tratar mal empates / valores iguais em meses seguidos.")
            elif etapa_ok and ok_b:
                print("  [OK] tambem correto com dados alternativos")
    if erro_b and not erro_a:
        tipo, msg, linha = erro_b
        onde = f" (linha {linha})" if linha else ""
        print(f"\nCom dados alternativos o seu codigo parou{onde}: {tipo}: {msg}")

    print("\n" + "-" * 66)
    print(f" Variaveis corretas com os dados oficiais: {total_ok} de {total}")
    print("-" * 66)
    return 0 if total_ok == total else 1


if __name__ == "__main__":
    codigo_saida = main()
    sys.stdout.flush()
    os._exit(codigo_saida)  # encerra mesmo que algum laco infinito tenha ficado em segundo plano
