from flask import Flask, render_template

# create a flask instance
# __name__ helps flask search for project files
app = Flask(__name__)

# jinja2 Filters
# safe - send html apply tags
# capitalize
# lower
# upper
# title
# trim - remove trailing space from end
# striptags - send html without tags


# create a route decorator
# route binds url to function
@app.route("/")
def index():
    first_name = "Jhon"
    stuff = "This is <strong>Bold</strong> Text."
    fav_pizza = ["cheese", "mushroom", 41]
    # return "<h1>Hello World!</h1>"
    return render_template(
        "index.html", first_name=first_name, stuff=stuff, fav_pizza=fav_pizza
    )


# localhost:5000/user/jay
@app.route("/user/<name>")
def user(name):
    return render_template("user.html", user_name=name)


# Custom Error Pages


# invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


# Internal server error
@app.errorhandler(500)
def internal_error_error(e):
    return render_template("500.html")


if __name__ == "__main__":
    app.run(debug=True)
