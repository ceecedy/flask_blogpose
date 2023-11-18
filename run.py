# This is imported from the package blogpose. 
# the app is in the __init__ of the blogpose module. 
from blogpose import create_app, db 

# importing User for token cleaning purposes. 
from blogpose.models import User

# getting an instance of create_app 
app = create_app()

if __name__ == "__main__":
    # This application context will run the db.create_all() if the databse is not yet existing. 
    # else, if the tables exists, then it will not modify the existing tables. 
    with app.app_context():
        # Call the cleanup_expired_tokens method before each request
        db.create_all()
        User.cleanup_expired_tokens()
        app.run(debug=True)