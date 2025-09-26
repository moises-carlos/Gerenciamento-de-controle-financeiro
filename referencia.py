from datetime import datetime

# Listas globais para armazenar os objetos (simulando um banco de dados em memória)
eventos = []
participantes = {} # Usamos um dicionário para busca rápida por CPF
inscricoes = []

class Evento:
    """
    Representa um evento com seus dados e métodos para interação com as inscrições.
    """
    def __init__(self, nome, data, local, capacidadeMaxima, descricao):
        self.idEvento = len(eventos) + 1
        self.nome = nome
        self.data = data
        self.local = local
        self.capacidadeMaxima = capacidadeMaxima
        self.descricao = descricao
        print(self)

    def verificarVagas(self):
        """
        Retorna o número de vagas restantes, ignorando inscrições canceladas.
        """
        inscritos_ativos = 0
        for i in inscricoes:
            if i.evento.idEvento == self.idEvento and i.status != 'Cancelada':
                inscritos_ativos += 1
        return self.capacidadeMaxima - inscritos_ativos

    def listarInscricoes(self):
        """
        Retorna uma lista de todas as inscrições para este evento, ignorando inscrições canceladas.
        """
        lista_inscricoes_ativas = []
        for i in inscricoes:
            if i.evento.idEvento == self.idEvento and i.status != 'Cancelada':
                lista_inscricoes_ativas.append(i)
        return lista_inscricoes_ativas

    def __str__(self):
        return f"Evento: {self.nome} (ID: {self.idEvento}) - Vagas: {self.verificarVagas()}/{self.capacidadeMaxima}"

class Participante:
    """
    Representa uma pessoa que pode se inscrever em eventos.
    O CPF é o identificador único.
    """
    def __init__(self, cpf, nome, email, telefone):
        self.idParticipante = cpf
        self.nome = nome
        self.email = email
        self.telefone = telefone
        print(self)

    def listarInscricoes(self):
        """
        Retorna uma lista de todas as inscrições do participante, ignorando as inscrições canceladas.
        """
        lista_inscricoes_ativas = []
        for i in inscricoes:
            if i.participante.idParticipante == self.idParticipante and i.status != 'Cancelada':
                lista_inscricoes_ativas.append(i)
        return lista_inscricoes_ativas
    
    def __str__(self):
        return f"Participante: {self.nome} (CPF: {self.idParticipante})"

class Inscricao:
    """
    Esta classe atua como uma classe de associação entre Evento e Participante,
    registrando a inscrição de um participante em um evento específico.
    """
    def __init__(self, evento, participante):
           # Validação da inscrição
        if evento.verificarVagas() <= 0:
            print(f"Erro: Não há vagas disponíveis para o evento {evento.nome}.")
            return None
        
        # Verifica se o participante já está inscrito, usando for tradicional
        for insc in inscricoes:
            if insc.participante.idParticipante == participante.idParticipante and insc.evento.idEvento == evento.idEvento and insc.status != 'Cancelada':
                print(f"Erro: O participante {participante.nome} já está inscrito no evento {evento.nome}.")
                return None

        self.idInscricao = len(inscricoes) + 1
        self.evento = evento
        self.participante = participante
        self.dataInscricao = datetime.now()
        self.status = 'Pendente'
        print(self)
        self.confirmarInscricao()# Confirmando automaticamente para simplificar
        inscricoes.append(self)

    def confirmarInscricao(self):
        """
        Altera o status da inscrição para 'Confirmada'.
        """
        self.status = 'Confirmada'
        print(self)
        
    def cancelarInscricao(self):
        """
        Altera o status da inscrição para 'Cancelada'.
        """
        self.status = 'Cancelada'
        print(self)
    
    def obterDetalhes(self):
        """
        Retorna detalhes sobre a inscrição.
        """
        return {
            "idInscricao": self.idInscricao,
            "evento": self.evento.nome,
            "participante": self.participante.nome,
            "data": self.dataInscricao.strftime('%d/%m/%Y %H:%M'),
            "status": self.status
        }

    def __str__(self):
        return f"Inscrição ID: {self.idInscricao} | Evento: {self.evento.nome} | Participante: {self.participante.nome} | Status: {self.status}"

# --- Simulação do Sistema ---

print("Criando eventos e os salvando na lista global")
evento1 = Evento("Hackathon 2025", datetime(2025, 10, 20, 9, 0), "Centro de Convenções", 3, "Competição de programação de 24 horas.")
eventos.append(evento1)
evento2 = Evento("Palestra de IA", datetime(2025, 11, 5, 18, 30), "Auditório Principal", 2, "Palestra sobre as últimas tendências em inteligência artificial.")
eventos.append(evento2)
evento3 = Evento("Workshop de Python", datetime(2025, 12, 1, 14, 0), "Sala de Treinamento", 10, "Workshop prático sobre desenvolvimento web com Python.")
eventos.append(evento3)

print("\n\nCriando participantes e os salvando na lista global")
participante1 = Participante("111.222.333-44", "Ana Silva", "ana.silva@email.com", "99111-2222")
participante2 = Participante("555.666.777-88", "Bruno Costa", "bruno.c@email.com", "99333-4444")
participante3 = Participante("999.888.777-66", "Carla Souza", "carla.s@email.com", "99555-6666")
participante4 = Participante("444.333.222-11", "Diego Mendes", "diego.m@email.com", "99777-8888")
participante5 = Participante("000.111.222-33", "Elisa Gomes", "elisa.g@email.com", "99999-0000")
for p in [participante1, participante2, participante3, participante4, participante5]:
     participantes[p.idParticipante] = p

print("\n\n--- Realizando Inscrições ---")

# Inscrições para o Hackathon (capacidade 3)
Inscricao(evento1, participante1)
Inscricao(evento1, participante2)
Inscricao(evento1, participante3)
Inscricao(evento1, participante4) # Deve falhar
print(f"\nEstão inscritos no {evento1}:")
for i in evento1.listarInscricoes():
    print(f" - {i}")

print("\n\n"+"-" * 25)

# Inscrições para a Palestra de IA (capacidade 2)
print(evento2)
Inscricao(evento2, participante1)
Inscricao(evento2, participante5)
print(f"Estão inscritos no {evento2}:")
for i in evento2.listarInscricoes():
    print(f" - {i}")

print("\n\n"+"-" * 25)


# Inscrição para o Workshop de Python
print(evento3)
Inscricao(evento3, participante2)
Inscricao(evento3, participante2) # Tentativa duplicada
print(f"\nEstão inscritos no {evento3}:")
for i in evento3.listarInscricoes():
    print(f" - {i}")


# Verificando o estado do sistema
print("\n\n--- Verificação do Sistema ---")

print(f"Eventos em que '{participante1.nome}' está inscrito:")
eventosPart1 = participante1.listarInscricoes()
for e in eventosPart1:
    print(f"- {e}")

print()
eventosPart1[0].cancelarInscricao()


print(f"\nEventos em que '{participante1.nome}' está inscrito:")
eventosPart1 = participante1.listarInscricoes()
for e in eventosPart1:
    print(f"- {e}")
    
print("\n\n--- Estado Final do Sistema: ---")
for e in eventos:
    print(e)
print()

for e in participantes:
    print(participantes[e])
print()

for e in inscricoes:
    print(e)
print()




