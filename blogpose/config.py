# This is where all your environment variables in this project is stored. 
class Config():
    # When using this two class that is made to be a form, we need to make a secret key. 
    # This will protect your users from modifying cookies and malicious attacks across web 
    SECRET_KEY = "8b1bb1a28dbba839be48a867ccd0fc45"   

    # URI is where your database is located. 
    # we will use SQL lite for the development of this project and postgresql for the production. 
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    # triple slash is a relative path, that means the site.db will be created into the current file which is the project file. 
    
    # email server configurations. 
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    # using environment variables for private access 
    MAIL_USERNAME = "jceee.castro@gmail.com"
    MAIL_PASSWORD = "rdbl qzno udxr jtlh"