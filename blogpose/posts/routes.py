from flask import Blueprint, render_template, url_for, flash, redirect, request, abort

# importing a login function to the function login 
# current_user is a variable from flask_login that holds a user data. 
# current_user can be used to modify certain current user tasks. 
# for login required function, just see the implementation for more details
from flask_login import current_user, login_required

# db is from the init of the blogpose package
from blogpose import db

# Importing Post Model. 
from blogpose.models import Post

# importing NewPost form from the very root package. 
from blogpose.posts.forms import NewPost


# instantiating a blueprint named users
posts = Blueprint('posts', __name__)


@posts.route("/feeds")
@login_required
def feeds():
    # getting all the post in the database and set it to one variable 
    # posts = Post.query.all()
    # making this a paginate method to make a object of all the data in the Post model to become paginated. 
    # the order_by method after query method is to order the data inside the Post model according to 
    #   the parameter inside the order_by
    posts = Post.query.order_by(Post.date_posted.desc()).paginate()
    return render_template("feeds.html", title = "Feeds", posts = posts)


@posts.route("/post/new", methods=['GET', 'POST'])
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
        return redirect(url_for('posts.feeds'))
    
    return render_template("create_post.html", title = "New Post", form = form, legend = "New Post") 


# the brackets inside the route is a variable that is interchangeable depending on the post to update. 
# the int: syntax is to ensure that the post_id will be an int. 
@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template('post.html', title = post.title, post = post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for("posts.post", post_id = post.id))
    
    elif request.method == "GET":
        form.title.data = post.title     
        form.content.data = post.content
        
    return render_template("create_post.html", title = "Update Post", form = form, legend = "Update Post") 


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
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
    return redirect(url_for('posts.feeds'))




# A func can have multiple decorators. 
# You can just let the development server run while you make changes to your code. 