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


app = Flask(__name__)
# When using this two class that is made to be a form, we need to make a secret key. 
# This will protect your users from modifying cookies and malicious attacks across web 
app.config['SECRET_KEY'] = "8b1bb1a28dbba839be48a867ccd0fc45"   

# URI is where your database is located. 
# we will use SQL lite for the development of this project and postgresql for the production. 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
# triple slash is a relative path, that means the site.db will be created into the current file which is the project file. 

# It is important to create a database instance. That's the use of SQL Alchemy. 
db = SQLAlchemy(app)

# creating an instance of bcrypt. 
# using bcrypt - a type of hasing algorithm, will help the passwords of the users to get hashed. 
bcrypt = Bcrypt(app)

# creating an instance of LoginManager 
# using LoginManager will ease up the development of login system of this project. 
login_manager = LoginManager(app)
# declare initially the login view of the app. 
# this will be get by the routes.py if needed to login first. 
login_manager.login_view = "login"
# along with login_view, this is a flash message above the login_view. 
# This will be get also by the routes.py if needed to login first. 
# declare initially this line below, if the user had access the account form while not logged in. 
login_manager.login_message_category = "info"

# initializing the oauth. 
oauth = OAuth2Provider(app)

# email server configurations. 
app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = "587"
app.config["MAIL_USE_TLS"] = "True"

# using environment variables for private access 
app.config["MAIL_USERNAME"] = "jceee.castro@gmail.com"
app.config["MAIL_PASSWORD"] = "rdbl qzno udxr jtlh"

# after setting up the mail server, we will now initialize it. 
mail = Mail(app)

# importing routes at this point to load up the routes at the init. 
from blogpose import routes

