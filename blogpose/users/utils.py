# importing secrets to process the profile picture to get secured. 
# importing os also for the process on where to put picture. 
import secrets, os

# importing image resizer module name pillow 
from PIL import Image

# importing message from flask-mail for additional mail functions
from flask_mail import Message

# url_for import for the send email 
# importing current app 
from flask import url_for, current_app

from blogpose import mail

# importing User model 
from blogpose.models import User


# function to process the uploads of user to their profile pictures. 
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
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


# function to send the current email. 
def send_reset_email(user):
    token = user.get_reset_token()
    # sending the email using url, using msg class from flask-mail
    msg = Message("Password Reset Request", sender = "blogpose@support.com", recipients = [user.email])
    
    msg.body = f''' To reset your password, visit the following link:
    
    {url_for('users.reset_token', token = token, _external = True)}
    
    If you did not make this request, simply ignore this message. 
    '''
    
    # finally passing the message to the email of the user.
    mail.send(msg)