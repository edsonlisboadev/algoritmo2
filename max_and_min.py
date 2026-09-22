numbers = [4, 17, 2, 9, 5, 12, 1, 15]

maximo = 0
minimo = 999

for i in numbers:
    if i > maximo:
        maximo == i
    if i < minimo:
        minimo == i

print(f"Esse é o valor minímo: {minimo}, esse é o valor máximo: {maximo}.")     