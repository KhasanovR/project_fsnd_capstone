
from datetime import date
from sqlalchemy import (
	Column,
	String,
	Integer,
	Date
	)
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
    db_init()

def db_init():

    new_movie = (Movie(
        title = 'My Udacity FSND Capstone Movie',
        release_date = date.today()
        ))
	
	new_movie.insert()
    
# ---------------------------------------------------------------------------- #
# Movies Model 																   #
# ---------------------------------------------------------------------------- #

class Movie(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(Date)
  
  def __init__(self, title, release_date) :
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title' : self.title,
      'release_date': self.release_date
    }
    