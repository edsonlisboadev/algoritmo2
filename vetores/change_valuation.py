
def buy_entry():
    buy = float(input("QUAL O VALOR DA SUA COMPRA?\n"))

    return buy


def payout():
    pay = float(input("COM QUAL VALOR VOCÊ IRÁ PAGAR?\n"))

    return pay

def change_calculated(buy, pay):
    if buy > pay:
        return "SEU PAGAMENTO DEVE SER MAIOR DO QUE A SUA COMPRA\n"

    change = pay - buy
    print(f"O total do seu troco foi: {change:.2f}\n")

    change_cents = int(round(change * 100))
    options_cents = [5000, 2000, 1000, 500, 200, 100, 50, 25, 10, 5, 1]

    used_cents = []


    for option in options_cents:
        amount = change_cents // option

        if change_cents >= option:
            value_in_reais = option / 100

            used_cents.append(f"Quantidade = {amount}, R${value_in_reais:.2f}")

            change_cents = change_cents % option

    return ",".join(used_cents)


valor_compra = buy_entry()
valor_pagamento = payout()

print(change_calculated(valor_compra, valor_pagamento))
