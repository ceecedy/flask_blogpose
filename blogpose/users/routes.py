from flask import Blueprint, render_template, url_for, flash, redirect, request, abort

# instantiating a blueprint named users
users = Blueprint('users', __name__)

# importing a login function to the function login 
# for more informations, see login_user function.
# current_user is a variable from flask_login that holds a user data. 
# current_user can be used to modify certain current user tasks. 
# for logout function, just see the implementation for more details
# for login required function, just see the implementation for more details
from flask_login import login_user, current_user, logout_user, login_required
 
# bcrypt is from the init of the blogpose package
# db is from the init of the blogpose package
from blogpose import bcrypt, db

# importing all models in the models module. 
from blogpose.models import User, Post

# importing all forms in the forms module. 
from blogpose.users.forms import Register, Login, UpdateAccount, RequestResetForm, RequestPasswordForm

# importing utils module. 
from blogpose.users.utils import save_picture, send_reset_email

# importing the posts or feeds 
from blogpose.posts.routes import feeds

# importing the home page
from blogpose.main.routes import home 



@users.route("/register", methods = ['GET', 'POST'])
def register():
    # this if statement will check if there's a existing user logged in, in the system 
    # and saw the register button and attempting to click it. 
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
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
        return redirect(url_for('users.home'))
        # this redirect function will execute if input is validated, it will redirect to homepage. 
    else:
        print(form.errors) # to see the errors to this validation. 
        print("Not validating")

    return render_template("register.html", title = "Register", form = form)


@users.route("/login", methods = ['GET', 'POST'])
def login():
    # this if statement will check if there's a existing user logged in, in the system 
    # and saw the login button and attempting to click it. 
    if current_user.is_authenticated:
        return redirect(url_for('users.feeds'))
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
            # if next_page has data since user redirects to account, and if user logs in after that, 
            # then redirect to next_page which will be redirecting to account. 
            if next_page:
                return redirect(next_page)
            # else next_page is None, redirect to home. 
            else:
                flash("You are now successfully logged in!", "success")
                print("Login successful. Redirecting to home.") # to see if the form was getting validated
                return redirect(url_for('posts.feeds'))
        else:
            flash("Incorrect Username or Password. Try again.", "error")
        
    return render_template("login.html", title = "Login", form = form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route("/account", methods = ['GET', 'POST'])
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
        return redirect(url_for('users.account'))
        
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


# when the certain user clicks a name to its post, it will output all posts relating to that user. 
@users.route("/user/<string:username>")
@login_required
def user_post(username):
    # getting the user 
    # if none user was get, then return 404 or not found. 
    user = User.query.filter_by(username = username).first_or_404()
    # getting all the post in the database and set it to one variable 
    # posts = Post.query.all() 
    # making this a paginate method to make a object of all the data in the Post model to become paginated. 
    # the order_by method after query method is to order the data inside the Post model according to 
    #   the parameter inside the order_by
    # the forward slash will help you to break the query to multiple line. 
    posts = Post.query.filter_by(author = user)\
        .order_by(Post.date_posted.desc())\
        .paginate()
        
    return render_template("user_posts.html", title = "Feeds", posts = posts, user = user)


# to request the token  
@users.route("/resetpassword", methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.feeds'))
    form = RequestResetForm()
    
    # validating the email entered by the user. 
    # after validating we should send the current user email, and we will make a function for that  
    #   just above on this function. 
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash(f"The email {form.email.data} has been sent with instructions to reset your password.", "info")
        return redirect(url_for('users.login'))   
    return render_template("reset_request.html", title = "Reset Password", form = form)


# actual changing of passwords. 
@users.route("/resetpassword/<token>", methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('users.feeds'))
    user = User.verify_reset_token(token)
    
    # checking if there is a verified user 
    if user is None:
        flash(f"That is now invalid or expired token.", "warning")
        return redirect(url_for('users.reset_request'))
    
    form = RequestPasswordForm()
    if form.validate_on_submit(): # read method if forgotten how it is working. 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        # commit the addition of user in the database 
        db.session.commit()
        # finally flash the user and redirect the user to the homepage. 
        flash(f'Your account password is now changed!', 'success')
        # the success second string is called category (a parameter), 
        # and it will be passed to the layout design that is named category in jinja2 
        # from the word itself, flash will pop up a notification or a word in your screen that the account was created. 
        print("Redirecting...")  # Check if this line is executed
        return redirect(url_for('users.home'))
        # this redirect function will execute if input is validated, it will redirect to homepage. 
    return render_template("reset_token.html", title = "Reset Password", form = form)
    
    
# A func can have multiple decorators. 
# You can just let the development server run while you make changes to your code. 