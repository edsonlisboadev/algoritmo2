def conversor(celsius):
    temp = 0
    celsius = (temp - 32) * 5/9 
    return celsius

def ambiente(celsius, estado):
    if celsius <= 0:
        estado == "Congelante"

    elif celsius > 0 and celsius < 25:
        estado == "Ameno"

    else:
        estado == "Quente"

    return estado






    
    