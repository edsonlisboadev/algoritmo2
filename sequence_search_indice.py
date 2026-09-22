search = [101, 205, 309, 412, 517, 1, 0, 5, 10, 20, 51, 69, 95, 412, 579, 492]



pesquisa = int(input("Escreva o número que precisa:\n"))

if pesquisa not in search:
    print("O número não foi encontrado")

for value in range(len(search)):

    if search[value] == pesquisa:
        print (f"O número {pesquisa} foi encontrado na posição {value}")
        break