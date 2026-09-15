def main():
    try:
        n = int(input("Digite o número até o qual quer ver múltiplos de 3 e 5: "))
    except ValueError:
        print("Entrada inválida. Digite um número inteiro.")
        return

    if n <= 0:
        print("Digite um número maior que zero.")
        return

    multiplos = []
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            multiplos.append(i)

    print("Múltiplos de 3 e 5 até", n, ":", multiplos)
    print("Quantidade:", len(multiplos))

if __name__ == "__main__":
    main()
