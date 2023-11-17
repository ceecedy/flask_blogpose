from flask import Flask

# check the description of the sql alchemy for informations. 
from flask_sqlalchemy import SQLAlchemy

# check the description of the Bcrypt for informations
from flask_bcrypt import Bcrypt

# check the description of LoginManager for informations 
from flask_login import LoginManager

# to have a send email function for authentication
from flask_mail import Mail

# importing oauth provider also here because the init is not reaching here. 
from flask_oauthlib.provider import OAuth2Provider

# importing config class from config file.  
from blogpose.config import Config

# It is important to create a database instance. That's the use of SQL Alchemy. 
db = SQLAlchemy()

# creating an instance of bcrypt. 
# using bcrypt - a type of hasing algorithm, will help the passwords of the users to get hashed. 
bcrypt = Bcrypt()

# creating an instance of LoginManager 
# using LoginManager will ease up the development of login system of this project. 
login_manager = LoginManager()
# declare initially the login view of the app. 
# this will be get by the routes.py if needed to login first. 
login_manager.login_view = "users.login"
# along with login_view, this is a flash message above the login_view. 
# This will be get also by the routes.py if needed to login first. 
# declare initially this line below, if the user had access the account form while not logged in. 
login_manager.login_message_category = "info"

# initializing the oauth. 
oauth = OAuth2Provider()

# after setting up the mail server, we will now initialize it. 
mail = Mail()

# function to create the app. 
def create_app(config_class = Config):
    # creation of the application
    app = Flask(__name__)

    # this is to include the environment variables needed in this project. 
    app.config.from_object(Config)
    
    # init_app is a method to use to initialize the extension.
    # on this structure, this initializations are part of the application when this create_app func runs.
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # importing routes at this point to load up the routes at the init. 
    from blogpose.users.routes import users
    from blogpose.posts.routes import posts
    from blogpose.main.routes import main
    
    # registering blueprints of the packages 
    # this is to let this "__init__.py" file to get the blueprints of sub-packages to let the sub-packages 
    #   to be part of this "__init__.py" to become one big system. 
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    
    # finally return app when everything is within the app. 
    return app
