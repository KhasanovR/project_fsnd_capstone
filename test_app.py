import json
from datetime import date
import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all
from config import (
    bearer_tokens,
    DATABASE_URL
)

casting_assistant_auth_header = {
    'Authorization': bearer_tokens['casting_assistant']
}

casting_director_auth_header = {
    'Authorization': bearer_tokens['casting_director']
}

executive_producer_auth_header = {
    'Authorization': bearer_tokens['executive_producer']
}


# ---------------------------------------------------------------------------- #
# Setup of Unittest 														   #
# ---------------------------------------------------------------------------- #

class AgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = DATABASE_URL

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # ----------------------------------------------------------------------------#
    # Tests for /actors POST
    # ----------------------------------------------------------------------------#

    def test_create_new_actor(self):
        json_create_actor = {
            'name': 'John',
            'age': 23
        }

        res = self.client().post('/actors', json=json_create_actor, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'] is not None)

    def test_error_401_new_actor(self):
        json_create_actor = {
            'name': 'John',
            'age': 23
        }

        res = self.client().post('/actors', json=json_create_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_422_create_new_actor(self):
        json_create_actor_without_name = {
            'age': 23
        }

        res = self.client().post('/actors', json=json_create_actor_without_name, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')


if __name__ == "__main__":
    unittest.main()
