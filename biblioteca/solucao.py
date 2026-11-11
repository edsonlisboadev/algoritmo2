"""
Sistema de biblioteca — exercício para casa (funções)
Algoritmos II · Univille

Nome: ______________________________   Data de entrega: quinta-feira, 12/11, até 23h50

Regras:
  - Escreva o corpo de cada função abaixo. NÃO mude o nome das funções nem a
    ordem e os nomes dos parâmetros: o testes.py chama cada função pelo nome.
  - Use apenas o que vimos: variáveis, if, for, while, listas, tuplas, dicionários e funções.
    Não use import e não use input().
  - Cada função recebe tudo de que precisa por PARÂMETRO e devolve o resultado com return.
    Não use variáveis globais dentro das funções.
  - Cada função é independente das outras: se travar numa, siga para a próxima.
    (Algumas chamam funções anteriores, e isso está avisado na própria função.)
  - Para conferir seu trabalho a qualquer momento:   python testes.py
"""

# ===== DADOS DE EXEMPLO (para você testar à mão; não use dentro das funções) =====
acervo_exemplo = {
    "L001": {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "ano": 1899, "exemplares": 2},
    "L002": {"titulo": "Capitães da Areia", "autor": "Jorge Amado", "ano": 1937, "exemplares": 1},
    "L003": {"titulo": "Vidas Secas", "autor": "Graciliano Ramos", "ano": 1938, "exemplares": 0},
    "L004": {"titulo": "Quincas Borba", "autor": "Machado de Assis", "ano": 1891, "exemplares": 3},
}
emprestimos_exemplo = {"Ana": ["L001", "L004"], "Bruno": ["L002"]}
categorias_exemplo = ["Romance", "Didático"]
meses_exemplo = ["Jan", "Fev", "Mar"]
matriz_exemplo = [
    [10, 12, 9],   # Romance
    [4, 15, 8],    # Didático
]
# ===== FIM DOS DADOS DE EXEMPLO =====

# ===== PARTE 1 — cadastro de livros =====
# Funções 1 a 5: criar, cadastrar, buscar, atualizar e listar.


# ---- função 1 ----
def criar_livro(titulo, autor, ano, exemplares):
    """Monta e devolve o dicionário de UM livro, com as chaves
    "titulo", "autor", "ano" e "exemplares".
    Não mexe em nenhum acervo: só cria e devolve (return).
    """
    # SEU CÓDIGO AQUI
    pass


# ---- função 2 ----
def cadastrar_livro(acervo, codigo, livro):
    """Guarda o livro no acervo usando o código como chave.
    Se o código JÁ existe, não grava nada (o primeiro cadastro vale).
    Devolve True se cadastrou e False se recusou.
    """
    # SEU CÓDIGO AQUI
    pass


# ---- função 3 ----
def buscar_livro(acervo, codigo):
    """Procura um livro pelo código.
    Devolve o dicionário do livro, ou None se o código não existe.
    Não altera o acervo.
    """
    # SEU CÓDIGO AQUI
    pass


# ---- função 4 ----
def atualizar_livro(acervo, codigo, campo, valor):
    """Troca o valor de um campo de um livro: campo é o nome ("titulo",
    "autor", "ano" ou "exemplares") e valor é o novo conteúdo.
    Devolve False, sem alterar nada, se o código não existe OU se o campo
    não é um dos campos do livro. Senão altera e devolve True.
    """
    # SEU CÓDIGO AQUI
    pass


# ---- função 5 ----
def listar_titulos(acervo):
    """Devolve uma LISTA com os títulos de todos os livros do acervo,
    na ordem em que estão no acervo. Acervo vazio devolve lista vazia.
    """
    # SEU CÓDIGO AQUI
    pass


# ===== PARTE 2 — empréstimos e remoção =====
# Funções 6 a 10: quem está com o quê, emprestar, devolver e remover.


# ---- função 6 ----
def livros_do_aluno(emprestimos, aluno):
    """emprestimos é um dicionário: aluno -> lista dos códigos que ele tem.
    Devolve a lista de códigos do aluno; se o aluno não está no dicionário
    (nunca pegou livro), devolve uma lista vazia. Não altera emprestimos.
    """
    # SEU CÓDIGO AQUI
    pass


# ---- função 7 ----
def livro_esta_emprestado(emprestimos, codigo):
    """Devolve True se ALGUM aluno está com o livro desse código,
    e False se ninguém está.
    """
    # SEU CÓDIGO AQUI
    pass


# ---- função 8 ----
def emprestar_livro(acervo, emprestimos, aluno, codigo):
    """Tenta emprestar o livro ao aluno. Devolve DOIS valores: (ok, motivo).
    Recusa, verificando NESTA ORDEM:
      "inexistente"   o código não está no acervo
      "sem exemplar"  o livro existe, mas exemplares == 0
      "limite"        o aluno já está com 3 livros
    Se recusou: devolve (False, motivo) e não altera nada.
    Se aceitou: exemplares diminui 1, o código entra na lista do aluno em
    emprestimos e devolve (True, "ok").
    Dica: use a função livros_do_aluno.
    """
    # SEU CÓDIGO AQUI
    pass


# ---- função 9 ----
def devolver_livro(acervo, emprestimos, aluno, codigo):
    """Registra a devolução. Devolve DOIS valores: (ok, motivo).
    Recusa com (False, "nao emprestado") se o aluno não está com esse livro
    (inclui o aluno que nunca pegou livro nenhum).
    Se aceitou: o código sai da lista do aluno, exemplares aumenta 1 e
    devolve (True, "ok"). Se a lista do aluno ficar vazia, o aluno deixa de
    aparecer em emprestimos.
    Dica: use a função livros_do_aluno.
    """
    # SEU CÓDIGO AQUI
    pass


# ---- função 10 ----
def remover_livro(acervo, emprestimos, codigo):
    """Tira um livro do acervo. Devolve DOIS valores: (ok, motivo).
    Recusa com (False, "inexistente") se o código não está no acervo, ou com
    (False, "emprestado") se algum aluno está com o livro.
    Se aceitou: apaga o livro do acervo e devolve (True, "ok").
    Dica: use a função livro_esta_emprestado.
    """
    # SEU CÓDIGO AQUI
    pass


# ===== PARTE 3 — relatórios =====
# Funções 11 a 13: três relatórios simples.


# ---- função 11 ----
def relatorio_por_autor(acervo):
    """Devolve um dicionário: autor -> quantidade de títulos desse autor
    no acervo.
    """
    # SEU CÓDIGO AQUI
    pass


# ---- função 12 ----
def relatorio_indisponiveis(acervo):
    """Devolve uma lista com os TÍTULOS dos livros com exemplares == 0,
    na ordem do acervo. Se todos têm exemplar, devolve lista vazia.
    """
    # SEU CÓDIGO AQUI
    pass


# ---- função 13 ----
def relatorio_emprestimos_mes(matriz, categorias, meses):
    """matriz[i][j] = empréstimos da categoria categorias[i] no mês meses[j].
    Devolve DOIS valores: (total_por_categoria, mes_mais_movimentado)
      total_por_categoria: dicionário categoria -> soma da linha da matriz
      mes_mais_movimentado: NOME do mês com maior soma de coluna
                            (empate: vale o primeiro)
    Não altera a matriz.
    """
    # SEU CÓDIGO AQUI
    pass


# ===== PARTE 4 (desafio) — juntando tudo =====
# Função 14: processa uma lista de movimentos usando as funções das partes anteriores.


# ---- função 14 ----
def processar_movimentos(acervo, emprestimos, movimentos):
    """movimentos é uma lista de tuplas, na ordem em que aconteceram:
      ("emprestar", aluno, codigo)   ("devolver", aluno, codigo)   ("remover", codigo)
    Executa cada movimento com as funções emprestar_livro, devolver_livro e
    remover_livro (o primeiro movimento é o de número 1).
    Devolve a lista das RECUSAS: tuplas (número_do_movimento, motivo),
    na ordem dos movimentos. Movimentos aceitos não entram na lista.
    """
    # SEU CÓDIGO AQUI
    pass


# ===== TESTE À MÃO (opcional) =====
# Aqui você pode chamar suas funções com os dados de exemplo e dar print para
# conferir. Rode:  python solucao.py   (o testes.py não mostra os seus prints).
# Exemplo:
#   print(buscar_livro(acervo_exemplo, "L001"))


# ===== EXPLICAÇÃO (obrigatória — com suas palavras, 1 a 3 frases cada) =====
# Pergunta 1: Na sua função cadastrar_livro, o que acontece quando o código já
#             existe? Por que você fez assim?
# R1:
# Pergunta 2: As funções recebem acervo e emprestimos como PARÂMETRO, em vez de
#             usar variáveis globais. Por que isso é melhor? E por que dentro de
#             cadastrar_livro basta fazer acervo[codigo] = livro, sem "return acervo"?
# R2:
