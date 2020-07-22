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

    # ----------------------------------------------------------------------------#
    # Tests for /actors GET
    # ----------------------------------------------------------------------------#

    def test_get_all_actors(self):
        res = self.client().get('/actors?page=1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_error_401_get_all_actors(self):
        res = self.client().get('/actors?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_404_get_actors(self):
        res = self.client().get('/actors?page=1234567890', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    # ----------------------------------------------------------------------------#
    # Tests for /actors PATCH
    # ----------------------------------------------------------------------------#

    def test_edit_actor(self):
        json_edit_actor_with_new_age = {
            'age': 32
        }
        res = self.client().patch('/actors/1', json=json_edit_actor_with_new_age, headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)
        self.assertEqual(data['updated'], 2)

    def test_error_400_edit_actor(self):
        res = self.client().patch('/actors/1', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    def test_error_404_edit_actor(self):
        json_edit_actor_with_new_age = {
            'age': 32
        }
        res = self.client().patch('/actors/1234567890', json=json_edit_actor_with_new_age,
                                  headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    # ----------------------------------------------------------------------------#
    # Tests for /actors DELETE
    # ----------------------------------------------------------------------------#

    def test_error_401_delete_actor(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_error_403_delete_actor(self):
        res = self.client().delete('/actors/1', headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '2')

    def test_error_404_delete_actor(self):
        res = self.client().delete('/actors/1234567890', headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

    # ----------------------------------------------------------------------------#
    # Tests for /movies POST
    # ----------------------------------------------------------------------------#

    def test_create_new_movie(self):
        json_create_movie = {
            'title': 'My Movie',
            'release_date': date.today()
        }

        res = self.client().post('/movies', json=json_create_movie, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['created'] is not None)

    def test_error_422_create_new_movie(self):
        json_create_movie_without_name = {
            'release_date': date.today()
        }

        res = self.client().post('/movies', json=json_create_movie_without_name, headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')


if __name__ == "__main__":
    unittest.main()
