import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

#give access to the project in ANY os we find ourselves in
#allow outside files/folders to be added to the project from the base directory

#load .env file, launch with environment variables
load_dotenv(os.path.join(basedir, ".env"))

class Config():
    """
        Set config variables for the flask app
        sing environment variables where available otherwise create the config variables
    """
    #keep here because actual set environment variables are going into gitignore, keeps app secure
    FLASK_APP = os.environ.get("FLASK_APP")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
    #securing for github so ppl can't mess with database
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'You will never guess this, haha'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False #Turn off database updates form sqlalchemy