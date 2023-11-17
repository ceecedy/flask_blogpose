from flask import Blueprint, render_template

# instantiating a blueprint named users
main = Blueprint('main', __name__)


# This app route is a route api. This is basically the home route. 
@main.route("/") 
@main.route("/home")
def home():
    return render_template("home.html")


@main.route("/about")
def about():
    return render_template("about.html", title = "About")



# A func can have multiple decorators. 
# You can just let the development server run while you make changes to your code. 