compras = [
    {
        "nome" : "Carne",
        "value" : 49.9,
        "amount" : 3
    },
    {
        "nome" : "Arroz", 
        "value" : 5.9,
        "amount" : 2
    },
    {
        "nome" : "Feijão", 
        "value" : 7.9,
        "amount" : 1
    },  
    {
        "nome" : "Leite", 
        "value" : 6.9,
        "amount" : 3
    }
]

total = sum(item["value"] * item["amount"] for item in compras)
subtotal = 0


print("-----RESUMO DE COMPRAS-----\n")


for item in compras:
    subtotal = item["value"] * item["amount"] 
    print(f"Nome: {item['nome']}, valor: {item['value']}, quantidade: {item['amount']}, final: {subtotal:.2f}")

print(f"Valor total deu: {total:.2f}\n")


if total >= 200:
    total -= total * 0.9
else:
    print("SEM DESCONTO, POIS NÃO ULTRAPASSOU OS R$200,00\n")
    