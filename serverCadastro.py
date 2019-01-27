import socket
import threadPool
import json
import pickle
import mysql.connector
import paciente as p
import medico as m

MAX_THREADS = 100
THREAD_BLOCK = 10

IPADDR = "127.0.0.1"
PORT = 9998

class sqlServer:
    def __init__(self):
        self.ipAddress = IPADDR
        self.port = PORT
        self.sock = None

        self.doctorList = list()

        self.threads = threadPool.tPool(self.run, MAX_THREADS, THREAD_BLOCK)

        self.createSocketTCP()

        self.startDB()

        '''
        connector = self.getSqlConnector()

        cursor = connector.cursor()

        cursor.execute("SELECT * FROM LOGIN")

        print(cursor.fetchall())
        '''

        print("SERVER INITIALIZED")

    def startDB(self):
        sqlConnector = mysql.connector.connect(
            host="localhost",
            user="stick",
            passwd="014412"
        )

        cursor = sqlConnector.cursor()


        try:
            cursor.execute("CREATE DATABASE SearchMed")
        except:
            pass

        try:
            cursor.execute("USE SearchMed")
        except:
            pass

        try:
            cursor.execute("CREATE TABLE LOGIN (login VARCHAR(12) PRIMARY KEY NOT NULL, senha VARCHAR(255) NOT NULL)")
        except:
            pass

        try:
            cursor.execute("CREATE TABLE PACIENTE ("
                           "CPF VARCHAR(12) NOT NULL,"
                           "nome VARCHAR(255) NOT NULL,"
                           "idade int,"
                           "sexo VARCHAR(10),"
                           "cidade VARCHAR(255),"
                           "email VARCHAR(255),"
                           "PRIMARY KEY(CPF),"
                           "FOREIGN KEY (CPF) REFERENCES LOGIN(login)"
                           ")")
        except:
            pass

        try:
            cursor.execute("CREATE TABLE MEDICO ("
                           "CRM VARCHAR(12) NOT NULL,"
                           "nome VARCHAR(255) NOT NULL,"
                           "sexo VARCHAR(10),"
                           "especialidade VARCHAR(255),"
                           "local VARCHAR(255),"
                           "idade int,"
                           "email VARCHAR(255) NOT NULL,"
                           "horarioInicio int,"
                           "horarioFim int,"
                           "PRIMARY KEY(CRM),"
                           "FOREIGN KEY (CRM) REFERENCES LOGIN(login)"
                           ")")
        except:
            pass

        try:
            cursor.execute("CREATE TABLE CONSULTAS("
                           "CRM VARCHAR(12) NOT NULL,"
                           "CPF VARCHAR(12) NOT NULL"
                           "dia int NOT NULL,"
                           "hora VARCHAR(10),"
                           "PRIMARY KEY(dia, hora),"
                           "FOREIGN KEY (CRM) REFERENCES MEDICO(CRM),"
                           "FOREIGN KEY (CPF) REFERENCES PACIENTE(CPF)"
                           ")")
        except:
            pass

        sqlConnector.commit()

    def waitClient(self):
        while True:
            con, client = self.sock.accept()

            print("Cliente ", client, " conectado")
            t = self.threads.getThread([con])

            t.start()

    def closeSocket(self):
        self.sock.close()

    def createSocketTCP(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                             socket.SOCK_STREAM)  # TCP

        self.sock.bind((self.ipAddress, self.port))

        self.sock.listen(1)

    def convertJson(self, message):
        try:
            msg = json.dumps(message)
            return msg
        except:
            return message

    def loadJson(self, message):
        try:
            msg = json.loads(message)
            return msg
        except:
            return message

    def loadMessage(self, message):
        return self.loadJson(pickle.loads(message))

    def prepareMsg(self, msg):
        jsonMsg = self.convertJson(msg)

        serializedMsg = pickle.dumps(jsonMsg)

        return serializedMsg

    def getMessage(self, connection):
        serializedMsg = connection.recv(1024)
        msg = self.loadMessage(serializedMsg)
        return msg

    def cadastrarUsuario(self, tipo, connection):
        if tipo == "1":
            user = p.Paciente()
            connection.send(self.prepareMsg("Digite o CPF do paciente: "))
            user.setCPF(self.getMessage(connection))
            connection.send(self.prepareMsg("Digite a cidade do paciente: "))
            user.setCidade(self.getMessage(connection))
        elif tipo == "2":
            user = m.Medico()
            connection.send(self.prepareMsg("Digite o CRM do medico: "))
            user.setCRM(self.getMessage(connection))
            connection.send(self.prepareMsg("Digite a especialidade do medico: "))
            user.setEspecialidade(self.getMessage(connection))
            connection.send(self.prepareMsg("Digite o local de atendimento do medico: "))
            user.setLocal(self.getMessage(connection))

            connection.send(self.prepareMsg("\nHorario de expediente:\n\nInicio: "))
            user.setInicio(self.getMessage(connection))
            connection.send(self.prepareMsg("Fim: "))
            user.setFim(self.getMessage(connection))

        connection.send(self.prepareMsg("Digite o nome: "))
        user.setNome(self.getMessage(connection))
        connection.send(self.prepareMsg("Digite o sexo: "))
        user.setSexo(self.getMessage(connection))
        connection.send(self.prepareMsg("Digite a idade: "))
        user.setIdade(self.getMessage(connection))
        connection.send(self.prepareMsg("Digite o email: "))
        user.setEmail(self.getMessage(connection))

        connection.send(self.prepareMsg("Digite a senha: "))
        senha = self.getMessage(connection)
        connection.send(self.prepareMsg("Confirme a senha: "))
        conf = self.getMessage(connection)


        if (senha == conf):
            self.cadastra(tipo, user, senha)

    def getSqlConnector(self):
        sqlConnector = mysql.connector.connect(
            host="localhost",
            user="stick",
            passwd="014412",
            database="SearchMed"
        )

        return sqlConnector

    def cadastra(self, tipo, user, passwd):
        connector = self.getSqlConnector()
        cursor = connector.cursor()

        if tipo == "1":
            try:
                string = "INSERT INTO LOGIN (login, senha) VALUES (%s, %s)"
                val = (user.CPF, passwd)

                cursor.execute(string, val)

                string = "INSERT INTO PACIENTE(CPF, nome, idade, sexo, cidade, email) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (user.CPF, user.nome, int(user.idade), user.sexo, user.cidade, user.email)
                cursor.execute(string, val)

                connector.commit()
                connector.close()
                return True
            except:
                return False
        elif tipo == "2":
            try:
                string = "INSERT INTO LOGIN (login, senha) VALUES (%s, %s)"
                val = (user.CRM, passwd)
                cursor.execute(string, val)

                string = "INSERT INTO MEDICO(CRM, nome, sexo, especialidade, local, idade, email, horarioInicio, horarioFim) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

                val = (user.CRM, user.nome, user.sexo, user.especialidade, user.local, int(user.idade), user.email,
                       int(user.inicioExpediente), int(user.fimExpediente))

                cursor.execute(string, val)

                connector.commit()
                connector.close()
                return True
            except:
                return False

    def mainMenu(self):
        msg = "Menu\n1 - Login\n2 - Cadastro\n0 - Sair\nSelecione uma opção: "
        return msg

    def autentica(self, tipo, connection):
        connection.send(self.prepareMsg("Digite o CPF ou CRM: "))
        login = self.getMessage(connection)
        connection.send(self.prepareMsg("Digite a senha: "))
        senha = self.getMessage(connection)

        sqlConnector = self.getSqlConnector()
        cursor = sqlConnector.cursor()

        sql = "SELECT login FROM LOGIN where login = %s and senha = %s"
        val = (login, senha)
        cont = 1
        cursor.execute(sql, val)

        results = cursor.fetchall()

        while len(results) != 1:
            cont += 1
            if cont == 4:
                break

            connection.send(self.prepareMsg("\nFalha na autenticação, digite novamente o CPF ou CRM (maximo 3 tentativas): "))
            login = self.getMessage(connection)
            connection.send(self.prepareMsg("Digite a senha: "))
            senha = self.getMessage(connection)

            val = (login, senha)
            cursor.execute(sql, val)
            results = cursor.fetchall()

        if cont < 4:
            if tipo == "1":
                sql = "SELECT * FROM PACIENTE WHERE CPF = " + login
                cursor.execute(sql)
                results = cursor.fetchall()

                paciente = p.Paciente()
                paciente.createPaciente(results[0])
                return paciente
            elif tipo == "2":
                sql = "SELECT * FROM MEDICO WHERE CRM = " + login
                cursor.execute(sql)
                results = cursor.fetchall()

                medico = m.Medico()
                medico.createMedico(results[0])
                return medico
        else:
            #Estourou as tentativas
            connection.send(self.prepareMsg("exit"))
            return None

    def showMenuPaciente(self):
        menu = "1 - Realizar consulta\n2 - Verificar consultas\n0 - Sair\nSelecione uma opção: "
        return menu

    def getMedicos(self):
        connector = self.getSqlConnector()
        cursor = connector.cursor()

        string = "Select nome, especialidade, local from MEDICO"
        cursor.execute(string)

        result = cursor.fetchall()

        return result

    def funcPaciente(self, paciente, connection):

        connection.send(self.prepareMsg(self.showMenuPaciente()))

        option = self.getMessage(connection)

        while(option != "0"):
            if option == "1":
                listaMedicos = self.getMedicos()

                msg = "\nMedicos disponiveis:\n\n"

                if len(listaMedicos) < 1:
                    msg = msg + "Não ha medicos disponiveis\n\n"
                    connection.send(self.prepareMsg(msg + self.showMenuPaciente()))
                    option = self.getMessage(connection)
                else:
                    k = 1
                    for i in listaMedicos:
                        msg = msg + str(k) + ":\n "
                        msg = msg + "Nome: " + i[0] + "\nEspecialidade: " + i[1] + "\nLocal: " + i[2] + "\n\n"

                    msg = msg + "Selecione um medico: "
                    connection.send(self.prepareMsg(msg))
                    medico = self.getMessage(connection)

                    if (int(medico) > len(listaMedicos)):
                        print ("DEU RUIM")
                    else:
                        print("Selecionado: " + listaMedicos[int(medico)][0])

            #elif option == "2":


        connection.send(self.prepareMsg("exit"))

    def run(self, connection):
        msg = self.getMessage(connection)

        if msg == "getServices":
            connection.send(self.prepareMsg(self.mainMenu()))
            msg = self.getMessage(connection)
        else:
            msg = "exit"

        while(msg != "exit"):
            if msg == "0":
                connection.send(self.prepareMsg("exit"))
                msg = "exit"
            elif msg == "1":
                connection.send(self.prepareMsg("1 - Paciente\n2 - Medico\nSelecione uma opção: "))
                tipo = self.getMessage(connection)
                if tipo == "1":
                    paciente = self.autentica(tipo, connection)

                    print(paciente.nome)

                    if paciente is not None:
                        print("ENTROU")
                        self.funcPaciente(paciente, connection)


                elif tipo == "2":
                    medico = self.autentica(tipo, connection)

                    if medico is not None:
                        msg = "exit"
                        connection.send(self.prepareMsg(msg))

                msg = "exit"
                connection.send(self.prepareMsg(msg))
            elif msg == "2":
                connection.send(self.prepareMsg("1 - Cadastrar Paciente\n2 - Cadastrar Medico\nSelecione uma opção: "))
                tipo = self.getMessage(connection)
                self.cadastrarUsuario(tipo, connection)

                connection.send(self.prepareMsg("\nCadastro realizado com sucesso\n\n" + self.mainMenu()))
                msg = self.getMessage(connection)

        self.threads.repopulate()


server = sqlServer()
server.waitClient()