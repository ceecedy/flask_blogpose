from flask import render_template, url_for, flash, redirect, request, abort

# Importing the forms.py to use the register class and login class. 
# They will be used to pass them in render_template via a variable. 
from blogpose.forms import Register, Login, UpdateAccount, NewPost, RequestResetForm, RequestPasswordForm

# import the classes from models.py 
from blogpose.models import User, Post
# This should be imported here to avoid import error on models 

# importing app in this routes since our decorators uses app
# app is from the init of the blogpose package 
# bcrypt is from the init of the blogpose package
# db is from the init of the blogpose package
# mail initialized from the init, for mail server. 
from blogpose import app, bcrypt, db, mail

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

# importing message from flask-mail for additional mail functions
from flask_mail import Message

# This app route is a route api. This is basically the home route. 
@app.route("/") 
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/feeds")
@login_required
def feeds():
    # getting all the post in the database and set it to one variable 
    # posts = Post.query.all()
    # making this a paginate method to make a object of all the data in the Post model to become paginated. 
    # the order_by method after query method is to order the data inside the Post model according to 
    #   the parameter inside the order_by
    posts = Post.query.order_by(Post.date_posted.desc()).paginate()
    return render_template("feeds.html", title = "Feeds", posts = posts)


# when the certain user clicks a name to its post, it will output all posts relating to that user. 
@app.route("/user/<string:username>")
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
        return redirect(url_for('feeds'))
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
                return redirect(url_for('feeds'))
        else:
            flash("Incorrect Username or Password. Try again.", "error")
        
    return render_template("login.html", title = "Login", form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


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


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPost()
    if form.validate_on_submit():
        # creating the object with values inserted by the user in his/her post. 
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        # now adding the created object to the database as record. 
        db.session.add(post)
        db.session.commit()
        flash(f"Your post has been created!", "success")
        return redirect(url_for('feeds'))
    
    return render_template("create_post.html", title = "New Post", form = form, legend = "New Post") 


# the brackets inside the route is a variable that is interchangeable depending on the post to update. 
# the int: syntax is to ensure that the post_id will be an int. 
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post.html', title = post.title, post = post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # after the post was found in the database, check first if the current user was a match to the particular post.
    if post.author != current_user:
        # error response to html server. 
        abort(403)
    
    form = NewPost()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f"This post has been successfully updated!", "success")
        return redirect(url_for("post", post_id = post.id))
    
    elif request.method == "GET":
        form.title.data = post.title     
        form.content.data = post.content
        
    return render_template("create_post.html", title = "Update Post", form = form, legend = "Update Post") 


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # after the post was found in the database, check first if the current user was a match to the particular post.
    if post.author != current_user:
        # error response to html server. 
        abort(403)
    
    #deleting the post via id 
    db.session.delete(post)
    db.session.commit()
    
    # notify user 
    flash(f"You have successfully deleted your post.", "success")
    return redirect(url_for('feeds'))


# function to send the current email. 
def send_reset_email(user):
    token = user.get_reset_token()
    # sending the email using url, using msg class from flask-mail
    msg = Message("Password Reset Request", sender = "blogpose@support.com", recipients = [user.email])
    
    msg.body = f''' To reset your password, visit the following link:
    
    {url_for('reset_token', token = token, _external = True)}
    
    If you did not make this request, simply ignore this message. 
    '''
    
    # finally passing the message to the email of the user.
    mail.send(msg)
    

@app.route("/resetpassword", methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('feeds'))
    form = RequestResetForm()
    
    # validating the email entered by the user. 
    # after validating we should send the current user email, and we will make a function for that  
    #   just above on this function. 
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash(f"The email {form.email.data} has been sent with instructions to reset your password.", "info")
        return redirect(url_for('login'))   
    return render_template("reset_request.html", title = "Reset Password", form = form)

    
@app.route("/resetpassword/<token>", methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('feeds'))
    user = User.verify_reset_token(token)
    
    # checking if there is a verified user 
    if user is None:
        flash(f"That is now invalid or expired token.", "warning")
        return redirect(url_for('reset_request'))
    
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
        return redirect(url_for('home'))
        # this redirect function will execute if input is validated, it will redirect to homepage. 
    return render_template("reset_token.html", title = "Reset Password", form = form)




# A func can have multiple decorators. 
# You can just let the development server run while you make changes to your code. 