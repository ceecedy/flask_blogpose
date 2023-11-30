from flask import Blueprint, render_template, url_for, flash, redirect, request, abort, jsonify

# importing a login function to the function login 
# current_user is a variable from flask_login that holds a user data. 
# current_user can be used to modify certain current user tasks. 
# for login required function, just see the implementation for more details
from flask_login import current_user, login_required

# db is from the init of the blogpose package
from blogpose import db

# Importing Post Model. 
from blogpose.models import Post, Comment, Like

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


@posts.route('/post_comment', methods=['POST', 'GET'])
def post_comment():
    post_id = request.form.get('post_id')
    comment_content = request.form.get('comment_content')

    # Validate and save the comment to the database
    # (You'll need to adjust this based on your actual models and database structure)
    post = Post.query.get(post_id)
    if post:
        new_comment = Comment(content=comment_content, user=current_user, post=post)
        db.session.add(new_comment)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Comment posted successfully'})

    return jsonify({'success': False, 'message': 'Invalid post ID'})


@posts.route('/like_post', methods = ['POST'])
def like_post():
    post_id = request.form.get('post_id')
    user_id = request.form.get('user_id')
    
    # check if the specific user already liked the post. 
    existing_like = Like.query.filter_by(post_id = post_id, user_id = user_id).first()
    
    # if not none
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        liked = False
    
    # if none 
    else:
        new_like = Like(post_id = post_id, user_id = user_id)
        db.session.add(new_like)
        db.session.commit()
        liked = True
    
    # get the total number likes of the post 
    total_likes = Like.query.filter_by(post_id = post_id).count()
    
    return jsonify({'success': True, 'liked': liked, 'total_likes': total_likes})
    








# A func can have multiple decorators. 
# You can just let the development server run while you make changes to your code. 