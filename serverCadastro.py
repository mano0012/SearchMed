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

        cursor.execute("DESCRIBE CONSULTAS")

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
            #cursor.execute("DROP DATABASE SearchMed")
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
                           "convenio VARCHAR(10),"
                           "PRIMARY KEY(CRM),"
                           "FOREIGN KEY (CRM) REFERENCES LOGIN(login)"
                           ")")
        except:
            pass

        try:
            cursor.execute("CREATE TABLE CONSULTAS("
                           "CRM VARCHAR(12) NOT NULL,"
                           "CPF VARCHAR(12) NOT NULL,"
                           "dia int NOT NULL,"
                           "hora VARCHAR(10) NOT NULL,"
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
            connection.send(self.prepareMsg("Digite a cidade de atendimento do medico: "))
            user.setLocal(self.getMessage(connection))
            connection.send(self.prepareMsg("Digite o convenio em que o medico atende: "))
            user.setConvenio(self.getMessage(connection))

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

        while (senha != conf or len(senha) < 6):
            connection.send(self.prepareMsg("Senha invalida, digite novamente: "))
            senha = self.getMessage(connection)
            connection.send(self.prepareMsg("Confirme a senha: "))
            conf = self.getMessage(connection)

        return self.cadastra(tipo, user, senha)

    def getSqlConnector(self):
        sqlConnector = mysql.connector.connect(
            host="localhost",
            user="stick",
            passwd="014412",
            database="SearchMed"
        )

        return sqlConnector

    def cadastra(self, tipo, user, passwd):
        if tipo == "1":
            try:
                val = (user.CPF, passwd)
                self.realizaInsercaoSQL("INSERT INTO LOGIN (login, senha) VALUES (%s, %s)", val)

                val = (user.CPF, user.nome, int(user.idade), user.sexo, user.cidade, user.email)
                self.realizaInsercaoSQL("INSERT INTO PACIENTE(CPF, nome, idade, sexo, cidade, email) VALUES (%s, %s, %s, %s, %s, %s)", val)

                return True
            except:
                return False
        elif tipo == "2":
            try:
                val = (user.CRM, passwd)
                self.realizaInsercaoSQL("INSERT INTO LOGIN (login, senha) VALUES (%s, %s)", val)

                val = (user.CRM, user.nome, user.sexo, user.especialidade, user.local, int(user.idade), user.email,
                       int(user.inicioExpediente), int(user.fimExpediente), user.convenio)

                self.realizaInsercaoSQL("INSERT INTO MEDICO(CRM, nome, sexo, especialidade, local, idade, email, horarioInicio, horarioFim, convenio) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", val)

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

        cont = 1

        val = (login, senha)
        results = self.realizaConsultaSQL("SELECT login FROM LOGIN where login = %s and senha = %s", val)

        while len(results) != 1:
            cont += 1
            if cont == 4:
                break

            connection.send(self.prepareMsg("\nFalha na autenticação, digite novamente o CPF ou CRM (maximo 3 tentativas): "))
            login = self.getMessage(connection)
            connection.send(self.prepareMsg("Digite a senha: "))
            senha = self.getMessage(connection)

            val = (login, senha)
            results = self.realizaConsultaSQL("SELECT login FROM LOGIN where login = %s and senha = %s", val)

        if cont < 4:
            if tipo == "1":
                results = self.realizaConsultaSQL("SELECT * FROM PACIENTE WHERE CPF = " + login)

                paciente = p.Paciente()
                paciente.createPaciente(results[0])
                return paciente
            elif tipo == "2":
                results = self.realizaConsultaSQL("SELECT * FROM MEDICO WHERE CRM = " + login)

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

    def getMedicos(self, cidade, especialidade):
        result = self.realizaConsultaSQL("Select * from MEDICO where local = %s and especialidade = %s", (cidade, especialidade))

        return result

    def realizaConsultaSQL(self, querry, vars = None):
        connector = self.getSqlConnector()
        cursor = connector.cursor()

        if vars is not None:
            cursor.execute(querry, vars)
        else:
            cursor.execute(querry)

        results = cursor.fetchall()

        connector.close()

        return results

    def realizaInsercaoSQL(self, querry, vars = None):
        connector = self.getSqlConnector()
        cursor = connector.cursor()

        try:
            cursor.execute(querry, vars)

            connector.commit()

            connector.close()
            return True
        except e:
            print(e)
            return False

    def alteraLocalizacao(self, medico, novaLocalizacao):
        return self.realizaInsercaoSQL("UPDATE MEDICO SET local = %s WHERE CRM = %s", (novaLocalizacao, medico))

    def horariosDisponiveis(self, medico, dia):
        agenda = medico.getAgenda()

        results = self.realizaConsultaSQL("Select * from CONSULTAS WHERE CRM = %s and dia = %s", (medico.CRM, int(dia)))

        for i in results:
            agenda.remove(int(i[3]))

        return agenda

    def addConsulta(self, medico, paciente, dia, horario):
        return self.realizaInsercaoSQL("INSERT INTO CONSULTAS(CRM,CPF,dia,hora) VALUES (%s,%s,%s,%s)", (medico, paciente, int(dia), horario))

    def getConsultasPaciente(self, paciente):
        return self.realizaConsultaSQL("SELECT * FROM CONSULTAS WHERE CPF = " + paciente + " ORDER BY dia")

    def getConsultasMedico(self, medico):
        return self.realizaConsultaSQL("SELECT * FROM CONSULTAS WHERE CRM = " + medico + " ORDER BY dia")


    def funcPaciente(self, paciente, connection):
        connection.send(self.prepareMsg(self.showMenuPaciente()))

        option = self.getMessage(connection)

        while(option != "0"):
            if option == "1":
                connection.send(self.prepareMsg("Digite a cidade de interesse: "))
                cidade = self.getMessage(connection)

                connection.send(self.prepareMsg("Digite a especialidade: "))
                especialidade = self.getMessage(connection)

                listaMedicos = self.getMedicos(cidade, especialidade)

                msg = "\nMedicos disponiveis:\n\n"

                if len(listaMedicos) < 1:
                    msg = msg + "Não ha medicos disponiveis\n\n"
                else:
                    k = 1
                    for i in listaMedicos:
                        msg = msg + str(k) + ":\n"
                        msg = msg + "Nome: " + i[1] + "\nEspecialidade: " + i[3] + "\nLocal: " + i[4] + "\nConvenio: " + i[9] + "\n\n"
                        k+=1

                    msg = msg + "Selecione um medico: "
                    connection.send(self.prepareMsg(msg))
                    medicoIndex = self.getMessage(connection)

                    if (int(medicoIndex) > len(listaMedicos)):
                        msg = "Medico inválido\n\n"
                    else:
                        medico = m.Medico()
                        medico.createMedico(listaMedicos[int(medicoIndex) - 1])

                        connection.send(self.prepareMsg("Digite o dia da consulta: "))
                        dia = self.getMessage(connection)

                        agenda = self.horariosDisponiveis(medico, dia)

                        msg = "Horarios Disponiveis:\n"

                        if len(agenda) < 1:
                            msg += "Não há horarios disponiveis para este dia\n\n"
                        else:
                            for i in range(len(agenda)):
                                msg += str(agenda[i]) + "\n"

                            msg += "Selecione um horario: "
                            connection.send(self.prepareMsg(msg))
                            horario = self.getMessage(connection)

                            if self.addConsulta(medico.CRM, paciente.CPF, dia, horario):
                                msg = "Consulta marcada com sucesso\n\n"
                            else:
                                msg = "Nao foi possivel marcar a consulta\n\n"
            elif option == "2":
                msg = "Consultas Marcadas:\n\n"
                result = self.getConsultasPaciente(paciente.CPF)

                if len(result) < 1:
                    msg += "Não há consultas marcadas\n\n"
                else:
                    for i in result:
                        dadosMedico = self.realizaConsultaSQL("Select nome, local, convenio FROM MEDICO where CRM = " + i[0])
                        print(dadosMedico[0])
                        msg += "Medico: " + dadosMedico[0][0] + "\nDia: " + str(i[2]) + "\nHorario: " + i[3] + "\nLocal: " + dadosMedico[0][1] + "\nConvenio: " + dadosMedico[0][2] + "\n\n"

            connection.send(self.prepareMsg(msg + self.showMenuPaciente()))
            option = self.getMessage(connection)

        connection.send(self.prepareMsg("exit"))

    def showMenuMedico(self):
        return "1 - Consultar agenda\n2 - Alterar cidade\n0 - Sair\nSelecione uma opção: "

    def funcMedico(self, medico, connection):
        connection.send(self.prepareMsg(self.showMenuMedico()))

        option = self.getMessage(connection)

        while(option != "0"):
            if option == "1":
                msg = "Agenda:\n\n"
                result = self.getConsultasMedico(medico.CRM)

                print(result)

                for i in result:
                    dadosConsulta = self.realizaConsultaSQL("Select nome FROM PACIENTE where CPF = " + i[1])
                    msg += "Paciente: " + dadosConsulta[0][0] + "\nDia: " + str(i[2]) + "\nHorario: " + i[
                        3] + "\n\n"

            elif option == "2":
                connection.send(self.prepareMsg("Digite a nova localização: "))
                local = self.getMessage(connection)
                if self.alteraLocalizacao(medico.CRM, local):
                    msg = "Alteração feita com sucesso\n\n"
                else:
                    msg = "Não foi possivel fazer a alteração\n\n"

            connection.send(self.prepareMsg(msg + self.showMenuMedico()))
            option = self.getMessage(connection)

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

                    if paciente is not None:
                        self.funcPaciente(paciente, connection)

                elif tipo == "2":
                    medico = self.autentica(tipo, connection)

                    if medico is not None:
                        self.funcMedico(medico, connection)

                msg = "exit"
            elif msg == "2":
                connection.send(self.prepareMsg("1 - Cadastrar Paciente\n2 - Cadastrar Medico\nSelecione uma opção: "))
                tipo = self.getMessage(connection)
                if self.cadastrarUsuario(tipo, connection):
                    connection.send(self.prepareMsg("\nCadastro realizado com sucesso\n\n" + self.mainMenu()))
                    msg = self.getMessage(connection)
                else:
                    connection.send(self.prepareMsg("\nNão foi possivel cadastrar\n\n" + self.mainMenu()))
                    msg = self.getMessage(connection)

        self.threads.repopulate()


server = sqlServer()
server.waitClient()