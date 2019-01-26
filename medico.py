import horarios

class Medico:
	def __init__(self):
		self.nome = None
		self.especialidade = None
		self.local = None
		self.CRM = None
		self.idade = None
		self.email = None
		self.agenda = horarios.Agenda()
	
	#Dados pessoais
	def setNome(self, nome):
		self.nome = nome
	
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
	
	#Agenda
	def setHorario(self, inicio, fim):
		self.agenda.setInicio(inicio)
		self.agenda.setFim(fim)
		
	def createJson(self):
		output = [
				{
					"nome": self.nome,
					"especialidade": self.especialidade,
					"local": self.local,
					"CRM": self.CRM,
					"idade": self.idade,
					"email": self.email,
					"inicio": self.agenda.getInicio(),
					"fim": self.agenda.getFim()
				}
        ]
		
		return output