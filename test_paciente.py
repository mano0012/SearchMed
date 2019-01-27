import unittest
import paciente

class TestPaciente(unittest.TestCase):
	def setUP(self):
		self.pac = None

	def test_tamanho_cpf_valido(self):
		self.pac = paciente.Paciente()
		self.pac.setCPF('77604634052')
		self.assertEqual(len(self.pac.CPF), 11, 'CPF deve ter 11 caracteres')

	def test_tamanho_cpf_invalido(self):
		self.pac = paciente.Paciente()
		self.pac.setCPF('1234567890')
		self.assertNotEqual(len(self.pac.CPF), 11, 'CPF deve ter 11 caracteres')
		self.pac.setCPF('1234567891011')
		self.assertNotEqual(len(self.pac.CPF), 11, 'CPF deve ter 11 caracteres')

	def test_email(self):
		REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
		self.pac = paciente.Paciente()
		self.pac.setEmail('exemplo@email.com')
		self.assertRegex(self.pac.email, REGEX, 'email valido deve ser aceito')
		self.pac.setEmail('exemplo.email.com')
		self.assertNotRegex(self.pac.email, REGEX, 'email invalido')

if __name__ == '__main__':
	unittest.main()
