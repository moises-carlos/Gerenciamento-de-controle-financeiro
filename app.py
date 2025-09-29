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
    def __init__(self, nome, cpf, saldo, tipo_conta, data_criacao=None):
        self.idConta = cpf
        self.nome = nome
        self._saldo = saldo
        self.tipo_conta = tipo_conta
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)
    
    def adicionarReceita(self, valor, descricao, categoria=None):
        if valor > 0:
            self._saldo += valor
            transacao = Transacao(valor, descricao, categoria)
            self.adicionar_transacao(transacao)
            print(f"Receita de R$ {valor:.2f} adicionada. Saldo atual: R$ {self._saldo:.2f}")
        else:
            print("Valor inválido para receita.")
    
    def adicionarDespesa(self, valor, descricao, categoria=None):
        if valor > 0:
            if valor <= self._saldo:
                self._saldo -= valor
                transacao = Transacao(-valor, descricao, categoria)
                self.adicionar_transacao(transacao)
                print(f"Despesa de R$ {valor:.2f} registrada. Saldo atual: R$ {self._saldo:.2f}")
            else:
                print("Saldo insuficiente para essa despesa.")
        else:
            print("Valor inválido para despesa.")

    def mostrar_transacoes(self):
        print(f"Transações da conta de {self.nome}:")
        for transacao in self.transacoes:
            print(transacao)
    
    def calcularSaldo(self):
        return self._saldo
    
    def __str__(self):
        return (f"Conta: {self.nome} | Tipo: {self.tipo_conta} | "
                f"Saldo: R$ {self._saldo:.2f}")


class Transacao:
    contadorIdTransação = 1

    def __init__(self, valor=0.0, descricao="", categoria=None):
        self.id = Transacao.contadorIdTransação
        Transacao.contadorIdTransação += 1
        self.valor = valor
        self.descricao = descricao
        self.categoria = categoria

    @classmethod
    def criarTransacao(cls, valor, descricao):
        return cls(valor, descricao)

    def editar(self, novoValor=None, novaDescricao=None):
        if novoValor is not None:
            self.valor = novoValor
        if novaDescricao is not None:
            self.descricao = novaDescricao
    
    @staticmethod
    def mostrarTransacoes(listaDeTransacoes, largura=100):
        mostrarTitulo(titulo2, largura)
        if not listaDeTransacoes:
            mostrarLinha("Nenhuma transação encontrada.", largura)
            print("-" * largura)
            return
        for i in listaDeTransacoes:
            mostrarLinha(str(i), largura)
        print("-" * largura)

    def __str__(self):
        categoria_str = self.categoria.nomeCategoria if self.categoria else "Sem categoria"
        return (f"ID: {self.id} | Valor: R$ {self.valor:.2f} | "
                f"Descrição: {self.descricao} | Categoria: {categoria_str}")

 
class Categoria:
    contadorIdCategoria= 1
    def __init__(self, nomeCategoria, tipo):
        self.idCategoria = Categoria.contadorIdCategoria
        Categoria.contadorIdCategoria += 1
        self.nomeCategoria = nomeCategoria
        self.tipo = tipo

    def criar_categoria(self):
        print(f"Categoria: ID:{self.idCategoria}, Nome: {self.nomeCategoria}, Tipo: {self.tipo}")

    def editar_categoria(self, nomeNovo, novoTipo):
        self.nomeCategoria = nomeNovo
        self.tipo = novoTipo
        print(f"Nova Categoria: Nome {self.nomeCategoria}, Tipo: {self.tipo}")

    def excluirCategoria(self):
        print(f"Categoria Excluida: {self.nomeCategoria} excluida")
        





if __name__ == "__main__":