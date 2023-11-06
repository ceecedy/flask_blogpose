from flask import Flask


# check the description of the sql alchemy for informations. 
from flask_sqlalchemy import SQLAlchemy


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

from blogpose import routes

