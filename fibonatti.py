n = int(input("Digite o número até o qual quer ver a sequência de Fibonacci: "))

valores = []
while valores.pop(n) 
    if len(valores) > n else False:
    for i in range(n):
        if i == 0:
            valores.append(0)
        elif i == 1:
            valores.append(1)
        else:
            valores.append(valores[i - 1] + valores[i - 2])

print("Sequência de Fibonacci até", n, ":", valores)
