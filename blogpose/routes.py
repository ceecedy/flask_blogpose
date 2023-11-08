from flask import render_template, url_for, flash, redirect, request

# Importing the forms.py to use the register class and login class. 
# They will be used to pass them in render_template via a variable. 
from blogpose.forms import Register, Login, ForgotPassword, Account

# import the classes from models.py 
from blogpose.models import User, Post
# This should be imported here to avoid import error on models 

# importing app in this routes since our decorators uses app
# app is from the init of the blogpose package 
# bcrypt is from the init of the blogpose package
# db is from the init of the blogpose package
from blogpose import app, bcrypt, db

# importing a login function to the function login 
# for more informations, see login_user function.
# current_user is a variable from flask_login that holds a user data. 
# current_user can be used to modify certain current user tasks. 
# for logout function, just see the implementation for more details
# for login required function, just see the implementation for more details
from flask_login import login_user, current_user, logout_user, login_required

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
    # this if statement will check if there's a existing user logged in, in the system 
    # and saw the register button and attempting to click it. 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Register()
    print(request.form) # outputting all inputs in the register form to the terminal in list form. 
    if form.validate_on_submit(): # read method if forgotten how it is working. 
        print("Form is valid")  # Check to ensure this gets printed
        # will now  create hashed password first. 
        # it is decoded to utf-8 to output to string, not bytes. 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # after creating hased password, we will not creating the user and insert it to the database. 
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        # add the user instance to the database
        db.session.add(user)
        # commit the addition of user in the database 
        db.session.commit()
        # finally flash the user and redirect the user to the homepage. 
        flash(f'Account {form.username.data} has been created!', 'success')
        # the success second string is called category (a parameter), 
        # and it will be passed to the layout design that is named category in jinja2 
        # from the word itself, flash will pop up a notification or a word in your screen that the account was created. 
        print("Redirecting...")  # Check if this line is executed
        return redirect(url_for('login'))
        # this redirect function will execute if input is validated, it will redirect to homepage. 
    else:
        print(form.errors) # to see the errors to this validation. 
        print("Not validating")

    return render_template("register.html", title = "Register", form = form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    # this if statement will check if there's a existing user logged in, in the system 
    # and saw the login button and attempting to click it. 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit():
        # Logging in the user
        # query first if the username is existing or account is existing
        user = User.query.filter_by(username = form.username.data).first()
        # if the username exists and the corresponding database password and the input password matches.
        # execute this conditional statement. 
        if user and bcrypt.check_password_hash(user.password, form.password.data): 
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            print("Full URL:", request.url) # For debugging purposes
            print("Next Page:", next_page) # For debugging purposes
            app.logger.debug(request.args) # For debugging purposes
            # if next_page has data since user redirects to account, and if user logs in after that, 
            # then redirect to next_page which will be redirecting to account. 
            if next_page:
                return redirect(next_page)
            # else next_page is None, redirect to home. 
            else:
                flash("You are now successfully logged in!", "success")
                print("Login successful. Redirecting to home.") # to see if the form was getting validated
                return redirect(url_for('home'))
        else:
            flash("Incorrect Username or Password. Try again.", "error")
        
    return render_template("login.html", title = "Login", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/forgotpassword")
def forgot_password():
    form = ForgotPassword()
    return render_template("forgot_password.html", title = "Forgot Password", form = form)

@app.route("/account")
@login_required
def account():
    form = Account()
    return render_template("account.html", title = "Account Settings")


# A func can have multiple decorators. 
# You can just let the development server run while you make changes to your code. 