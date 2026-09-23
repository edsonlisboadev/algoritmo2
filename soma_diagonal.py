matriz = [
    [5, 1, 2],
    [3, 8, 4],
    [6, 7, 9]
]
soma = 0 

for i in range(len(matriz)):
    soma += matriz[i][i]

print(soma)

