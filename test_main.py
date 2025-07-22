import unittest
import main
import database
import os

class TestMain(unittest.TestCase):

    def setUp(self):
        database.init_db()

    def tearDown(self):
        os.remove(database.DATABASE)

    def test_register(self):
        database.create_user('testuser', 'testpassword')
        user = database.get_user('testuser')
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], 'testuser')

    def test_subscribe(self):
        database.create_user('testuser', 'testpassword')
        database.subscribe_user('testuser')
        user = database.get_user('testuser')
        self.assertTrue(user['subscribed'])

if __name__ == '__main__':
    unittest.main()
