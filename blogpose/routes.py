from flask import Flask, render_template, url_for, flash, redirect, request

# Importing the forms.py to use the register class and login class. 
# They will be used to pass them in render_template via a variable. 
from blogpose.forms import Register, Login, ForgotPassword

# import the classes from models.py 
from blogpose.models import User, Post
# This should be imported here to avoid import error on models 

# importing app in this routes since our decorators uses app
# app is from the init of the blogpose package
from blogpose import app 
          
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