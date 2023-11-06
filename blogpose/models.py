from blogpose import db

# importing datetime class 
from datetime import datetime

# Using sql alchemy, we can represent the database structure as classes. 
# That classes is called models. 
# This class named User is inheriting the db.Model. This is important to do when making a model. 
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True) # setting this id to be a primary key. It automatically generates. 
    username = db.Column(db.String(35), unique = True, nullable = False) # setting this username to become unique and not null. 
    email = db.Column(db.String(120), unique = True, nullable = False) # setting this email to become unique and not null. 
    # setting this email to become unique and not null.
    # this will accept string. It is possible because the image willbe hashed. 
    # users can have similar profiles, so it is not unique. 
    # if user does not set his/her own profile, there would be a default photo for them. 
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