
from flask_sqlalchemy import SQLAlchemy
from config import database_setup


#----------------------------------------------------------------------------#
# Database Setup 
#----------------------------------------------------------------------------#

database_path = "postgres://{}:{}@{}:{}/{}"
	.format(
		database_setup["username"], 
		database_setup["password"], 
		database_setup["host"], 
		database_setup["port"], 
		database_setup["db_name"]
		)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):

    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    
    db.drop_all()
    db.create_all()
    