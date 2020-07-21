import unittest
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, db_drop_and_create_all
from config import (
	bearer_tokens,
	database_setup
	)


# ---------------------------------------------------------------------------- #
# Setup of Unittest 														   #
# ---------------------------------------------------------------------------- #

class AgencyTestCase(unittest.TestCase):


    def setUp(self):
        
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgres://{}:{}@{}:{}/{}".format(
        	database_setup["username"], 
        	database_setup["password"],
        	database_setup["host"], 
        	database_setup["port"], 
        	database_setup["dbname"]
        	)

        setup_db(self.app, self.database_path)
        db_drop_and_create_all()

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()