# This is imported from the package blogpose. 
# the app is in the __init__ of the blogpose module. 
from blogpose import app, db 

if __name__ == "__main__":
    # This application context will run the db.create_all() if the databse is not yet existing. 
    # else, if the tables exists, then it will not modify the existing tables. 
    with app.app_context():
        db.create_all()
        app.run(debug=True)