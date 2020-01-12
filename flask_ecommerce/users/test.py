import unittest
from app import create_app, db
"""
Assert in Python is a debugging aid that tests a condition
"""
class UserTestCase(unittest.TestCase):
    """This class represents the user test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.data = {
            'username': 'xyz',
            'password': 'xyz',
            'email': 'xyz@test.com'
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def create_user(self):
        response = self.client().post('/users/create_user', json=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('User has been created', str(response.data))

    def login_user(self):
        response = self.client().post('/users/login', json={'username': self.data['username'],
                                                            'password': self.data['password']})
        self.assertEqual(response.status_code, 200)
        token = response.json
        headers = {"Authorization": "Bearer {}".format(token)}
        return headers

    def test_create_user(self):
        """Test API can create a user (POST request)"""
        self.create_user()

    def test_get_user(self):
        """Test API can get a user (GET request)."""
        self.create_user()
        headers = self.login_user()
        response = self.client().get('/users', headers=headers)
        self.assertEqual(response.status_code, 200)
        assert len(response.json) == 1 and response.json[0]['username'] == 'xyz'

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()