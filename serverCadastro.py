import pickle
import json
import socket
import medico
import threading

IP = "127.0.0.1"
PORT = 9998

class Server:
	def __init__(self):
		self.listaMedicos = list()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.sock.bind((IP, PORT))
		
		self.sock.listen()
		
	def loadMessage(self, message):
		return self.loadJson(pickle.loads(message))
	
	def getMessage(self, connection):
		serializedMsg = connection.recv(1024)
		print(pickle.loads(serializedMsg))
        
		#return acao, dados
	
	def run(self):
		while(True):
			con, client = self.sock.accept()
			
			t = threading.Thread(target=self.mainMenu, args = [con])
			t.start()
		
	def mainMenu(self, con):
		msg = con.recv(1024)
		acao, dados = pickle.loads(msg)
		
		if acao == "Cadastrar":
			tipo = dados[0]
			
			if (tipo == "Medico"):
				user = medico.Medico()
				x = json.loads(dados[1][0])
				
				user.nome = dados[1]["nome"]
				user.especialidade = dados[1]["especialidade"]
				user.local = dados[1]["local"]
				user.CRM = dados[1]["CRM"]
				user.idade = dados[1]["idade"]
				user.email = dados[1]["email"]
				user.agenda.setInicio = dados[1]["inicio"]
				user.agenda.setFim = dados[1]["fim"]
				
			elif (tipo == "Paciente"):
				user = paciente.Paciente()
				
				user.nome = dados[1]["nome"]
				user.sexo = dados[1]["sexo"]
				user.cidade = dados[1]["cidade"]
				user.CPF = dados[1]["CPF"]
				user.idade = dados[1]["idade"]
				user.email = dados[1]["email"]
			
			self.cadastra(tipo, user)
		elif acao == "Login":
			if(dados[0] == "Paciente"):
				if dados[1][0] == "teste" and dados[1][1] == "123456":
					print("Autenticado")
					con.send(pickle.dumps(self.menuPaciente()))
					msg = int(pickle.loads(con.recv(1024)))
					
					if msg == 1:
						self.enviarListaMedicos(con)
				else:
					con.send(pickle.dumps("ERRO"))
			elif dados[0] == "Medico":
				if dados[1][0] == "teste" and dados[1][1] == "123456":
					print("Autenticado")
					con.send(pickle.dumps(self.menuMedico()))
				else:
					con.send(pickle.dumps("ERRO"))
				
	def menuPaciente(self):
		return ("1 - Marcar horario")
		
	def menuMedico(self):
		print("1 - Consultar agenda")
		
	def enviarListaMedicos(self):
		msg = "Medicos disponiveis:\n"
		k = 1
		for i in self.listaMedicos:
			msg = msg + k + " - " + i.nome + "\n"
			k += 1
		
		con.send(pickle.dumps(msg))
		
	def cadastra(self, tipo, user):
		if tipo == "Paciente":
			pass
		elif tipo == "Medico":
			self.listaMedicos.append(user)
		
server = Server()

server.run()