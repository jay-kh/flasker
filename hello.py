# ==================================== Import Section ========================================


from flask import Flask, render_template, flash

# to create a form object
from flask_wtf import FlaskForm

# string input box, submit button, imagefield for images
from wtforms import StringField, SubmitField

# if something is not filled or empty, then gives warning
# different validators for email, password, etc
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ======================================= App Config Section ========================================

# create a flask instance
# __name__ helps flask search for project files
app = Flask(__name__)


# add Database
# URI - uniform resource indicator -- indicates where our database is
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

# initialize the data base
db = SQLAlchemy(app)


# with form there is csrf token -- it will create a secrete key with form,
# and behind the scene it will synch with another secrete key.
# making sure that hacker won't hijack the form,
# we need to create a secrete key for backend
app.config["SECRET_KEY"] = "This is a secrate key which not ment to be shared"

# ==================================== Model Section ========================================


# create a model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # create string
    def __repr__(self):
        return "<name %r>" % self.name


# To solve RuntimeError: Working outside of application context.
# This typically means that you attempted to use functionality that needed
# the current application.
# To solve this, set up an application context
# with app.app_context().
with app.app_context():
    db.create_all()

# ===================================== Form Section =========================================


# create a form class
# inheriting with a flask form
class NamerForm(FlaskForm):
    name = StringField("Whats Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


# USER Form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


# ============================================== Views Section ======================================


# create name page
@app.route("/name", methods=["GET", "POST"])
def name():
    name = None

    # blank form
    form = NamerForm()

    # validate form
    if form.validate_on_submit():
        # if someone posted a name, it will be stored here
        name = form.name.data

        # it will clear the name-field for the next fill
        form.name.data = None

        flash("Form Submitted Successfully")

    return render_template("name.html", name=name, form=form)


## Fields
# BooleanField
# DateField
# DateTimeField
# DecimalField
# FileField
# HiddenField
# MultipleField
# FieldList
# FloatField
# FormField
# IntegerField
# PasswordField
# RadioField
# SelectField
# SelectMultipleField
# SubmitField
# StringField
# TextAreaField

## Validators
# DataRequired
# Email
# EqualTo
# InputRequired
# IPAddress
# Length
# MacAddress
# NumberRange
# Optional
# Regexp
# URL
# UUID
# AnyOf
# NoneOf


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


# user adds view
@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    name = None

    form = UserForm()

    if form.validate_on_submit():
        # grab all the email id from database and match with user input
        # it should be non because email should be unique
        user = Users.query.filter_by(email=form.email.data).first()

        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()

        name = form.name.data
        form.name.data = ""
        form.email.data = ""
        flash("User Added Successfully!")

    our_users = Users.query.order_by(Users.date_added)

    return render_template("add_user.html", form=form, name=name, our_users=our_users)


# =============================================== Application Run Section =================================

if __name__ == "__main__":
    app.run(debug=True)
