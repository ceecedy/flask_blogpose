# This is imported to ease the creation of forms in the flask. 
from flask_wtf import FlaskForm
# FlaskForm is a class from the module flask_wtf. So if we create forms, we need to make a class that extends FlaskForm. 

# Inside the forms class we need a fields that will be an object.
# We will use StringField class from module wtforms to create a String object to accept a string input. 
# PasswordField class from wtforms is also imported to create an object to accept effective password. 
# SubmitField class from wtforms is used to create a button specialized in submitting data. 
# DateField class was used to take the dates input. It is from wtforms module.
# RadioField class is used for taking radio button inputs. From wtforms module. 
from wtforms import StringField, PasswordField, SubmitField, DateField, RadioField, Form, SelectField, BooleanField

# importing a class that will make sure that the input should not be empty. 
# the name of the class is "DataRequired" from module wtforms.validators. 
# Length class was also used to make sure the imput will have limited characters. 
# EqualTo clas is used to compare the current object to another. 
# Regexp or Regular Expression class is used to ensure that the input is a number. It is from validator module. 
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class Register(FlaskForm):
    # Validators parameter are used in the StringField to have restrictions for input of the users. 
    # Inside validators, DataRequired class is used and Length to make sure that there will be restrictions 
    #   on both input and input length. 
    # For email validator, we used the Email class from wtforms.validators to ensure that the input email 
    #   is valid.  
    
    # accept full name
    # will pass it to variable fullname
    fullname = StringField('FullName', validators = [DataRequired(message = "This is required, have input on this form."), 
                                             Length(min = 10, max = 100)])
    # accept username
    # will pass it to variable username
    username = StringField('Username', validators = [DataRequired(message = "This is required, have input on this form."), 
                                                     Length(min = 7, max = 35)]) 
    # accept email 
    # will pass it to variable email 
    email = StringField('Email', validators = [DataRequired(message = "This is required, have input on this form."),
                                               Email()])
    # accept password 
    # will pass it to variable password 
    password = PasswordField('Password', validators=[DataRequired(message = "Password should be minimum of 10 and maximum of 40."),
                                                     Length(min = 10, max = 40)])
    # accept confirmation of password 
    # will pass it to variable confirm_password 
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message = "Confirm your password."),
                                                     Length(min = 10, max = 40), EqualTo('password')])
    # accept phone number 
    # will pass it to the variable phone_number
    phone_number = StringField('Phone Number', validators = [DataRequired(message = "This is a required field."),
                                                             Length(min = 11, max = 11, message = "Phone number must be 11 digits and starts with 0."),
                                                             Regexp("^[0-9]+$", message = "Phone number must consist of numeric digits only.")])
    # accept birth date 
    # will pass it to the variable birth_date 
    birth_date = DateField('Birth Date', format = "%m/%d%/%Y", 
                                         validators = [DataRequired(message = 'Birthday is required!')])
    # accept gender 
    # will pass it to the variable gender 
    gender = RadioField('Gender', choices = [('Male'), ('Female'), ('Prefer not to say')],
                                    validators = [DataRequired(message = "State your gender...")])
    # accept street address 
    # will pass it to the variable street_address
    street_address = StringField('Street Address', validators =[DataRequired(message = "Address is important!"),
                                                                Length(min = 10, max = 100)])   
    # accept country 
    # will pass it to the variable country 
    country = SelectField('Country', choices=[('Country'), ('Philippines'), ('UK'), ('USA'), ('Japan')],
                                        validators=[DataRequired(message = "Pick your country!")])
    # accept city 
    # will pass it to the variable city 
    city = StringField('City', validators = [DataRequired(message = "State your city!"),
                                             Length(min = 1, max = 100)])
    # accept submit button 
    # will pass it to variable submit 
    submit = SubmitField('Submit')


class Login(FlaskForm):
    
    # accepting username 
    # will pass it to variable username 
    username = StringField('Username', validators = [DataRequired(message = "This is required, have input on this form."), 
                                                     Length(min = 7, max = 35)]) 
    # accept password 
    # will pass it to variable password 
    password = PasswordField('Password', validators=[DataRequired(message = "Password should be minimum of 10 and maximum of 16."),
                                                     Length(min = 10, max = 16)]) 
    # accept boolean to let the user have choice to stay login 
    # will pass it to the variable remember 
    remember = BooleanField('Remember me')
    
    # accept login button 
    # will pass it to variable Login 
    submit = SubmitField('Login')
    

class ForgotPassword():
    
    # accepting email for password change. 
    # will pass it to variable email
    email = StringField('Email', validators = [DataRequired(message = "This is required, have input on this form."),
                                               Email()])
    # accept login button 
    # will pass it to variable Login 
    submit = SubmitField('Submit')
    

