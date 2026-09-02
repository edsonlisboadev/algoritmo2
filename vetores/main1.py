n = int(input("Quantos números você vai digitar? "))

vet: list[float] = []

for i in range(n):
    vet.append(float(input("Digite um número: ")))


print()
print("NUMEROS DIGITADOS: \n")
for numero in vet:
    print(f"{numero :.1f}") 

soma = sum(vet)
media = soma / n
maximo = max(vet)
minimo = min(vet)

print(f"valor média{media :.1f}\n")
print(f"valor da soma{soma :.1f}\n")
print(f"valor máximo{maximo :.1f}\n")
print(f"valor minímo{minimo :.1f}\n")