from datetime import datetime

titulo1 = "Gerenciamento de Controle Financeiro"
titulo2 = "SUAS TRANSAÇÕES"

def mostrarTitulo(texto, largura=100):
    print("-" * largura)
    print("|" + texto.center(largura - 2) + "|")
    print("-" * largura)

def mostrarOpcao(texto, largura=100):
    print("| " + texto.ljust(largura - 3) + "|")

def mostrarLinha(texto, largura=100):
    print("| " + texto.ljust(largura - 3) + "|")

def mostrarMenu():
    mostrarTitulo(titulo1)
    opcoes = [
        "0 - Sair",
        "1 - Criar nova conta",
        "2 - Adicionar receita",
        "3 - Adicionar despesa",
        "4 - Editar transação",
        "5 - Mostrar transações",
        "6 - Consultar saldo",
        "7 - Criar categoria",
        "8 - Editar categoria",
        "9 - Excluir categoria",
        "10 - Atribuir categoria a transação",
        "11 - Listar gasto por categoria"
    ]
    for opcao in opcoes:
        mostrarOpcao(opcao)
    print("-" * 100)


class Conta:
    def __init__(self, nome, cpf, saldo, tipoConta):
        self.idConta = cpf
        self.nome = nome
        self._saldo = saldo
        self.tipoConta = tipoConta
        self.transacoes = []

    def adicionarTransacao(self, transacao):
        self.transacoes.append(transacao)

    def adicionarReceita(self, valor, descricao, categoria=None):
        if valor > 0:
            self._saldo += valor
            transacao = Transacao(valor, descricao, categoria, tipo="Receita")
            self.adicionarTransacao(transacao)
            print(f"Receita de R$ {valor:.2f} adicionada. Saldo atual: R$ {self._saldo:.2f}")
        else:
            print("Valor inválido para receita.")

    def adicionarDespesa(self, valor, descricao, categoria=None):
        if valor > 0:
            if valor <= self._saldo:
                self._saldo -= valor
                transacao = Transacao(-valor, descricao, categoria, tipo="Despesa")
                self.adicionarTransacao(transacao)
                print(f"Despesa de R$ {valor:.2f} registrada. Saldo atual: R$ {self._saldo:.2f}")
            else:
                print("Saldo insuficiente para essa despesa.")
        else:
            print("Valor inválido para despesa.")

    def mostrarTransacoes(self):
        if not self.transacoes:
            print(f"Nenhuma transação na conta de {self.nome}.")
            return
        print(f"Transações da conta de {self.nome}:")
        for t in self.transacoes:
            print(t)

    def calcularSaldo(self):
        return self._saldo

    def __str__(self):
        return f"Conta: {self.nome} | Tipo: {self.tipoConta} | Saldo: R$ {self._saldo:.2f}"


class Transacao:
    contadorIdTransacao = 1

    def __init__(self, valor=0.0, descricao="", categoria=None, tipo=None):
        self.id = Transacao.contadorIdTransacao
        Transacao.contadorIdTransacao += 1
        self.valor = valor
        self.descricao = descricao
        self.categoria = categoria
        self.tipo = tipo

    def editar(self, novoValor=None, novaDescricao=None, novoTipo=None):
        if novoValor is not None:
            self.valor = novoValor
        if novaDescricao is not None:
            self.descricao = novaDescricao
        if novoTipo is not None:
            self.tipo = novoTipo

    def __str__(self):
        categoria_str = self.categoria.nomeCategoria if self.categoria else "Sem categoria"
        tipo_str = self.tipo if self.tipo else ("Receita" if self.valor > 0 else "Despesa")
        return (f"ID: {self.id} | {tipo_str} | Valor: R$ {abs(self.valor):.2f} | "
                f"Descrição: {self.descricao} | Categoria: {categoria_str}")


class Categoria:
    contadorIdCategoria = 1

    def __init__(self, nomeCategoria, tipo):
        self.idCategoria = Categoria.contadorIdCategoria
        Categoria.contadorIdCategoria += 1
        self.nomeCategoria = nomeCategoria
        self.tipo = tipo

    def criarCategoria(self):
        print(f"Categoria criada: ID:{self.idCategoria} | Nome: {self.nomeCategoria} | Tipo: {self.tipo}")

    def editarCategoria(self, nomeNovo, novoTipo):
        self.nomeCategoria = nomeNovo
        self.tipo = novoTipo
        print(f"Categoria editada: {self.nomeCategoria} ({self.tipo})")

    def excluirCategoria(self):
        print(f"Categoria '{self.nomeCategoria}' excluída.")


def gastoPorCategoria(conta):
    if not conta.transacoes:
        print("Nenhuma transação nesta conta.")
        return

    gastos = {}
    for transacao in conta.transacoes:
        if transacao.tipo == "Despesa" and transacao.categoria:
            nome_cat = transacao.categoria.nomeCategoria
            gastos[nome_cat] = gastos.get(nome_cat, 0) + abs(transacao.valor)

    mostrarTitulo(f"Gasto por Categoria - {conta.nome}")
    if not gastos:
        mostrarLinha("Nenhuma despesa registrada.")
    else:
        gastosOrdenados = sorted(gastos.items(), key=lambda x: x[1], reverse=True)
        for cat, total in gastosOrdenados:
            mostrarLinha(f"{cat}: R$ {total:.2f}")
    print("-" * 100)


def atribuirCategoriaATransacao(conta, categorias):
    if not conta.transacoes:
        print("Nenhuma transação nesta conta.")
        return

    print("Transações disponíveis:")
    for i, t in enumerate(conta.transacoes, start=1):
        print(f"{i} - {t}")

    idx_trans = int(input("Escolha a transação para adicionarmos a uma categoria: ")) - 1
    transacao = conta.transacoes[idx_trans]

    if not categorias:
        print("Nenhuma categoria existente. Vamos criar uma nova.")
        nome = input("Nome da nova categoria: ")
        tipo = "Despesa" if transacao.valor < 0 else "Receita"
        nova_cat = Categoria(nome, tipo)
        categorias.append(nova_cat)
        transacao.categoria = nova_cat
        print(f"Categoria '{nome}' atribuída à transação com sucesso!")
        return

    print("Categorias disponíveis:")
    for i, cat in enumerate(categorias, start=1):
        print(f"{i} - {cat.nomeCategoria} ({cat.tipo})")

    escolha = input("Deseja adicionar uma nova categoria? (s/n): ").strip().lower()
    if escolha == "s":
        nome = input("Nome da nova categoria: ")
        tipo = "Despesa" if transacao.valor < 0 else "Receita"
        nova_cat = Categoria(nome, tipo)
        categorias.append(nova_cat)
        transacao.categoria = nova_cat
        print(f"Categoria '{nome}' criada e atribuída à transação com sucesso!")
    else:
        idx_cat = int(input("Escolha a categoria existente: ")) - 1
        transacao.categoria = categorias[idx_cat]
        print(f"Categoria '{categorias[idx_cat].nomeCategoria}' atribuída à transação com sucesso!")


if __name__ == "__main__":
    contas = []
    categorias = []

    while True:
        mostrarMenu()
        opcao = input("Escolha o que desejas realizar: ").strip()

        if opcao == "0":
            print("Saindo... Até logo!")
            break

        elif opcao == "1":
            nome = input("Nome do titular: ")
            cpf = input("CPF: ")
            saldo = float(input("Saldo inicial: "))
            tipoConta = input("Tipo de conta: ")
            conta = Conta(nome, cpf, saldo, tipoConta)
            contas.append(conta)
            print("Conta criada com sucesso!")

        elif opcao in ["2", "3"]:
            if not contas:
                print("Nenhuma conta cadastrada.")
                continue
            for i, c in enumerate(contas, start=1):
                print(f"{i} - {c}")
            idx = int(input("Escolha a conta: ")) - 1
            conta = contas[idx]

            valor = float(input("Valor: "))
            descricao = input("Descrição: ")

            categoria = None
            if categorias:
                print("Categorias disponíveis:")
                for i, cat in enumerate(categorias, start=1):
                    print(f"{i} - {cat.nomeCategoria} ({cat.tipo})")
                cat_idx = input("Escolha a categoria (Enter para nenhuma): ")
                if cat_idx:
                    categoria = categorias[int(cat_idx)-1]

            if opcao == "2":
                conta.adicionarReceita(valor, descricao, categoria)
            else:
                conta.adicionarDespesa(valor, descricao, categoria)

        elif opcao == "4":
            if not contas:
                print("Nenhuma conta cadastrada.")
                continue
            for i, c in enumerate(contas, start=1):
                print(f"{i} - {c}")
            idx_conta = int(input("Escolha a conta: ")) - 1
            conta = contas[idx_conta]
            if not conta.transacoes:
                print("Nenhuma transação para editar.")
                continue
            for i, t in enumerate(conta.transacoes, start=1):
                print(f"{i} - {t}")
            idx_trans = int(input("Escolha a transação: ")) - 1
            novo_valor = input("Novo valor (Enter para manter): ")
            nova_desc = input("Nova descrição (Enter para manter): ")
            conta.transacoes[idx_trans].editar(
                float(novo_valor) if novo_valor else None,
                nova_desc if nova_desc else None
            )
            print("Transação editada com sucesso!")

        elif opcao == "5":
            if not contas:
                print("Nenhuma conta cadastrada.")
                continue
            for i, c in enumerate(contas, start=1):
                print(f"{i} - {c}")
            idx = int(input("Escolha a conta: ")) - 1
            contas[idx].mostrarTransacoes()

        elif opcao == "6":
            if not contas:
                print("Nenhuma conta cadastrada.")
                continue
            for i, c in enumerate(contas, start=1):
                print(f"{i} - {c}")
            idx = int(input("Escolha a conta: ")) - 1
            print(f"Saldo da conta: R$ {contas[idx].calcularSaldo():.2f}")

        elif opcao == "7":
            nome = input("Nome da categoria: ")
            tipo = input("Tipo (Receita/Despesa): ")
            categoria = Categoria(nome, tipo)
            categorias.append(categoria)
            categoria.criarCategoria()

        elif opcao == "8":
            if not categorias:
                print("Nenhuma categoria cadastrada.")
                continue
            for i, cat in enumerate(categorias, start=1):
                print(f"{i} - {cat.nomeCategoria} ({cat.tipo})")
            idx = int(input("Escolha a categoria: ")) - 1
            nomeNovo = input("Novo nome: ")
            novoTipo = input("Novo tipo (Receita/Despesa): ")
            categorias[idx].editarCategoria(nomeNovo, novoTipo)

        elif opcao == "9":
            if not categorias:
                print("Nenhuma categoria cadastrada.")
                continue

            for i, cat in enumerate(categorias, start=1):
                print(f"{i} - {cat.nomeCategoria} ({cat.tipo})")

            escolha = input("Digite o número da categoria para excluir (Enter para cancelar): ").strip()
            if not escolha:
                print("Exclusão cancelada.")
                continue

            if escolha.isdigit() and 1 <= int(escolha) <= len(categorias):
                idx = int(escolha) - 1
                cat = categorias[idx]
                if input(f"Excluir '{cat.nomeCategoria}'? (s/n): ").strip().lower() == "s":
                    cat.excluirCategoria()
                    categorias.pop(idx)
                else:
                    print("Exclusão cancelada.")
            else:
                print("Opção inválida.")

        elif opcao == "10":
            if not contas:
                print("Nenhuma conta cadastrada.")
                continue
            for i, conta in enumerate(contas, start=1):
                print(f"{i} - {conta}")
            idx = int(input("Escolha a conta: ")) - 1
            atribuirCategoriaATransacao(contas[idx], categorias)

        elif opcao == "11":
            if not contas:
                print("Nenhuma conta cadastrada, impossível realizar a listagem.")
                continue
            for i, conta in enumerate(contas, start=1):
                print(f"{i} - {conta}")
            idx = int(input("Escolha a conta: ")) - 1
            gastoPorCategoria(contas[idx])

        else:
            print("Opção inválida. Tente novamente.")

        input("Pressione Enter para continuar...")