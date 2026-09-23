matriz = [ 
    [1, 3],
    [7, 5],
    [4, 2]
]
transposta= []

for c in range(len(matriz[0])):
    nova_linha = []
    for l in range(len(matriz)):
        nova_linha.append(matriz[l][c])
    transposta.append(nova_linha)


print("Matriz\n")
for linha in transposta:
    print(linha)