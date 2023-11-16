from flask import Flask, render_template, flash

# to create a form object
from flask_wtf import FlaskForm

# string input box, submit button, imagefield for images
from wtforms import StringField, SubmitField

# if something is not filled or empty, then gives warning
# different validators for email, password, etc
from wtforms.validators import DataRequired


# with form there is csrf token -- it will create a secrete key with form,
# and behind the scene it will synch with another secrete key.
# making sure that hacker won't hijack the form,
# we need to create a secrete key for backend

# create a flask instance
# __name__ helps flask search for project files
app = Flask(__name__)
app.config["SECRET_KEY"] = "This is a secrate key which not ment to be shared"


# create a form class
# inheriting with a flask form
class NamerForm(FlaskForm):
    name = StringField("Whats Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


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


if __name__ == "__main__":
    app.run(debug=True)
