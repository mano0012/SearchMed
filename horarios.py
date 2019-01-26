class Agenda:
	def __init__(self):
		self.inicio = None
		self.fim = None
		self.horariosLivres = list() * 31
	
	def setInicio(self, inicio):
		self.inicio = inicio
	
	def getInicio(self):
		return self.inicio
		
	def getFim(self):
		return self.fim
	
	def setFim(self, fim):
		self.fim = fim
	
	def getHorariosLivres(self, dia):
		return self.horariosLivre[dia]
		
	def criaHorariosAgenda(self):
		for i in range(31):
			for j in range(inicio, fim, 1):
				self.horariosLivres[i].append(j)
	
	def selectHorario(self, dia, hora):
		self.horariosLivres[dia].remove(hora)

	def setDuracao(self, duracao):
		self.duracaoConsulta = duracao