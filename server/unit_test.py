import unittest
from app import app
from tempdb import TempDB
from unittest import mock


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        app.testing = True
        self.client = app.test_client()
        self.db = TempDB()
        self.db.create({'name': '買早餐'})
        self.db.create({'name': '買中餐'})
        self.test_db = TempDB()
        self.test_db.create({'name': '買早餐'})
        self.test_db.create({'name': '買中餐'})

    def test_post_task(self):
        data = {'name': '再買早餐'}

        with mock.patch('app.temp_db', new=self.db):
            response = self.client.post('/task', json=data)
        response_json = response.json
        response_status_code = response.status_code

        self.assertEqual({"result": self.test_db.create(data)}, response_json)
        self.assertEqual(201, response_status_code)
        self.assertEqual(self.test_db.read_all(), self.db.read_all())

    def test_get_task(self):
        with mock.patch('app.temp_db', new=self.db):
            response = self.client.get('/tasks')
        response_json = response.json
        response_status_code = response.status_code

        self.assertEqual({"result": self.test_db.read_all()}, response_json)
        self.assertEqual(200, response_status_code)

    def test_put_task(self):
        data = {"name": "買早餐", "status": 1}
        task_id = 0

        with mock.patch('app.temp_db', new=self.db):
            response = self.client.put(f'/task/{task_id}', json=data)
        response_json = response.json
        response_status_code = response.status_code

        self.assertEqual(self.test_db.update(data, task_id), response_json)
        self.assertEqual(200, response_status_code)
        self.assertEqual(self.test_db.read_all(), self.db.read_all())

    def test_delete_task(self):
        task_id = 0

        with mock.patch('app.temp_db', new=self.db):
            response = self.client.delete(f'/task/{task_id}')
        response_status_code = response.status_code

        self.test_db.delete(task_id)

        self.assertEqual(200, response_status_code)
        self.assertEqual(self.test_db.read_all(), self.db.read_all())


if __name__ == '__main__':
    unittest.main()
