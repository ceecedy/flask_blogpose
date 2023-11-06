# This file is where I create the script for creating the database. 
# This can go in terminal but I prefer to have one separate file for this. 

# importing app because app is the name of my flask application instance. 
# importing db because db is the name of my databse instance using SQL Alchemy. 
from blogpose import app, db, User, Post 

# It is essential to make application context for creating database.   
with app.app_context():
    # list of database operations should be inside application context. 
    
    # getting the user. 
    user = User.query.filter_by(username='ceecedie').first()
    
    # if user exists.
    if user:
        # get all user's posts. 
        user_posts = user.posts
        
        # print all the post of the specific user.
        for post in user_posts:
            print(post.title, post.date_posted)
            
    # if user was not found
    else:
        print("User not found")
        
with app.app_context():
    post = Post.query.first()
    print(post.Author)
