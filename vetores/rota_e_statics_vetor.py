notas = [6.5, 8.0, 4.5, 9.2, 7.0]

soma = 0
maximo = 0
minimo = 100
for nota in notas:
    soma += nota

    if nota > maximo:
        maximo = nota

    if nota < minimo:
        minimo = nota

media = soma / len(notas)

print(f"Soma = {soma}, média = {media:.2f}, máximo = {maximo}, minímo = {minimo}")