from flask import render_template, url_for, flash, redirect, request

# Importing the forms.py to use the register class and login class. 
# They will be used to pass them in render_template via a variable. 
from blogpose.forms import Register, Login, ForgotPassword, UpdateAccount

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

# importing secrets to process the profile picture to get secured. 
# importing os also for the process on where to put picture. 
import secrets, os

# importing image resizer module name pillow 
from PIL import Image

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
        # after creating hased password, we will now creating the user and insert it to the database. 
        user = User(
            fullname=form.fullname.data,
            username=form.username.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            birth_date=form.birth_date.data,
            gender=form.gender.data,
            street_address=form.street_address.data,
            country=form.country.data,
            city=form.city.data,
            password=hashed_password
        )
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
        return redirect(url_for('home'))
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

# function to process the uploads of user to their profile pictures. 
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # maximum size of profile picture
    output_size = (125, 125)
    # opening the image and pass it to an instance of Image 
    i = Image.open(form_picture)
    # creating thumbnail for the uploaded picture. 
    i.thumbnail(output_size)
    # saving the thumbnail 
    i.save(picture_path) 
    
    # thumbnails are helpful in the web for better performance. 
    # if we put the original picture in the web, it might affect the performance as the user grows. 
    
    return picture_fn

@app.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        # handling if the user changes his/her profile 
        if form.picture.data:
            print("I have the data")
            picture_file = save_picture(form.picture.data)
            current_user.img_file = picture_file
            
        current_user.fullname = form.fullname.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone_number = form.phone_number.data
        current_user.birth_date = form.birth_date.data
        current_user.gender = form.gender.data
        current_user.street_address = form.street_address.data
        current_user.country = form.country.data
        current_user.city = form.city.data
        
        # changing the data in the database 
        db.session.commit()
        
        #notify in the terminal that changes has succeed. 
        print("Changes succeeed.") 
        # flash the user that the changes succeed 
        flash(f"Data changes succeed for account {current_user.username}", "success")
        return redirect(url_for('account'))
        
    elif request.method == "GET":
        # if the request method is get, which by default at first is get
        # it will fetch all the current user data and display it to the field. 
        form.fullname.data = current_user.fullname 
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone_number.data = current_user.phone_number
        form.birth_date.data = current_user.birth_date
        form.gender.data = current_user.gender
        form.street_address.data = current_user.street_address
        form.country.data = current_user.country
        form.city.data = current_user.city
    
    profile_image = url_for('static', filename = 'profile_pics/' + current_user.img_file)
    # the img_file argument is for the database to pass the value of the profile picture to UI layout. 
    return render_template("account.html", title = "Account Settings", form = form, img_file = profile_image)


# A func can have multiple decorators. 
# You can just let the development server run while you make changes to your code. 