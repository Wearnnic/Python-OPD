import unittest
from main import app

class QuadraticSolverTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_get_form(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.data.decode('utf-8')
        self.assertIn('Введите коэффициенты', data)

    def test_two_roots(self):
        response = self.client.post('/', data={'a': '1', 'b': '-3', 'c': '2'})
        data = response.data.decode('utf-8')
        self.assertIn('Два корня', data)
        self.assertIn('x1 = 2.00', data)
        self.assertIn('x2 = 1.00', data)

    def test_one_root(self):
        response = self.client.post('/', data={'a': '1', 'b': '2', 'c': '1'})
        data = response.data.decode('utf-8')
        self.assertIn('Один корень', data)
        self.assertIn('x = -1.00', data)

    def test_no_roots(self):
        response = self.client.post('/', data={'a': '1', 'b': '0', 'c': '1'})
        data = response.data.decode('utf-8')
        self.assertIn('Корней нет', data)

    def test_a_zero(self):
        response = self.client.post('/', data={'a': '0', 'b': '2', 'c': '1'})
        data = response.data.decode('utf-8')
        self.assertIn('Коэффициент a не должен быть равен нулю', data)

    def test_invalid_input(self):
        response = self.client.post('/', data={'a': 'abc', 'b': '2', 'c': '1'})
        data = response.data.decode('utf-8')
        self.assertIn('Пожалуйста, введите корректные числовые значения', data)

if __name__ == '__main__':
    unittest.main()
