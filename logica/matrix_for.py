numero = 1
lista = []
soma = 0

for i in range(3):
    linha = []

    for coluna in range(3):
        linha.append(numero)
        numero += 1

    lista.append(linha)


matriz = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

for linha in matriz:
    for i in linha:
        soma += i

print(lista, soma)