# importing datetime class 
from datetime import datetime

from blogpose import db, login_manager 

# this is used for the status feedback of the logged in user. 
# for more informations, read the UserMixin.
from flask_login import UserMixin

# func with decorator. Called user_loader.  
# this is for reloading the user from the user id stored in the session. 
# read the descriptions in the decorator for more informations.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Using sql alchemy, we can represent the database structure as classes. 
# That classes is called models. 
# This class named User is inheriting the db.Model. This is important to do when making a model. 
# extending also the UserMixin class in the class User. 
# This is essential because the extension load user has to know how to find the user by id. 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True) # setting this id to be a primary key. It automatically generates. 
    fullname = db.Column(db.String(150), nullable=False) # setting this fullname to become not null 
    username = db.Column(db.String(35), unique = True, nullable = False) # setting this username to become unique and not null. 
    email = db.Column(db.String(120), unique = True, nullable = False) # setting this email to become unique and not null. 
    # setting this email to become unique and not null.
    # this will accept string. It is possible because the image willbe hashed. 
    # users can have similar profiles, so it is not unique. 
    # if user does not set his/her own profile, there would be a default photo for them. 
    phone_number = db.Column(db.String(11), nullable=False) # setting this phone_number to become not null
    birth_date = db.Column(db.Date, nullable=False) # setting this birth_date to become not null
    gender = db.Column(db.String(10), nullable=False) # setting this gender to become not null
    street_address = db.Column(db.String(100), nullable=False) # setting this street_address to become not null
    country = db.Column(db.String(50), nullable=False) # setting this country to become not null
    city = db.Column(db.String(100), nullable=False) # setting this city to become not null
    img_file = db.Column(db.String(20), nullable = False, default = "default.jpg")
    # This password will have to accept 60 characters in a hashed way. 
    # Password can be not unique also for the reason of some users may have similar passwords. 
    password = db.Column(db.String(60), nullable = False) 
    
    # relationship to the Post Model.
    # The argument Post will be the connection of this User class to the other 
    # The argument backref will reference the user who post a particular post. 
    # backref adds another column to the Post Model and it will named Author, the value passed will be the instance of the user. 
    # lazy argument makes the sqlalchemy to load the data necessary from the database in one go. 
    posts = db.relationship("Post", backref = "Author", lazy = True)
    
    def __repr__(self):
        return f"User ('{self.username}', '{self.email}', '{self.img_file}')"
    

# This class named Post is inheriting the db.Model. This is important to do when making a model.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True) # setting this id to be a primary key. It automatically generates. 
    title = db.Column(db.String(100), nullable = False) # setting the title to become not null so that all the post will have a title. 
    # this will accept datetime where the default value to be accepted is the current datetime at specific utc. 
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) 
    content = db.Column(db.Text, nullable = False)
    
    # adding user id to a particular post. 
    # the argument inside foreign key is small case because the models in the SQL alchemy when they create the table 
    #   it automatically makes it a smallcase. Same goes on to the other models. 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    
    
    def __repr__(self):
        return f"Post ('{self.title}', '{self.date_posted}')" 