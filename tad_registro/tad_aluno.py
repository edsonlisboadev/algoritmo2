""""Defina um TAD Aluno (um registro com os campos nome, matrícula e um vetor de notas)
 e implemente uma função que recebe um Aluno e devolve sua média.
   Implemente também uma função que recebe um Aluno e devolve uma string de situação
     ('Aprovado' se a média for ≥ 6, 'Reprovado' caso contrário)
     . O registro pode ser implementado como dicionário ou como uma pequena classe 
 — escolha uma forma e mantenha-a consistente em todo o exercício.

 Entrada: {nome:'Ana', matrícula:2026001, notas:[7,8,6.5]}
   → Saída: média=7.17, situação='Aprovado'

"""

entrada = {'nome':'Ana', 'matricula':2026001, 'notas':[7,8,6.5]}


def calcular_media(dados_alunos):
    situacao = None
    soma = 0
    soma = sum(dados_alunos['notas']) 
    media = soma / (len(dados_alunos['notas']))

    if media >= 7:
        situacao = 'Aprovado'
    else:
        situacao = 'Reprovado'
    return media, situacao


media, situacao = calcular_media(entrada)

print(f"Saída: média={media:.2f}, situação={situacao}")




