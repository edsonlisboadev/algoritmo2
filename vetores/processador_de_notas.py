
def entrada():
      while True:
            try:
                nota = float(input("Escreva sua nota:\n"))

                if nota < 0 or nota > 10:
                    print("Escreva um valor válido entre 0 e 10!!\n")

                else:
                     return nota

            except ValueError:
                print("Digite um valor válido.\n")
    


def classificados(nota):
     if nota >= 6:
          return "Aprovado"
     else:
          return "Reprovado"


def contar_aprovados(notas):
    aprovados = 0
    reprovados = 0

    for nota in notas:
        resultado = classificados(nota)

        if resultado == "Aprovado":
            aprovados = aprovados + 1
        elif resultado == "Reprovado":
             reprovados = reprovados + 1             

    return aprovados, reprovados
     

def media_geral(notas):
    soma = sum(notas)
    media = soma / len(notas)
    return media 

def relatorio(media, aprovados, reprovados):

     print(f"Valor médio: {media :.2f}", " Aprovados: ", aprovados,"  Reprovados: ", reprovados)





n = int(input("Quantas notas você vai digitar?\n"))

vet : list[float] = []


for i in range (n):
    nota = entrada()

    vet.append(nota)


aprovados, reprovados = contar_aprovados(vet)
media = media_geral(vet)
relatorio = relatorio(media, aprovados, reprovados)
