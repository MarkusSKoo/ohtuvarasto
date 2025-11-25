import unittest
from app import app, warehouses


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        warehouses.clear()

    def tearDown(self):
        warehouses.clear()

    def test_index_empty(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Warehouses', response.data)
        self.assertIn(b'No warehouses yet', response.data)

    def test_create_warehouse_get(self):
        response = self.client.get('/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create New Warehouse', response.data)

    def test_create_warehouse_post(self):
        response = self.client.post('/create', data={
            'name': 'Test Warehouse',
            'tilavuus': '100',
            'alku_saldo': '50'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Warehouse', response.data)
        self.assertIn('Test Warehouse', warehouses)

    def test_create_warehouse_duplicate(self):
        self.client.post('/create', data={
            'name': 'Duplicate',
            'tilavuus': '100',
            'alku_saldo': '0'
        })
        response = self.client.post('/create', data={
            'name': 'Duplicate',
            'tilavuus': '100',
            'alku_saldo': '0'
        })
        self.assertIn(b'Name already exists', response.data)

    def test_create_warehouse_empty_name(self):
        response = self.client.post('/create', data={
            'name': '',
            'tilavuus': '100',
            'alku_saldo': '0'
        })
        self.assertIn(b'Name is required', response.data)

    def test_create_warehouse_invalid_number(self):
        response = self.client.post('/create', data={
            'name': 'Test',
            'tilavuus': 'invalid',
            'alku_saldo': '0'
        })
        self.assertIn(b'Invalid number format', response.data)

    def test_edit_warehouse_get(self):
        from varasto import Varasto
        warehouses['Test'] = Varasto(100, 50)
        response = self.client.get('/edit/Test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Edit Warehouse', response.data)

    def test_edit_warehouse_not_found(self):
        response = self.client.get('/edit/NonExistent')
        self.assertEqual(response.status_code, 302)

    def test_delete_warehouse(self):
        from varasto import Varasto
        warehouses['ToDelete'] = Varasto(10, 0)
        response = self.client.post('/delete/ToDelete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('ToDelete', warehouses)

    def test_delete_nonexistent_warehouse(self):
        response = self.client.post('/delete/NonExistent', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
