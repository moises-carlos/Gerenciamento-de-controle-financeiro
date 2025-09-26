from datetime import datetime

titulo1 = "MENU FINANCEIRO"
titulo2 = "SUAS TRANSAÇÕES"

def mostrarTitulo(texto, largura=100):
    print("-" * largura)
    print("|" + texto.center(largura - 2) + "|")
    print("-" * largura)

def mostrarOpcao(texto, largura=100):
    print("| " + texto.ljust(largura - 3) + "|")

def mostrarLinha(texto, largura=100):
    """Imprime qualquer linha de texto formatada no padrão da caixa."""
    print("| " + texto.ljust(largura - 3) + "|")


class Conta:
    def __init__(self,nome, cpf,  saldo, tipo_conta, data_criacao = None):
        idConta = cpf
        self.nome = nome
        self._saldo = saldo
        self.tipo_conta = tipo_conta
        self.data_criacao = data_criacao
    
    def adicionarReceita(self, valor, descricao):
        if valor > 0:
            self._saldo += valor
            print(f"Receita de R$ {valor:.2f} adicionada. Saldo atual: R$ {self._saldo:.2f}")
        else:
            print("Valor inválido para receita.")
    
    
    def adicionarDespesa(self, valor):
        if valor > 0:
            if valor <= self._saldo:
                self._saldo -= valor
                print(f"Despesa de R$ {valor:.2f} registrada. Saldo atual: R$ {self._saldo:.2f}")
            else:
                print("Saldo insuficiente para essa despesa.")
        else:
            print("Valor inválido para despesa.")
    
    def transferir(self, valor, conta_destino):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            conta_destino.adicionarReceita(valor, descricao=f"Transferência de {self.nome}")
            print(f"Transferência de R$ {valor:.2f} para {conta_destino.nome} realizada com sucesso.")
        else:
            print("Saldo insuficiente ou valor inválido para transferência.")
    
    def calcularSaldo(self):
        return self._saldo
    
    def __str__(self):
        return (f"Conta: {self.nome} | Tipo: {self.tipo_conta} | "
                f"Saldo: R$ {self._saldo:.2f} | Criada em: {self.data_criacao.strftime('%d/%m/%Y')}")
    
    


class Transacao:
    contadorIdTransação = 1
 
    def __init__(self, valor=0.0, descricao="", data=None):
        self.id = Transacao.contadorIdTransação
        Transacao.contadorIdTransação += 1

        self.valor = valor
        self.descricao = descricao
        self.data = data if data else datetime.now()
        self.recorrente = False

    def editar(self, novoValor=None, novaDescricao=None):
        if novoValor is not None:
            self.valor = novoValor
        if novaDescricao is not None:
            self.descricao = novaDescricao

    def marcarComoRecorrente(self):
        self.recorrente = True

    def __str__(self):
        recorrente_str = " (Recorrente)" if self.recorrente else ""
        return (f"ID: {self.id} | Valor: R$ {self.valor:.2f} | "
                f"Data: {self.data.strftime('%d/%m/%Y')} | "
                f"Descrição: {self.descricao}{recorrente_str}")



""" 
def mostrarTransacoes(listaDeTransacoes, largura=100):
    mostrarTitulo(titulo2, largura)
    if not listaDeTransacoes:
        mostrarLinha("Nenhuma transação encontrada.", largura)
        print("-" * largura)
        return
    for i in listaDeTransacoes:
        mostrarLinha(str(i), largura)
    print("-" * largura)


def mostrar_menu_opcoes():
    mostrarTitulo(titulo1)
    mostrarOpcao("1 - Adicionar uma nova transação", 100)
    mostrarOpcao("2 - Editar uma transação", 100)
    mostrarOpcao("3 - Marcar uma transação como recorrente", 100)
    mostrarOpcao("4 - Apagar uma transação", 100)
    mostrarOpcao("5 - Ver todas as transações", 100)
    mostrarOpcao("6 - Sair", 100)
    print("-" * 100)

def menu():
    minhasTransacoes = []

    while True:
        mostrar_menu_opcoes()

        escolha = input("O que você quer fazer? Digite o número: ")

        if escolha == "1":
            try:
                valor = float(input("Qual o valor da transação? "))
                descricao = input("Qual a descrição (ex: 'Almoço', 'Mercado')? ")
                novaTransacao = Transacao(valor, descricao)
                minhasTransacoes.append(novaTransacao)
                print(f"Transação adicionada! ID: {novaTransacao.id}\n")
            except ValueError:
                print("Valor inválido. Tente novamente.\n")

        elif escolha == "2":
            mostrarTransacoes(minhasTransacoes)
            try:
                idParaEditar = int(input("Qual o ID da transação que você quer editar? "))
                transacaoEncontrada = next((i for i in minhasTransacoes if i.id == idParaEditar), None)
                if transacaoEncontrada:
                    novoValor = input("Novo valor (deixe em branco para não mudar): ")
                    novaDescricao = input("Nova descrição (deixe em branco para não mudar): ")
                    
                    transacaoEncontrada.editar(
                        novoValor = float(novoValor) if novoValor else None,
                        novaDescricao = novaDescricao if novaDescricao else None
                    )
                    
                    print("Transação atualizada!\n")
                else:
                    print("Transação não encontrada.\n")
            except (ValueError, IndexError):
                print("ID inválido,tente novamente.\n")

        elif escolha == "3":
            mostrarTransacoes(minhasTransacoes)
            try:
                marcarId = int(input("Qual o ID da transação para marcar como recorrente? "))
                transacaoEncontrada = next((i for i in minhasTransacoes if i.id == marcarId), None)
                if transacaoEncontrada:
                    transacaoEncontrada.marcarComoRecorrente()
                    print("Transação marcada como recorrente!\n")
                else:
                    print("Transação não encontrada.\n")
            except ValueError:
                print("ID inválido.\n")

        elif escolha == "4":
            mostrarTransacoes(minhasTransacoes)
            try:
                apagarId = int(input("Qual o ID da transação que você quer apagar? "))
                transacaoEncontrada = next((i for i in minhasTransacoes if i.id == apagarId), None)
                if transacaoEncontrada:
                    minhasTransacoes.remove(transacaoEncontrada)
                    print("Transação apagada!\n")
                else:
                    print("Transação não encontrada.\n")
            except ValueError:
                print("ID inválido, tente novamente")

        elif escolha == "5":
            mostrarTransacoes(minhasTransacoes)

        elif escolha == "6":
            print("Até mais, tchau tchau!")
            break

        else:
            print("Opção inválida. Por favor, tente de novo.\n")
"""

if __name__ == "__main__":
    
    conta1 = Conta(nome="Alice", cpf="12345678900", saldo=1000.0, tipo_conta="Corrente", data_criacao=datetime.now())
    conta2 = Conta(nome="Bob", cpf="98765432100", saldo=500.0, tipo_conta="Poupança", data_criacao=datetime.now())

    
    print(conta1)
    print(conta2)
    print("-" * 50)

   
    conta1.adicionarReceita(200.0, "Salario")
    conta1.adicionarDespesa(150.0)
    print("-" * 50)

  
    conta1.transferir(100.0, conta2)
    print("-" * 50)

    
    print(f"Saldo final {conta1.nome}: R$ {conta1.calcularSaldo():.2f}")
    print(f"Saldo final {conta2.nome}: R$ {conta2.calcularSaldo():.2f}")
    print("-" * 50)

    t1 = Transacao(valor=200, descricao="Salário")
    t2 = Transacao(valor=50, descricao="Supermercado")
    t3 = Transacao(valor=100, descricao="Transferência")

    
    print("Transações realizadas:")
    print(t1)
    print(t2)
    print(t3)

   
    t2.editar(novoValor=60, novaDescricao="Supermercado atualizado")
    print("\nTransação editada:")
    print(t2)

    
    t1.marcarComoRecorrente()
    print("\nTransação recorrente:")
    print(t1)