import unittest
import paciente

class TestPaciente(unittest.TestCase):
	def setUP(self):
		self.pac = None

	def test_nome(self):
		self.pac = paciente.Paciente()
		self.pac.setNome('Joao')
		self.assertIsNot(self.pac.nome, '', 'nome não dever ser vazio')

	def test_sexo(self):
		self.pac = paciente.Paciente()
		self.pac.setSexo('m')
		self.assertIn(self.pac.sexo, ['m', 'f'], 'sexo m deve ser valido')
		self.pac.setSexo('f')
		self.assertIn(self.pac.sexo, ['m', 'f'], 'sexo f deve ser valido')
		self.pac.setSexo('x')
		self.assertNotIn(self.pac.sexo, ['m', 'f'], 'sexo deve ser m ou f')

	def test_idade(self):
		self.pac = paciente.Paciente()
		self.pac.setIdade(30)
		self.assertGreater(self.pac.idade, 0, 'idade deve ser maior que 0')

	def test_cidade(self):
		self.pac = paciente.Paciente()
		self.pac.setCidade('Goiania')
		self.assertIsNot(self.pac.cidade, '', 'cidade não dever ser vazio')

	def test_email(self):
		REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
		self.pac = paciente.Paciente()
		self.pac.setEmail('exemplo@email.com')
		self.assertRegex(self.pac.email, REGEX, 'email valido deve ser aceito')
		self.pac.setEmail('exemplo.email.com')
		self.assertNotRegex(self.pac.email, REGEX, 'email invalido')

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

if __name__ == '__main__':
	unittest.main()
