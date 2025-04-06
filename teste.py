menu = """
1-Cadastrar-se
2-Login
3-Sair
"""

opcao = int(input(menu))

while opcao != 3:
    if opcao == 1:
        menu = """
        1-Preencher cadastro
        2-Voltar para o menu principal
        """
        opcaoInt = int(input(menu))

        while opcaoInt != 2:
            if opcaoInt == 1:
                print("Cadastrado!")
            else:
                print("Opção inválida")
            opcaoInt = int(input(menu))

    elif opcao == 2:
        menu = """
        1-Preencher login
        2-Voltar para o menu principal
        """
        opcaoInt = int(input(menu))

        while opcaoInt != 2:
            if opcaoInt == 1:
                print("Logado!")
            else:
                print("Opção inválida")
            opcaoInt = int(input(menu))

    opcao = int(input(menu))