"""
Autoconferencia - Sistema de biblioteca (Algoritmos II - Univille)

Uso (na mesma pasta do seu solucao.py):
    python testes.py                 # confere o arquivo solucao.py
    python testes.py outro_nome.py   # confere outro arquivo

O que este programa faz:
  1) carrega o seu arquivo e, para CADA funcao, chama a funcao com varios dados de
     teste (alguns iguais aos exemplos do enunciado, outros diferentes), comparando
     o que ela DEVOLVE (return) e o que ela ALTEROU nos dicionarios e listas recebidos;
  2) mostra, para cada funcao que falhou, qual caso falhou, os dados de entrada, o
     valor que a sua funcao devolveu, o valor esperado e uma dica;
  3) confere se as duas respostas (R1 e R2) do final do arquivo foram preenchidas.

Ele so LE o seu arquivo; nao altera nada. Cada funcao e testada separadamente, entao
um erro (ou um laco infinito) em uma funcao nao atrapalha a avaliacao das outras.
"""
import copy
import json
import os
import re
import subprocess
import sys
import traceback

TEMPO_MAX = 6  # segundos por funcao
MARCA = "@@RESULTADO@@"
EXPL = "# ===== EXPLICA"

# (numero, nome, parametros, grupo)
FUNCOES = [
    (1, "criar_livro", ["titulo", "autor", "ano", "exemplares"], 1),
    (2, "cadastrar_livro", ["acervo", "codigo", "livro"], 1),
    (3, "buscar_livro", ["acervo", "codigo"], 1),
    (4, "atualizar_livro", ["acervo", "codigo", "campo", "valor"], 1),
    (5, "listar_titulos", ["acervo"], 1),
    (6, "livros_do_aluno", ["emprestimos", "aluno"], 2),
    (7, "livro_esta_emprestado", ["emprestimos", "codigo"], 2),
    (8, "emprestar_livro", ["acervo", "emprestimos", "aluno", "codigo"], 2),
    (9, "devolver_livro", ["acervo", "emprestimos", "aluno", "codigo"], 2),
    (10, "remover_livro", ["acervo", "emprestimos", "codigo"], 2),
    (11, "relatorio_por_autor", ["acervo"], 3),
    (12, "relatorio_indisponiveis", ["acervo"], 3),
    (13, "relatorio_emprestimos_mes", ["matriz", "categorias", "meses"], 3),
    (14, "processar_movimentos", ["acervo", "emprestimos", "movimentos"], 4),
]
GRUPOS = {1: "Parte 1 - cadastro de livros", 2: "Parte 2 - emprestimos e remocao",
          3: "Parte 3 - relatorios", 4: "Parte 4 (desafio) - juntando tudo"}
PARAMS = {nome: ps for _, nome, ps, _ in FUNCOES}


# ---------------------------------------------------------------- dados de teste
def acervo_a():  # o mesmo acervo_exemplo do solucao.py
    return {
        "L001": {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899, "exemplares": 2},
        "L002": {"titulo": "Capitães da Areia", "autor": "Jorge Amado", "ano": 1937, "exemplares": 1},
        "L003": {"titulo": "Vidas Secas", "autor": "Graciliano Ramos", "ano": 1938, "exemplares": 0},
        "L004": {"titulo": "Quincas Borba", "autor": "Machado de Assis", "ano": 1891, "exemplares": 3},
    }


def emp_a():
    return {"Ana": ["L001", "L004"], "Bruno": ["L002"]}


def acervo_x():  # outro acervo, com outros codigos, autores e quantidades
    return {
        "M1": {"titulo": "Alfa", "autor": "Zeca Prado", "ano": 2001, "exemplares": 1},
        "M2": {"titulo": "Beta", "autor": "Ana Souza", "ano": 1999, "exemplares": 0},
        "M3": {"titulo": "Gama", "autor": "Zeca Prado", "ano": 2010, "exemplares": 2},
        "M4": {"titulo": "Delta", "autor": "Bia Lima", "ano": 1980, "exemplares": 0},
        "M5": {"titulo": "Epsilon", "autor": "Zeca Prado", "ano": 1975, "exemplares": 4},
    }


def acervo_antigo():  # acervo dos 21 movimentos do caso extra grande
    def liv(t, ex):
        return {"titulo": t, "autor": "Autor " + t[0], "ano": 2000, "exemplares": ex}
    return {"L001": liv("Dom Casmurro", 2), "L002": liv("Capitães da Areia", 1), "L003": liv("Vidas Secas", 1),
            "L004": liv("O Cortiço", 0), "L005": liv("São Bernardo", 3), "L006": liv("Esaú e Jacó", 1)}


MOVS_GRANDE = [
    ("emprestar", "Ana", "L001"), ("emprestar", "Bruno", "L001"), ("emprestar", "Carla", "L001"),
    ("emprestar", "Ana", "L002"), ("emprestar", "Ana", "L003"), ("emprestar", "Ana", "L005"),
    ("emprestar", "Ana", "L004"), ("devolver", "Ana", "L005"), ("emprestar", "Diego", "L009"),
    ("emprestar", "Diego", "L004"), ("devolver", "Bruno", "L001"), ("devolver", "Bruno", "L001"),
    ("emprestar", "Carla", "L001"), ("remover", "L002"), ("remover", "L006"), ("remover", "L010"),
    ("devolver", "Ana", "L002"), ("remover", "L002"), ("emprestar", "Ana", "L002"),
    ("emprestar", "Ana", "L005"), ("devolver", "Diego", "L004"),
]


# ---------------------------------------------------------------- referencia independente
def r_criar_livro(titulo, autor, ano, exemplares):
    return dict(titulo=titulo, autor=autor, ano=ano, exemplares=exemplares)


def r_cadastrar_livro(acervo, codigo, livro):
    if codigo in acervo.keys():
        return False
    acervo.update({codigo: livro})
    return True


def r_buscar_livro(acervo, codigo):
    return acervo.get(codigo)


def r_atualizar_livro(acervo, codigo, campo, valor):
    if codigo not in acervo or campo not in ("titulo", "autor", "ano", "exemplares"):
        return False
    acervo[codigo][campo] = valor
    return True


def r_listar_titulos(acervo):
    return [v["titulo"] for v in acervo.values()]


def r_livros_do_aluno(emprestimos, aluno):
    return emprestimos[aluno] if aluno in emprestimos else []


def r_livro_esta_emprestado(emprestimos, codigo):
    return any(codigo in lista for lista in emprestimos.values())


def r_emprestar_livro(acervo, emprestimos, aluno, codigo):
    if codigo not in acervo:
        return (False, "inexistente")
    if acervo[codigo]["exemplares"] <= 0:
        return (False, "sem exemplar")
    if len(emprestimos.get(aluno, [])) >= 3:
        return (False, "limite")
    acervo[codigo]["exemplares"] -= 1
    emprestimos.setdefault(aluno, []).append(codigo)
    return (True, "ok")


def r_devolver_livro(acervo, emprestimos, aluno, codigo):
    if codigo not in emprestimos.get(aluno, []):
        return (False, "nao emprestado")
    emprestimos[aluno].remove(codigo)
    acervo[codigo]["exemplares"] += 1
    if not emprestimos[aluno]:
        del emprestimos[aluno]
    return (True, "ok")


def r_remover_livro(acervo, emprestimos, codigo):
    if codigo not in acervo:
        return (False, "inexistente")
    if r_livro_esta_emprestado(emprestimos, codigo):
        return (False, "emprestado")
    del acervo[codigo]
    return (True, "ok")


def r_relatorio_por_autor(acervo):
    r = {}
    for v in acervo.values():
        r[v["autor"]] = r.get(v["autor"], 0) + 1
    return r


def r_relatorio_indisponiveis(acervo):
    return [v["titulo"] for v in acervo.values() if v["exemplares"] == 0]


def r_relatorio_emprestimos_mes(matriz, categorias, meses):
    tot = {c: sum(matriz[i]) for i, c in enumerate(categorias)}
    somas = [sum(matriz[i][j] for i in range(len(categorias))) for j in range(len(meses))]
    return (tot, meses[somas.index(max(somas))])


def r_processar_movimentos(acervo, emprestimos, movimentos):
    rec = []
    for n, m in enumerate(movimentos, 1):
        if m[0] == "emprestar":
            r = r_emprestar_livro(acervo, emprestimos, m[1], m[2])
        elif m[0] == "devolver":
            r = r_devolver_livro(acervo, emprestimos, m[1], m[2])
        else:
            r = r_remover_livro(acervo, emprestimos, m[1])
        if not r[0]:
            rec.append((n, r[1]))
    return rec


REF = {nome: globals()["r_" + nome] for _, nome, _, _ in FUNCOES}


# ---------------------------------------------------------------- casos de teste
# cada caso: (descricao, extra?, funcao que monta os argumentos novos a cada uso)
# extra=False: caso igual a um exemplo do enunciado; extra=True: caso adicional
def novo_livro():
    return {"titulo": "O Cortiço", "autor": "Aluísio Azevedo", "ano": 1890, "exemplares": 2}


def com3():  # aluno com 3 livros (no limite)
    return {"Zeca": ["M1", "M3", "M4"], "Lia": ["M3"]}


CASOS = {
    "criar_livro": [
        ("livro do exemplo do enunciado", False, lambda: ("Dom Casmurro", "Machado de Assis", 1899, 2)),
        ("outros valores, com exemplares = 0", True, lambda: ("Zero", "Fulana de Tal", 2024, 0)),
        ("outros valores de novo (nao pode ser texto fixo)", True, lambda: ("Beta", "Ana Souza", 1999, 7)),
    ],
    "cadastrar_livro": [
        ("codigo novo (L005): deve cadastrar", False, lambda: (acervo_a(), "L005", novo_livro())),
        ("codigo que JA existe (L001): nao pode sobrescrever", False, lambda: (acervo_a(), "L001", novo_livro())),
        ("acervo vazio", True, lambda: ({}, "Z1", novo_livro())),
        ("outro acervo, codigo repetido (M3)", True, lambda: (acervo_x(), "M3", novo_livro())),
        ("outro acervo, codigo novo (M9)", True, lambda: (acervo_x(), "M9", novo_livro())),
    ],
    "buscar_livro": [
        ("codigo que existe (L003)", False, lambda: (acervo_a(), "L003")),
        ("codigo que NAO existe (L999): deve devolver None", False, lambda: (acervo_a(), "L999")),
        ("acervo vazio", True, lambda: ({}, "L001")),
        ("outro acervo, ultimo codigo (M5)", True, lambda: (acervo_x(), "M5")),
        ("outro acervo, codigo que nao existe", True, lambda: (acervo_x(), "L001")),
    ],
    "atualizar_livro": [
        ("trocar exemplares de L003 para 5", False, lambda: (acervo_a(), "L003", "exemplares", 5)),
        ("codigo que nao existe (L999)", False, lambda: (acervo_a(), "L999", "ano", 2000)),
        ("campo que nao existe (editora): nao pode criar campo novo", False, lambda: (acervo_a(), "L001", "editora", "X")),
        ("trocar o titulo em outro acervo", True, lambda: (acervo_x(), "M2", "titulo", "Beta 2a edicao")),
        ("trocar o autor (campo de texto)", True, lambda: (acervo_x(), "M4", "autor", "Outra Pessoa")),
        ("exemplares para 0", True, lambda: (acervo_x(), "M1", "exemplares", 0)),
        ("campo invalido em outro acervo", True, lambda: (acervo_x(), "M1", "isbn", "123")),
    ],
    "listar_titulos": [
        ("acervo do exemplo", False, lambda: (acervo_a(),)),
        ("acervo vazio: lista vazia", False, lambda: ({},)),
        ("outro acervo (5 livros)", True, lambda: (acervo_x(),)),
        ("acervo com um unico livro", True, lambda: ({"Q1": {"titulo": "Unico", "autor": "A", "ano": 1, "exemplares": 1}},)),
    ],
    "livros_do_aluno": [
        ("aluno que existe (Ana)", False, lambda: (emp_a(), "Ana")),
        ("aluno que nunca pegou livro (Carla): lista vazia e sem criar a chave", False, lambda: (emp_a(), "Carla")),
        ("dicionario vazio", True, lambda: ({}, "Ana")),
        ("aluno com 3 livros", True, lambda: (com3(), "Zeca")),
        ("segundo aluno do dicionario", True, lambda: (com3(), "Lia")),
    ],
    "livro_esta_emprestado": [
        ("L002 esta com o Bruno", False, lambda: (emp_a(), "L002")),
        ("L003 nao esta com ninguem", False, lambda: (emp_a(), "L003")),
        ("dicionario vazio", True, lambda: ({}, "L001")),
        ("livro so com o ultimo aluno da lista (nao pode parar no primeiro)", True,
         lambda: ({"A": ["X1"], "B": ["X2"], "C": ["X3", "X4"]}, "X4")),
        ("livro com o segundo aluno", True, lambda: ({"A": ["X1"], "B": ["X2"], "C": ["X3"]}, "X2")),
        ("livro que ninguem tem, com varios alunos", True, lambda: ({"A": ["X1"], "B": ["X2"]}, "X9")),
    ],
    "emprestar_livro": [
        ("aluno novo (Carla) pega L004: aceito e cria a lista dela", False, lambda: (acervo_a(), emp_a(), "Carla", "L004")),
        ("L003 tem 0 exemplares: 'sem exemplar'", False, lambda: (acervo_a(), emp_a(), "Ana", "L003")),
        ("codigo L999 nao existe: 'inexistente'", False, lambda: (acervo_a(), emp_a(), "Ana", "L999")),
        ("Ana ja tem 3 livros e pede L001: 'limite'", False,
         lambda: (acervo_a(), {"Ana": ["L001", "L004", "L002"], "Bruno": ["L002"]}, "Ana", "L001")),
        ("aluno que ja tem livros (Ana, 2) pega mais um: aceito (limite e 3)", True, lambda: (acervo_a(), emp_a(), "Ana", "L002")),
        ("no limite e livro SEM exemplar: vale 'sem exemplar' (ordem das regras)", True, lambda: (acervo_x(), com3(), "Zeca", "M2")),
        ("no limite e codigo inexistente: vale 'inexistente' (ordem das regras)", True, lambda: (acervo_x(), com3(), "Zeca", "Z9")),
        ("aluno com exatamente 3 livros e livro disponivel: 'limite'", True, lambda: (acervo_x(), com3(), "Zeca", "M5")),
        ("ultimo exemplar: aceito e exemplares vira 0", True, lambda: (acervo_x(), {}, "Teo", "M1")),
        ("outro aluno, mesmo livro de quem esta no limite", True, lambda: (acervo_x(), com3(), "Lia", "M3")),
        ("emprestimos vazio", True, lambda: (acervo_x(), {}, "Teo", "M5")),
    ],
    "devolver_livro": [
        ("Ana devolve L001 (ainda fica com L004)", False, lambda: (acervo_a(), emp_a(), "Ana", "L001")),
        ("Bruno devolve L002, o unico livro dele: ele sai de emprestimos", False, lambda: (acervo_a(), emp_a(), "Bruno", "L002")),
        ("Bruno nao esta com L001: 'nao emprestado'", False, lambda: (acervo_a(), emp_a(), "Bruno", "L001")),
        ("Carla nunca pegou livro: 'nao emprestado' (sem erro e sem criar Carla)", False, lambda: (acervo_a(), emp_a(), "Carla", "L001")),
        ("aluno com 3 livros devolve o do meio", True, lambda: (acervo_x(), com3(), "Zeca", "M3")),
        ("dois alunos com o mesmo livro: so o aluno certo muda", True, lambda: (acervo_x(), com3(), "Lia", "M3")),
        ("emprestimos vazio", True, lambda: (acervo_x(), {}, "Zeca", "M1")),
        ("livro existe no acervo mas o aluno nao esta com ele", True, lambda: (acervo_x(), com3(), "Lia", "M1")),
    ],
    "remover_livro": [
        ("L003 existe e ninguem esta com ele: removido", False, lambda: (acervo_a(), emp_a(), "L003")),
        ("L001 esta com a Ana: 'emprestado'", False, lambda: (acervo_a(), emp_a(), "L001")),
        ("L999 nao existe: 'inexistente'", False, lambda: (acervo_a(), emp_a(), "L999")),
        ("livro emprestado so ao ultimo aluno do dicionario", True, lambda: (acervo_x(), {"A": ["M1"], "B": ["M2"], "C": ["M3"]}, "M3")),
        ("emprestimos vazio: remove", True, lambda: (acervo_x(), {}, "M5")),
        ("emprestimos vazio, codigo inexistente", True, lambda: (acervo_x(), {}, "Z9")),
        ("o outro livro do mesmo aluno nao impede a remocao", True, lambda: (acervo_x(), {"A": ["M1", "M3"]}, "M4")),
    ],
    "relatorio_por_autor": [
        ("acervo do exemplo", False, lambda: (acervo_a(),)),
        ("acervo vazio: dicionario vazio", True, lambda: ({},)),
        ("outro acervo (um autor com 3 titulos)", True, lambda: (acervo_x(),)),
        ("todos do mesmo autor", True, lambda: ({"1": {"titulo": "a", "autor": "Z", "ano": 1, "exemplares": 1},
                                                  "2": {"titulo": "b", "autor": "Z", "ano": 2, "exemplares": 0}},)),
    ],
    "relatorio_indisponiveis": [
        ("acervo do exemplo (so L003 esta sem exemplar)", False, lambda: (acervo_a(),)),
        ("outro acervo (dois indisponiveis)", True, lambda: (acervo_x(),)),
        ("ninguem indisponivel: lista vazia", True,
         lambda: ({"1": {"titulo": "a", "autor": "Z", "ano": 1, "exemplares": 1}},)),
        ("todos indisponiveis", True,
         lambda: ({"1": {"titulo": "a", "autor": "Z", "ano": 1, "exemplares": 0},
                   "2": {"titulo": "b", "autor": "Z", "ano": 2, "exemplares": 0}},)),
        ("acervo vazio", True, lambda: ({},)),
    ],
    "relatorio_emprestimos_mes": [
        ("matriz 2x3 do exemplo", False, lambda: ([[10, 12, 9], [4, 15, 8]], ["Romance", "Didático"], ["Jan", "Fev", "Mar"])),
        ("matriz 3x4 (mais linhas e colunas)", True,
         lambda: ([[5, 9, 7, 6], [20, 15, 25, 10], [12, 30, 8, 22]], ["Poesia", "Ciência", "HQ"], ["Mar", "Abr", "Mai", "Jun"])),
        ("empate entre meses: vale o primeiro", True,
         lambda: ([[5, 5, 1], [5, 5, 1]], ["A", "B"], ["m1", "m2", "m3"])),
        ("maior mes e o ultimo", True, lambda: ([[1, 2, 3, 40]], ["Unica"], ["a", "b", "c", "d"])),
        ("matriz 4x2 (mais linhas que colunas)", True,
         lambda: ([[1, 2], [3, 4], [5, 6], [7, 8]], ["a", "b", "c", "d"], ["x", "y"])),
    ],
    "processar_movimentos": [
        ("6 movimentos do exemplo do enunciado", False, lambda: (acervo_a(), emp_a(), [
            ("emprestar", "Carla", "L004"), ("emprestar", "Carla", "L003"), ("devolver", "Bruno", "L001"),
            ("remover", "L001"), ("remover", "L003"), ("emprestar", "Carla", "L003")])),
        ("lista de movimentos vazia", True, lambda: (acervo_a(), emp_a(), [])),
        ("21 movimentos (todos os motivos de recusa)", True, lambda: (acervo_antigo(), {}, list(MOVS_GRANDE))),
        ("outro acervo, mesmo livro emprestado duas vezes e removido depois", True, lambda: (acervo_x(), {}, [
            ("emprestar", "Zeca", "M1"), ("emprestar", "Zeca", "M1"), ("emprestar", "Zeca", "M3"),
            ("emprestar", "Zeca", "M5"), ("emprestar", "Zeca", "M3"), ("devolver", "Zeca", "M1"),
            ("remover", "M1"), ("devolver", "Lia", "M3"), ("remover", "M3"), ("remover", "M2")])),
    ],
}

DICAS_FUNCAO = {
    "criar_livro": "monte um dicionario com as 4 chaves e devolva com return (nao use print).",
    "cadastrar_livro": "teste com 'in' se o codigo ja e chave do acervo ANTES de gravar; devolva True/False.",
    "buscar_livro": "se o codigo nao esta no acervo, devolva None em vez de acessar acervo[codigo].",
    "atualizar_livro": "confira DUAS coisas antes de alterar: o codigo existe? o campo existe dentro do livro?",
    "listar_titulos": "percorra o acervo, pegue o campo \"titulo\" de cada livro e guarde numa lista.",
    "livros_do_aluno": "se o aluno nao esta em emprestimos, devolva [] sem criar a chave.",
    "livro_esta_emprestado": "percorra TODOS os alunos; so devolva False depois de olhar todos.",
    "emprestar_livro": "verifique as regras na ordem do enunciado e faca as duas alteracoes so no final; devolva 2 valores.",
    "devolver_livro": "aluno que nao existe em emprestimos tambem e 'nao emprestado'; apague o aluno se a lista ficar vazia.",
    "remover_livro": "use livro_esta_emprestado; a ordem das recusas e: inexistente, depois emprestado.",
    "relatorio_por_autor": "na 1a vez que o autor aparece a contagem comeca em 1; use d.get(chave, 0) + 1.",
    "relatorio_indisponiveis": "guarde o TITULO (nao o codigo) de cada livro com exemplares == 0.",
    "relatorio_emprestimos_mes": "soma de linha: i fixo, j varia; soma de coluna: j fixo, i varia; devolva 2 valores; use len(), nao numeros fixos.",
    "processar_movimentos": "depende de emprestar_livro, devolver_livro e remover_livro: confira primeiro se elas passam.",
}

DICAS_ERRO = {
    "KeyError": "voce acessou uma chave que nao existe no dicionario; teste com 'in' antes de usar",
    "ValueError": "talvez 'remove' em algo que nao esta na lista, ou desempacotou o numero errado de valores",
    "TypeError": "operacao com tipos incompativeis (ex.: None no lugar de numero/lista) ou numero errado de argumentos",
    "IndexError": "indice fora da lista; confira o tamanho com len()",
    "NameError": "nome nao definido: erro de digitacao ou variavel criada em outra funcao (variavel local nao existe fora)",
    "UnboundLocalError": "variavel usada antes de receber valor dentro da funcao",
    "AttributeError": "metodo usado em um tipo que nao o possui (ex.: .append em dicionario)",
    "RecursionError": "a funcao chama a si mesma sem parar",
    "ZeroDivisionError": "divisao por zero",
}


# ---------------------------------------------------------------- comparacao
def numero(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def igual(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return type(a) is type(b) and a == b
    if numero(a) and numero(b):
        return a == b
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(igual(a[k], b[k]) for k in a)
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(igual(x, y) for x, y in zip(a, b))
    return a == b


def resumo(x, limite=110):
    s = repr(x)
    return s if len(s) <= limite else s[: limite - 3] + "..."


def diferenca(obt, esp, caminho=""):
    """Texto curto com a primeira diferenca encontrada (ou None)."""
    nome = caminho or "valor"
    if igual(obt, esp):
        return None
    mesmo_tipo = type(obt) is type(esp) or (numero(obt) and numero(esp))
    if not mesmo_tipo:
        return f"{nome}: o tipo esperado e {type(esp).__name__}, o seu e {type(obt).__name__} ({resumo(obt, 50)})"
    if isinstance(esp, dict):
        falta = [k for k in esp if k not in obt]
        sobra = [k for k in obt if k not in esp]
        if falta:
            return f"{nome}: faltam as chaves {resumo(falta, 60)}"
        if sobra:
            return f"{nome}: sobram as chaves {resumo(sobra, 60)}"
        for k in esp:
            d = diferenca(obt[k], esp[k], f"{caminho}[{k!r}]")
            if d:
                return d
    if isinstance(esp, (list, tuple)):
        if len(obt) != len(esp):
            return f"{nome}: esperados {len(esp)} itens, o seu tem {len(obt)} (seu {resumo(obt, 50)})"
        for k, (x, y) in enumerate(zip(obt, esp)):
            d = diferenca(x, y, f"{caminho}[{k}]")
            if d:
                return d
    return f"{nome}: seu {resumo(obt, 60)} | esperado {resumo(esp, 60)}"


# ---------------------------------------------------------------- worker (um por funcao)
def carregar(caminho):
    """Executa o arquivo do aluno. Devolve (ns, erro_de_carga)."""
    def sem_input(*a, **k):
        raise RuntimeError("nao use input() neste exercicio")

    with open(caminho, encoding="utf-8", errors="replace") as f:
        fonte = f.read()
    nome = os.path.basename(caminho)
    ns = {"__name__": "__aluno__", "print": lambda *a, **k: None, "input": sem_input}
    try:
        exec(compile(fonte, nome, "exec"), ns)
        return ns, None
    except SyntaxError as e:
        return ns, ("SyntaxError", f"{e.msg}", e.lineno, True)
    except BaseException as e:  # noqa: BLE001
        linha = None
        for fr in traceback.extract_tb(e.__traceback__):
            if fr.filename == nome:
                linha = fr.lineno
        return ns, (type(e).__name__, str(e), linha, False)


def linha_do_aluno(exc, nome_arq):
    linha = None
    for fr in traceback.extract_tb(exc.__traceback__):
        if fr.filename == nome_arq:
            linha = fr.lineno
    return linha


def worker(caminho, nome_func):
    nome_arq = os.path.basename(caminho)
    ns, erro = carregar(caminho)
    saida = {"carga": erro, "status": "ok", "casos": [], "assinatura": None}
    if nome_func == "__carga__":
        print(MARCA + json.dumps(saida), flush=True)
        return
    f = ns.get(nome_func)
    if not callable(f):
        saida["status"] = "ausente"
        print(MARCA + json.dumps(saida), flush=True)
        return
    import inspect
    try:
        n_param = len(inspect.signature(f).parameters)
    except (TypeError, ValueError):
        n_param = None
    esperado_n = len(PARAMS[nome_func])
    if n_param is not None and n_param != esperado_n:
        saida["status"] = "assinatura"
        saida["assinatura"] = [n_param, esperado_n]
        print(MARCA + json.dumps(saida), flush=True)
        return
    for k, (descr, extra, monta) in enumerate(CASOS[nome_func]):
        print(f"@@CASO {k}", flush=True)
        args = monta()
        ref_args = copy.deepcopy(args)
        esp_ret = REF[nome_func](*ref_args)
        al_args = copy.deepcopy(args)
        msgs = []
        try:
            obt_ret = f(*al_args)
        except BaseException as e:  # noqa: BLE001
            linha = linha_do_aluno(e, nome_arq)
            onde = f" (linha {linha})" if linha else ""
            msgs.append(f"erro ao executar{onde}: {type(e).__name__}: {e}")
            if type(e).__name__ in DICAS_ERRO:
                msgs.append("dica: " + DICAS_ERRO[type(e).__name__])
            saida["casos"].append({"descr": descr, "extra": extra, "ok": False, "msgs": msgs,
                                   "entrada": entrada(nome_func, args)})
            continue
        if not igual(obt_ret, esp_ret):
            msgs.append(f"a funcao devolveu {resumo(obt_ret, 90)} | esperado {resumo(esp_ret, 90)}")
            if obt_ret is None and esp_ret is not None:
                msgs.append("a funcao devolveu None: faltou o 'return' (ou a funcao ainda esta vazia)?")
            elif isinstance(esp_ret, tuple) and not isinstance(obt_ret, tuple):
                msgs.append("era para devolver DOIS valores de uma vez: return ok, motivo")
            else:
                d = diferenca(obt_ret, esp_ret, "devolvido")
                if d and isinstance(esp_ret, (dict, list, tuple)):
                    msgs.append(d)
        for i, (a, e) in enumerate(zip(al_args, ref_args)):
            if not igual(a, e):
                nome_p = PARAMS[nome_func][i]
                d = diferenca(a, e, nome_p)
                msgs.append(f"depois da chamada, o argumento '{nome_p}' deveria ficar diferente: {d}")
                break
        saida["casos"].append({"descr": descr, "extra": extra, "ok": not msgs, "msgs": msgs,
                               "entrada": entrada(nome_func, args)})
    print(MARCA + json.dumps(saida), flush=True)


def entrada(nome_func, args):
    return [f"{p} = {resumo(a, 95)}" for p, a in zip(PARAMS[nome_func], args)]


# ---------------------------------------------------------------- orquestracao
def rodar_worker(caminho, nome):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        p = subprocess.run([sys.executable, os.path.abspath(__file__), "--worker", caminho, nome],
                           capture_output=True, timeout=TEMPO_MAX, env=env)
        out = p.stdout.decode("utf-8", errors="replace")
        err = p.stderr.decode("utf-8", errors="replace")
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b"").decode("utf-8", errors="replace") if isinstance(e.stdout, (bytes, type(None))) else str(e.stdout)
        casos = re.findall(r"@@CASO (\d+)", out)
        return {"timeout": True, "ultimo_caso": int(casos[-1]) if casos else None}
    if MARCA not in out:
        return {"quebrou": True, "erro": err.strip().splitlines()[-1] if err.strip() else "sem resposta"}
    return json.loads(out.split(MARCA, 1)[1].splitlines()[0])


def conferir_explicacao(texto):
    achadas = {}
    for m in re.finditer(r"(?m)^#[ \t]*R(\d)[ \t]*:[ \t]*(.*)$", texto):
        if len(m.group(2).strip()) >= 25:
            achadas[m.group(1)] = True
    return len(achadas)


def main():
    try:
        sys.stdout.reconfigure(errors="replace")
    except Exception:  # noqa: BLE001
        pass
    base = os.path.dirname(os.path.abspath(__file__))
    caminho = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, "solucao.py")
    if not os.path.exists(caminho):
        caminho = os.path.join(base, caminho)
    if not os.path.exists(caminho):
        print(f"Arquivo nao encontrado: {caminho}")
        return 2
    nome = os.path.basename(caminho)
    print("=" * 68)
    print(f" Conferindo {nome}")
    print("=" * 68)

    carga = rodar_worker(caminho, "__carga__")
    if carga.get("timeout"):
        print("\nO arquivo ficou mais de %ds carregando: ha um laco infinito FORA das funcoes" % TEMPO_MAX)
        print("(codigo solto no meio do arquivo, como um while sem fim). Corrija e rode de novo.")
        print("\n" + "-" * 68 + "\n Funcoes corretas: 0 de 14\n" + "-" * 68)
        return 1
    if carga.get("quebrou"):
        print("\nNao consegui carregar o arquivo:", carga.get("erro"))
        return 1
    erro_c = carga.get("carga")
    if erro_c and erro_c[3]:
        print(f"\nErro de escrita no codigo (linha {erro_c[2]}): {erro_c[0]}: {erro_c[1]}")
        print("Corrija esse erro (parenteses, dois-pontos, indentacao) e rode de novo.")
        print("\n" + "-" * 68 + "\n Funcoes corretas: 0 de 14\n" + "-" * 68)
        return 1
    if erro_c:
        print(f"\nATENCAO: o arquivo deu erro ao ser executado (linha {erro_c[2]}): {erro_c[0]}: {erro_c[1]}")
        print("As funcoes definidas ANTES dessa linha ainda sao testadas; as depois dela nao existem para o teste.")

    corretas = 0
    so_extras = 0
    grupo_atual = None
    for num, nf, params, grupo in FUNCOES:
        if grupo != grupo_atual:
            grupo_atual = grupo
            print(f"\n{GRUPOS[grupo]}")
        r = rodar_worker(caminho, nf)
        rotulo = f"{num:>2}. {nf}"
        if r.get("timeout"):
            print(f"  [ X] {rotulo}")
            k = r.get("ultimo_caso")
            if k is not None:
                print(f"        parou de responder em mais de {TEMPO_MAX}s no caso: {CASOS[nf][k][0]}")
            print("        dica: provavel laco infinito (while sem condicao de parada)")
            continue
        if r.get("quebrou"):
            print(f"  [ X] {rotulo}\n        o teste desta funcao quebrou: {r.get('erro')}")
            continue
        if r["status"] == "ausente":
            print(f"  [ X] {rotulo}\n        funcao nao encontrada: confira o 'def {nf}(...)' (nome exato, sem mudar)")
            continue
        if r["status"] == "assinatura":
            print(f"  [ X] {rotulo}\n        a funcao tem {r['assinatura'][0]} parametros; o certo sao {r['assinatura'][1]}: def {nf}({', '.join(params)})")
            continue
        falhas = [c for c in r["casos"] if not c["ok"]]
        if not falhas:
            corretas += 1
            print(f"  [OK] {rotulo}  ({len(r['casos'])} casos)")
            continue
        oficiais_ok = all(c["ok"] for c in r["casos"] if not c["extra"])
        if oficiais_ok:
            so_extras += 1
        print(f"  [ X] {rotulo}  ({len(falhas)} de {len(r['casos'])} casos falharam)")
        for c in falhas[:1]:
            print(f"        caso: {c['descr']}" + ("  [caso extra]" if c["extra"] else ""))
            for linha in c["entrada"]:
                print(f"          entrada: {linha}")
            for m in c["msgs"]:
                print(f"          {m}")
        if len(falhas) > 1:
            print(f"        (mais {len(falhas) - 1} caso(s) falharam; corrija este primeiro e rode de novo)")
        if oficiais_ok:
            print("        (passa nos exemplos do enunciado mas falha em casos extras: a logica precisa valer para outros dados)")
        print(f"        dica: {DICAS_FUNCAO[nf]}")

    print("\nExplicacao do final do arquivo")
    with open(caminho, encoding="utf-8", errors="replace") as f:
        fonte = f.read()
    expl = fonte.split(EXPL, 1)[1] if EXPL in fonte else ""
    n = conferir_explicacao(expl)
    print(f"  [{'OK' if n == 2 else ' X'}] {n} de 2 respostas (R1, R2) preenchidas, com pelo menos uma frase cada")

    print("\n" + "-" * 68)
    print(f" Funcoes corretas: {corretas} de {len(FUNCOES)}")
    if so_extras:
        print(f" (falham so em casos extras: {so_extras})")
    print("-" * 68)
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "--worker":
        worker(sys.argv[2], sys.argv[3])
    else:
        sys.exit(main())
