numero = float(input("Escreva o número do qual você quer a tabuada.\n"))
multi = 0
for i in range(1, 11):
    multi += i
    resultado = numero * multi
    print(f"{numero} x  {multi} = {resultado}") 