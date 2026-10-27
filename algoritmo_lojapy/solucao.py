"""
Loja de Papelaria — análise de vendas do semestre
Algoritmos II · Univille
Aluno: Edson Dal Bo Lisboa Junior

Regras: use apenas listas, matrizes (lista de listas), dicionários, for/while e if.
Não é preciso criar funções. Não use input(). Não altere o bloco de DADOS.
Seu código deve funcionar para outros dados: use len(), nunca números fixos.

Para conferir seu trabalho:   python testes.py
"""

# ===== DADOS (não altere esta parte) =====
codigos = ["P01", "P02", "P03", "P04", "P05", "P06"]
meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun"]

# vendas[i][j] = unidades vendidas do produto codigos[i] no mês meses[j]
vendas = [
    [320, 300, 280, 250, 270, 310],   # P01
    [150, 160, 140, 170, 165, 180],   # P02
    [40, 38, 45, 60, 52, 35],         # P03
    [25, 30, 22, 22, 20, 41],         # P04
    [200, 180, 170, 160, 150, 145],   # P05
    [90, 95, 88, 92, 100, 105],       # P06
]

catalogo = {
    "P01": {"nome": "Caneta",      "preco": 2.50,   "estoque": 600},
    "P02": {"nome": "Caderno",     "preco": 18.90,  "estoque": 515},
    "P03": {"nome": "Mochila",     "preco": 129.90, "estoque": 90},
    "P04": {"nome": "Calculadora", "preco": 59.90,  "estoque": 120},
    "P05": {"nome": "Pasta",       "preco": 6.50,   "estoque": 300},
    "P06": {"nome": "Marcador",    "preco": 4.20,   "estoque": 400},
}
# ===== FIM DOS DADOS =====


# ===== ETAPA 1 — vetores a partir da matriz =====
# total_por_produto : lista com o total de unidades vendidas de cada produto
#                     (mesma ordem de 'codigos')
# total_por_mes     : lista com o total de unidades vendidas em cada mês
#                     (mesma ordem de 'meses')
# mes_mais_vendido  : nome do mês com mais unidades vendidas (empate: o primeiro)

total_por_produto = []
for i in range(len(codigos)):
    soma = 0
    for j in range(len(meses)):
        soma = soma + vendas[i][j]
    total_por_produto.append(soma)

# para somar uma coluna, o laço de fora passa a ser o dos meses
total_por_mes = []
for j in range(len(meses)):
    soma = 0
    for i in range(len(codigos)):
        soma = soma + vendas[i][j]
    total_por_mes.append(soma)

# começa pelo primeiro mês e só troca se achar um MAIOR (assim o empate fica com o primeiro)
mes_mais_vendido = meses[0]
maior_venda = total_por_mes[0]
for j in range(len(meses)):
    if total_por_mes[j] > maior_venda:
        maior_venda = total_por_mes[j]
        mes_mais_vendido = meses[j]

# ===== ETAPA 2 — faturamento (dicionário + matriz + vetor) =====
# faturamento           : dicionário  código -> total vendido em R$ (unidades x preço)
# faturamento_total     : soma do faturamento de todos os produtos
# mes_maior_faturamento : nome do mês com maior faturamento em R$ (empate: o primeiro)

faturamento = {}
faturamento_total = 0
for i in range(len(codigos)):
    codigo = codigos[i]
    preco = catalogo[codigo]["preco"]
    faturamento[codigo] = total_por_produto[i] * preco
    faturamento_total = faturamento_total + faturamento[codigo]

faturamento_por_mes = []
for j in range(len(meses)):
    soma = 0
    for i in range(len(codigos)):
        soma = soma + vendas[i][j] * catalogo[codigos[i]]["preco"]
    faturamento_por_mes.append(soma)

mes_maior_faturamento = meses[0]
maior_valor = faturamento_por_mes[0]
for j in range(len(meses)):
    if faturamento_por_mes[j] > maior_valor:
        maior_valor = faturamento_por_mes[j]
        mes_maior_faturamento = meses[j]



# ===== ETAPA 3 — reposição de estoque =====
# Um produto precisa de reposição se o estoque for MENOR que o total vendido
# nos 3 últimos meses.
# reposicao : dicionário  código -> quantidade que falta (vendas dos 3 últimos meses
#             menos estoque). Só entram os produtos que precisam de reposição.

reposicao = {}
for i in range(len(codigos)):
    codigo = codigos[i]
    vendas_ultimos_3 = 0
    # os 3 últimos meses são sempre os 3 últimos índices, tenha a matriz quantos meses tiver
    for j in range(len(meses) - 3, len(meses)):
        vendas_ultimos_3 = vendas_ultimos_3 + vendas[i][j]
    estoque = catalogo[codigo]["estoque"]
    if estoque < vendas_ultimos_3:
        reposicao[codigo] = vendas_ultimos_3 - estoque



# ===== ETAPA 4 — top 3 por faturamento =====
# top3 : lista com os 3 códigos de maior faturamento, do maior para o menor
# Depois, imprima o ranking (veja o formato no enunciado).

# sem sort: acha o maior que ainda não está no top3, três vezes
top3 = []
while len(top3) < 3:
    melhor = ""
    for codigo in codigos:
        if codigo not in top3:
            if melhor == "" or faturamento[codigo] > faturamento[melhor]:
                melhor = codigo
    top3.append(melhor)

print("TOP 3 POR FATURAMENTO")
for posicao in range(len(top3)):
    codigo = top3[posicao]
    nome = catalogo[codigo]["nome"]
    print(f"{posicao + 1}. {nome} ({codigo}) - R$ {faturamento[codigo]:.2f}")



# ===== ETAPA 5 (desafio) — sequências de queda =====
# maior_queda : dicionário  código -> maior número de quedas SEGUIDAS nas vendas
#               (queda = vendas do mês menor que as do mês anterior; igual não é queda)
# em_alerta   : lista com os NOMES dos produtos com 3 ou mais quedas seguidas
#               (na ordem de 'codigos')

maior_queda = {}
for i in range(len(codigos)):
    seguidas = 0   # zera a cada produto
    maior = 0
    for j in range(1, len(meses)):
        if vendas[i][j] < vendas[i][j - 1]:
            seguidas = seguidas + 1
        else:
            seguidas = 0   # subiu ou ficou igual: a sequência quebra
        if seguidas > maior:
            maior = seguidas
    maior_queda[codigos[i]] = maior

em_alerta = []
for codigo in codigos:
    if maior_queda[codigo] >= 3:
        em_alerta.append(catalogo[codigo]["nome"])

