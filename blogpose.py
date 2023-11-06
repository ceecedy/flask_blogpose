from flask import Flask, render_template, url_for, flash, redirect, request

# Importing the forms.py to use the register class and login class. 
# They will be used to pass them in render_template via a variable. 
from forms import Register, Login, ForgotPassword

# check the description of the sql alchemy for informations. 
from flask_sqlalchemy import SQLAlchemy

# importing datetime class 
from datetime import datetime

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
     
     

# creating dummy data 
posts = [
    {
        "author": "Ryan Lester Zamudio",
        "title": "I'm Using BlogPose!",
        "content": "First Post Content",
        "date_posted": "October 26, 2023"
    },
    {
        "author": "Amado Jeremiah Galzote",
        "title": "I'm Using BlogPose TOO!",
        "content": "Second Post Content",
        "date_posted": "October 27, 2023"
    }
]

# This app route is a route api. This is basically the home route. 
@app.route("/") 
@app.route("/home")
def home():
    return render_template("home.html", posts = posts)

@app.route("/about")
def about():
    return render_template("about.html", title = "About")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = Register()
    print(request.form) # outputting all inputs in the register form to the terminal in list form. 
    if form.validate_on_submit(): # read method if forgotten how it is working. 
        print("Form is valid")  # Check to ensure this gets printed
        flash(f'Account {form.username.data} has been created!', 'success')
        # the success second string is called category (a parameter), 
        # and it will be passed to the layout design that is named category in jinja2 
        # from the word itself, flash will pop up a notification or a word in your screen that the account was created. 
        print("Redirecting...")  # Check if this line is executed
        return redirect(url_for('home'))
        # this redirect function will execute if input is validated, it will redirect to homepage. 
    else:
        print(form.errors) # to see the errors to this validation. 
        print("Not validating")

    return render_template("register.html", title = "Register", form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        if form.username.data == "ceeceddy" and form.password.data == "KoreanChallenger":
            flash("You are now successfully logged in!", "success")
            print("Login successful. Redirecting to home.") # to see if the form was getting validated
            return redirect(url_for('home'))
        else:          
            flash("Incorrect Username or Password. Try again.", "error")
        
    return render_template("login.html", title = "Login", form = form)

@app.route("/forgotpassword")
def forgot_password():
    form = ForgotPassword()
    return render_template("forgot_password.html", title = "Forgot Password", form = form)


# A func can have multiple decorators. 
# You can just let the development server run while you make changes to your code. 


if __name__ == "__main__":
    app.run(debug=True)