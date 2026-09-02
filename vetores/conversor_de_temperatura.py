def conversor(celsius):
    
    celsius = (fah - 32) * 5/9 
    return celsius

def ambiente(celsius, estado):
    if celsius <= 0:
        estado == "Congelante"

    elif celsius > 0 and celsius < 25:
        estado == "Ameno"

    else:
        estado == "Quente"

    return estado


def relatorio(celsius):
    for len(celsius) in range:
        print("Saída: [ {celsius}°C = {fah}°F({estado})]")
    return ""
##ficamos aqui em return valor de entrada



fah = float(input("Quantos fahrenheit está no momento?"))


    
    