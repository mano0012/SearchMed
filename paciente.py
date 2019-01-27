class Paciente:
    def __init__(self):
        self.nome = None
        self.sexo = None
        self.idade = None
        self.cidade = None
        self.email = None
        self.CPF = None

    # Dados pessoais
    def setNome(self, nome):
        self.nome = nome

    def setSexo(self, sexo):
        self.sexo = sexo

    def setCidade(self, cidade):
        self.cidade = cidade

    def setCPF(self, CPF):
        self.CPF = CPF

    def setIdade(self, idade):
        self.idade = idade

    def setEmail(self, email):
        self.email = email

    def createPaciente(self, dados):
        self.setCPF(dados[0])
        self.setNome(dados[1])
        self.setIdade(dados[2])
        self.setSexo(dados[3])
        self.setCidade(dados[4])
        self.setEmail(dados[5])

    def printDados(self):
        print(self.nome)
        print(self.sexo)
