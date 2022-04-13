import os


DEBUG = True
TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///weather.sqlite'
SECRET_KEY = os.urandom(24)
