from tests import BaseCase

from app.main import routes as main_route


class TestMainApp(BaseCase):

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.request.path, '/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Acceuil", response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_contact_page(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.request.path, '/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Contatez-nous", response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_houses_page(self):
        response = self.client.get('/proprietes-disponibles/')
        self.assertEqual(response.request.path, '/proprietes-disponibles/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
