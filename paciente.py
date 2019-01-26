class Paciente:
	def __init__(self):
		self.nome = None
		self.sexo = None
		self.idade = None
		self.cidade = None
		self.email = None
		self.CPF = None
	
	#Dados pessoais
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
		
	def createJson(self):
		output = {
					"nome": self.nome,
					"sexo": self.sexo,
					"idade": self.idade,
					"CPF": self.CPF,
					"idade": self.idade,
					"email": self.email,
					"cidade": self.cidade
				}
		
		return output