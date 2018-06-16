# app/__init__.py
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

#### Create the instances of the Flask extensions without intializing
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

######################################
#### Application Factory Function ####
######################################
def create_app(config_name):
    # create the Flask application
    app = Flask(__name__) 
    # configuring the Flask applicaton
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initializing the extensions to be used
    # bind each extension to the Flask application instance (app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    
    ## attach routes and custom error pages blueprint here
    ## blueprint registration
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
