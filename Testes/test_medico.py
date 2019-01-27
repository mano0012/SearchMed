import unittest
import medico

class TestPaciente(unittest.TestCase):
	def setUP(self):
		self.med = None

	def test_nome(self):
		self.med = medico.Medico()
		self.med.setNome('Joao')
		self.assertIsNot(self.med.nome, '', 'nome não dever ser vazio')

	def test_sexo(self):
		self.med = medico.Medico()
		self.med.setSexo('m')
		self.assertIn(self.med.sexo, ['m', 'f'], 'sexo m deve ser valido')
		self.med.setSexo('f')
		self.assertIn(self.med.sexo, ['m', 'f'], 'sexo f deve ser valido')
		self.med.setSexo('x')
		self.assertNotIn(self.med.sexo, ['m', 'f'], 'sexo deve ser m ou f')

	def test_especialidade(self):
		self.med = medico.Medico()
		self.med.setEspecialidade('Oncologia')
		self.assertIsNot(self.med.especialidade, '', 'especialidade não deve ser vazio')

	def test_local(self):
		self.med = medico.Medico()
		self.med.setLocal('HUGO')
		self.assertIsNot(self.med.local, '', 'local não deve ser vazio')

	def test_crm(self):
		self.med = medico.Medico()
		self.med.setCRM(123)
		self.assertGreater(self.med.CRM, 0, 'número crm deve ser maior que 0')

	def test_idade(self):
		self.med = medico.Medico()
		self.med.setIdade(30)
		self.assertGreater(self.med.idade, 0, 'idade deve ser maior que 0')

	def test_email(self):
		REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
		self.med = medico.Medico()
		self.med.setEmail('exemplo@email.com')
		self.assertRegex(self.med.email, REGEX, 'email valido deve ser aceito')
		self.med.setEmail('exemplo.email.com')
		self.assertNotRegex(self.med.email, REGEX, 'email invalido')

	def test_expediente(self):
		self.med = medico.Medico()
		self.med.setInicio(9)
		self.med.setFim(15)
		self.assertLess(self.med.inicioExpediente, self.med.fimExpediente,
												'inicio deve ser menor que fim')
		self.assertGreater(self.med.fimExpediente, self.med.inicioExpediente,
												'fim deve ser maior que inicio')

	def test_agenda(self):
		self.med = medico.Medico()
		self.med.setInicio(9)
		self.med.setFim(15)
		agenda = self.med.getAgenda()
		expediente = self.med.fimExpediente - self.med.inicioExpediente
		self.assertEqual(len(agenda), expediente,
				'agenda deve conter a quantidade correta de horarios livres')

if __name__ == '__main__':
	unittest.main()
