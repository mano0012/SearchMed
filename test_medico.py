import unittest
import medico

class TestPaciente(unittest.TestCase):
	def setUP(self):
		self.med = None

	def test_email(self):
		REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
		self.med = medico.Medico()
		self.med.setEmail('exemplo@email.com')
		self.assertRegex(self.med.email, REGEX, 'email valido deve ser aceito')
		self.med.setEmail('exemplo.email.com')
		self.assertNotRegex(self.med.email, REGEX, 'email invalido')

if __name__ == '__main__':
	unittest.main()
