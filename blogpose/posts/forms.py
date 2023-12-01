from flask_wtf import FlaskForm

# We will use StringField class from module wtforms to create a String object to accept a string input.
# TextAreaField class will make an object that has the content of the post in the Post form.
# SubmitField class from wtforms is used to create a button specialized in submitting data.
from wtforms import StringField, TextAreaField, SubmitField

# this import is to take files as input of the clients. 
# filefield is the class to accept the images. 
# fileallowed is the class to check and limit the validations of the input images. 
from flask_wtf.file import FileField, FileAllowed

# importing a class that will make sure that the input should not be empty. 
# the name of the class is "DataRequired" from module wtforms.validators. 
from wtforms.validators import DataRequired, Length


class NewPost(FlaskForm):
    
    # accept title input
    # will pass it to the title variable 
    title = StringField('Title', validators=[
        DataRequired(message = 'Title is required'), 
        Length(min = 1)
    ])
    
    # accept content 
    # will pass it to the content variable 
    content = TextAreaField('Content', validators=[
        DataRequired(message = 'Content is required')
    ])
    
    # accept images 
    # will pass it to the variable images 
    image = FileField('Upload Image(s)', validators=[
        FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    
    # accept submit button 
    # will pass it to the submit variable 
    submit = SubmitField('Post')