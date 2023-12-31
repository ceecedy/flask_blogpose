from flask_wtf import FlaskForm

# This import is for uploading a files that will be used in the app. 
# the FileField is a class that creates an object for the input of images. 
# the FileAllowed is a class that responsible for filtering the allowed files for the input of the user. 
# FileAllowed class can be seen as validator. 
from flask_wtf.file import FileAllowed, FileField

# Inside the forms class we need a fields that will be an object.
# We will use StringField class from module wtforms to create a String object to accept a string input. 
# PasswordField class from wtforms is also imported to create an object to accept effective password. 
# SubmitField class from wtforms is used to create a button specialized in submitting data. 
# DateField class was used to take the dates input. It is from wtforms module.
# RadioField class is used for taking radio button inputs. From wtforms module. 
# ValidationError class is used to validate every inputs of the user in the form.
# TextAreaField class will make an object that has the content of the post in the Post form.
from wtforms import StringField, PasswordField, SubmitField, DateField, RadioField, Form, SelectField, BooleanField, ValidationError, TextAreaField

# importing a class that will make sure that the input should not be empty. 
# the name of the class is "DataRequired" from module wtforms.validators. 
# Length class was also used to make sure the imput will have limited characters. 
# EqualTo clas is used to compare the current object to another. 
# Regexp or Regular Expression class is used to ensure that the input is a number. It is from validator module. 
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

# Importing flask_login.utils.current_user for the usage of UpdateAccount form. 
# This is to validate the current user changes in data. 
from flask_login import current_user

# importing User Model 
from blogpose.models import User


class Register(FlaskForm):
    # Validators parameter are used in the StringField to have restrictions for input of the users. 
    # Inside validators, DataRequired class is used and Length to make sure that there will be restrictions 
    #   on both input and input length. 
    # For email validator, we used the Email class from wtforms.validators to ensure that the input email 
    #   is valid.  
    
    # accept full name
    # will pass it to variable fullname
    fullname = StringField('Full Name', validators=[
        DataRequired(message="Full name is required."),
        Length(min=10, max=100, message="Full name should be between 10 and 100 characters.")
    ])
    
    # accept username
    # will pass it to variable username
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=7, max=35, message="Username should be between 7 and 35 characters.")
    ])
    
    # accept email 
    # will pass it to variable email 
    email = StringField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email format.")
    ])
    
    # accept password 
    # will pass it to variable password 
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=10, max=40, message="Password should be between 10 and 40 characters.")
    ])
     
    # accept confirmation of password 
    # will pass it to variable confirm_password 
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    # accept phone number 
    # will pass it to the variable phone_number
    phone_number = StringField('Phone Number', validators=[
        DataRequired(message="Phone number is required."),
        Regexp("^0[0-9]{10}$", message="Phone number must be 11 digits and starts with 0.")
    ])
    
    # accept birth date 
    # will pass it to the variable birth_date 
    birth_date = DateField('Birth Date', validators=[DataRequired(message='Birthday is required.')])
    
    # accept gender 
    # will pass it to the variable gender 
    gender = RadioField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('not_say', 'Prefer not to say')
    ], validators=[DataRequired(message="Please select your gender.")])

    # accept street address 
    # will pass it to the variable street_address
    street_address = StringField('Street Address', validators=[
        DataRequired(message="Street address is required."),
        Length(min=10, max=100, message="Address should be between 10 and 100 characters.")
    ])
    
    # accept country 
    # will pass it to the variable country 
    country = SelectField('Country', choices=[
        ('Philippines'),
        ('United Kingdom'),
        ('United States'),
        ('Japan')
    ], validators=[DataRequired(message="Please select your country.")])
    
    # accept city 
    # will pass it to the variable city 
    city = StringField('City', validators=[
        DataRequired(message="City is required."),
        Length(min=3, max=100, message="City should not exceed 100 characters.")
    ])
    
    # accept submit button 
    # will pass it to variable submit 
    submit = SubmitField('Submit')

    # function to validate username field. 
    def validate_username(self, username):
        # getting the query of a given username if exists and pass it to variable user 
        # the first method will be use to securely return the first result to filter. 
        user = User.query.filter_by(username = username.data).first()
        
        # if user does not found, it will have value "None"
        if user:    
            raise ValidationError(f"The username {username.data} already exists. Try another")
    
    # function to validate email field. 
    def validate_email(self, email):
        # getting the query of a given email if exists and pass it to variable user 
        # the first method will be use to securely return the first result to filter. 
        user = User.query.filter_by(email = email.data).first()
        
        # if user does not found, it will have value "None"
        if user:    
            raise ValidationError(f"The username {email.data} already exists. Try another")


class Login(FlaskForm):
    
    # accepting username 
    # will pass it to variable username 
    username = StringField('Username', validators = [DataRequired(message = "This is required, have input on this form."), 
                                                     Length(min = 7, max = 35)]) 
    # accept password 
    # will pass it to variable password 
    password = PasswordField('Password', validators=[DataRequired(message = "Password should be minimum of 10 and maximum of 16."),
                                                     Length(min = 10, max = 40)]) 
    # accept boolean to let the user have choice to stay login 
    # will pass it to the variable remember 
    remember = BooleanField('Remember me')
    
    # accept login button 
    # will pass it to variable Login 
    login = SubmitField('Login')
    

class UpdateAccount(FlaskForm):
    
    # accept full name
    # will pass it to variable fullname
    fullname = StringField('Full Name', validators=[
        DataRequired(message="Full name is required."),
        Length(min=10, max=100, message="Full name should be between 10 and 100 characters.")
    ])
    
    # accept username
    # will pass it to variable username
    username = StringField('Username', validators=[
        DataRequired(message="Username is required."),
        Length(min=7, max=35, message="Username should be between 7 and 35 characters.")
    ])
    
    # accept email 
    # will pass it to variable email 
    email = StringField('Email', validators=[
        DataRequired(message="Email is required."),
        Email(message="Invalid email format.")
    ])
    
    # accept phone number 
    # will pass it to the variable phone_number
    phone_number = StringField('Phone Number', validators=[
        DataRequired(message="Phone number is required."),
        Regexp("^0[0-9]{10}$", message="Phone number must be 11 digits and starts with 0.")
    ])
    
    # accept birth date 
    # will pass it to the variable birth_date 
    birth_date = DateField('Birth Date', validators=[DataRequired(message='Birthday is required.')])
    
    # accept gender 
    # will pass it to the variable gender 
    gender = RadioField('Gender', choices=[
        ('Male'),
        ('Female'),
        ('Prefer not to say')
    ], validators=[DataRequired(message="Please select your gender.")])

    # accept street address 
    # will pass it to the variable street_address
    street_address = StringField('Street Address', validators=[
        DataRequired(message="Street address is required."),
        Length(min=10, max=100, message="Address should be between 10 and 100 characters.")
    ])
    
    # accept country 
    # will pass it to the variable country 
    country = SelectField('Country', choices=[
        ('Philippines'),
        ('United Kingdom'),
        ('United States'),
        ('Japan')
    ], validators=[DataRequired(message="Please select your country.")])
    
    # accept city 
    # will pass it to the variable city 
    city = StringField('City', validators=[
        DataRequired(message="City is required."),
        Length(min=3, max=100, message="City should not exceed 100 characters.")
    ])
    
    # accept profile picture 
    # will pass it to the variable picture
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    # accept submit button 
    # will pass it to variable submit 
    submit = SubmitField('Update')

    # function to validate username field. 
    def validate_username(self, username):
        # checking first if a user's username is not equal to the current username.  
        if username.data != current_user.username:
            # getting the query of a given username if exists and pass it to variable user 
            # the first method will be use to securely return the first result to filter. 
            user = User.query.filter_by(username = username.data).first()
            
            # if user does not found, it will have value "None"
            if user:    
                raise ValidationError(f"The username {username.data} already exists. Try another")    

    
    # function to validate email field. 
    def validate_email(self, email):
        # checking first if a user's email is not equal to the current email.  
        if email.data != current_user.email:
            # getting the query of a given email if exists and pass it to variable user 
            # the first method will be use to securely return the first result to filter. 
            user = User.query.filter_by(email = email.data).first()
            
            # if user does not found, it will have value "None"
            if user:    
                raise ValidationError(f"The username {email.data} already exists. Try another")


# this class is to request a reset form for email. 
class RequestResetForm(FlaskForm):
    
    # accepting email for password change. 
    # will pass it to variable email
    email = StringField('Email', validators = [DataRequired(message = "This is required, have input on this form."),
                                               Email()])
    # accept login button 
    # will pass it to variable change 
    change = SubmitField('Request Password Reset')
    
     # function to validate email field. 
    def validate_email(self, email):
        # getting the query of a given email if exists and pass it to variable user 
        # the first method will be use to securely return the first result to filter. 
        user = User.query.filter_by(email = email.data).first()
        
        # if user is none, then raise validation error to let the user to register first. 
        if user is None:    
            raise ValidationError(f"There is no account associated with the email {email.data}. Register first.")
        
        
# this class is for requesting password form. 
class RequestPasswordForm(FlaskForm):
    
    # accept password 
    # will pass it to variable password 
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required."),
        Length(min=10, max=40, message="Password should be between 10 and 40 characters.")
    ])
     
    # accept confirmation of password 
    # will pass it to variable confirm_password 
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Confirm your password."),
        EqualTo('password', message="Passwords must match.")
    ])
    
    # accept password reset button 
    # will pass it to variable change 
    change = SubmitField('Change Password')