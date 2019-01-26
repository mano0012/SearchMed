import socket
import medico
import paciente
import hashlib
import pickle

serverIP = "127.0.0.1"
serverPort = 9998

class Cliente:
	def __initi__(self):
		self.sock = None
							 
	def createSocket(self):
		self.sock = socket.socket(socket.AF_INET,
                             socket.SOCK_STREAM)
							 
	def connect(self):
		self.createSocket()
		self.sock.connect((serverIP, serverPort))
		
	def closeSocket(self):
		try:
			self.sock.close()
			self.sock = None
		except:
			pass
	
	def menuPrincipal(self):
		print("==========MENU============")
		print("1 - Login")
		print("2- Cadastro")
		option = int(input("Selecione uma opcao: "))
		
		while (option != 1 and option != 2):
			option = input("Opção invalida, digite novamente: ")
			
		return option
	
	def run(self):
		print("Bem vindo ao SearchMed")
		option = self.menuPrincipal()
		if option == 1:
			msg = self.menuLogin()
			if (msg != False):
				submenuOption = self.loggedFunctions(msg)
				self.enviarMensagem(submenuOption)
				
				msg = self.lerMensagem()
				
				print(msg)
			
		elif option == 2:
			option = self.menuCadastro()
			
			if (option == 1):
				self.cadastraMedico()
			else: self.cadastraPaciente()
			
			
	def loggedFunctions(self, menu):
		print(menu)
		option = int(input("Selecione uma opção: "))
		
		return option
	
	def menuLogin(self):
		print("1 - Paciente")
		print("2 - Medico")
		submenuOption = int(input("Selecione uma opção: "))
		
		if (submenuOption == 1):
			cpf = input("Digite o CPF: ")
			senha = input("Digite a senha: ")
			return self.autenticaUsuario("Paciente", (cpf,senha))
		elif (submenuOption == 2):
			crm = input("Digite o CRM: ")
			senha = input("Digite a senha: ")
			return self.autenticaUsuario("Medico", (crm,senha))
		
	def menuCadastro(self):
		print("Voce deseja cadastrar: ")
		print ("1 - Medico")
		print ("2 - Paciente")
		
		option = int(input("Selecione uma opcao: "))
		
		while (option != 1 and option != 2):
			option = int(input("Opção invalida, digite novamente: "))
			
		return option
		
	def verificaSenha(self, senha, conf):
		if len(senha) < 6 or len(senha) > 14:
			print("A senha deve ter tamanho entre 6 e 14 digitos")
			return -1
		
		if senha != conf:
			print("As senhas devem coincidir")
			return -1
		
		return 0
		
	def cadastraMedico(self):
		doutor = medico.Medico()
		
		doutor.setNome(input("Digite o nome completo do medico: "))
		doutor.setEspecialidade(input("Digite a especialidade: "))
		doutor.setLocal(input("Digite o local de atendimento: "))
		doutor.setCRM(input("Digite o CRM do medico: "))
		doutor.setIdade(input("Digite a idade: "))
		doutor.setEmail(input("Digite o email de contato: "))
		print("Horario de atendimento: ")
		
		inicio = input("Inicio: ")
		fim = input("Fim: ")
		
		doutor.setHorario(int(inicio), int(fim))
		
		senha = input("Digite uma senha: ")
		conf = input("Confirme a senha: ")
		
		while self.verificaSenha(senha,conf) == -1:
			senha = input("Digite novamente a senha: ")
			conf = input("Confirme a senha: ")
		
		self.cadastraUsuario("Medico", doutor)
		
	def cadastraPaciente(self):
		paciente = paciente.Paciente()
		
		paciente.setNome(input("Digite o nome completo: "))
		paciente.setSexo(input("Digite o sexo: "))
		paciente.setCidade(input("Digite a cidade onde o paciente mora: "))
		paciente.setCPF(input("Digite o CPF: "))
		paciente.setIdade(input("Digite a idade do paciente: "))
		paciente.setEmail(input("Digite o email do paciente: "))
	
		senha = input("Digite uma senha: ")
		conf = input("Confirme a senha: ")
		
		while self.verificaSenha(senha,conf) == -1:
			senha = input("Digite novamente a senha: ")
			conf = input("Confirme a senha: ")
		
		self.cadastraUsuario("Paciente", paciente)
	
	def cadastraUsuario(self, tipo, user):
		self.connect()
		
		dados = (tipo, user.createJson())
		
		self.enviarMensagem(("Cadastrar", dados))
		
	def enviarMensagem(self, msg):
		self.sock.send(pickle.dumps(msg))
		
	def lerMensagem(self):
		data, _ = self.sock.recvfrom(1024)
		msg = pickle.loads(data)
		return msg
		
	def autenticaUsuario(self, tipo, credenciais):
		self.connect()
		
		self.enviarMensagem(("Login", (tipo, credenciais)))
		
		msg = self.lerMensagem()
		
		if msg != "ERRO":
			return msg
		else:
			return False
	
	
cliente = Cliente()

cliente.run()