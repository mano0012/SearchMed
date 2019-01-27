class Medico:
    def __init__(self):
        self.nome = None
        self.sexo = None
        self.especialidade = None
        self.local = None
        self.CRM = None
        self.idade = None
        self.email = None
        self.inicioExpediente = None
        self.fimExpediente = None
        self.convenio = None

    #Dados pessoais
    def setNome(self, nome):
        self.nome = nome

    def setSexo(self, sexo):
        self.sexo = sexo

    def setConvenio(self, convenio):
        self.convenio = convenio

    def setEspecialidade(self, especialidade):
        self.especialidade = especialidade

    def setLocal(self, local):
        self.local = local

    def setCRM(self, CRM):
        self.CRM = CRM

    def setIdade(self, idade):
        self.idade = idade

    def setEmail(self, email):
        self.email = email

    def createMedico(self, dados):
        self.setCRM(dados[0])
        self.setNome(dados[1])
        self.setSexo(dados[2])
        self.setEspecialidade(dados[3])
        self.setLocal(dados[4])
        self.setIdade(dados[5])
        self.setEmail(dados[6])
        self.setInicio(dados[7])
        self.setFim(dados[8])
        self.setConvenio(dados[9])

    #Agenda
    def setInicio(self, inicio):
        self.inicioExpediente = inicio

    def setFim(self, fim):
        self.fimExpediente = fim

    def getAgenda(self):
        agenda = list()
        for i in range(self.inicioExpediente,self.fimExpediente, 1):
            agenda.append(i)

        return agenda

