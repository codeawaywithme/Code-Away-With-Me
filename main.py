from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from os import environ, path
from dotenv import load_dotenv
import config
import smtplib

#TODO Add all files to requirements.txt

# Create App
app = Flask(__name__)
app.config.from_pyfile('config.py')

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# Get year for copyright
year = date.today().strftime(("%Y"))

#TODO connect DB for email list, blogs, login for admin user to add content
#TODO Ensure REST architechture used

# Set up routes
@app.route('/', methods=["POST", "GET"])
def get_home():
    #TODO create flash messages for already entered emails
    signed_up = False
    if request.method == "POST":
        email = request.form["email"]
        signed_up = True
        send_email(email)
    return render_template("/pages/home.html", year=year, signed_up=signed_up)

@app.route('/construction')
def get_construction():
    return render_template("/pages/construction.html", year=year)

@app.route('/blog')
def get_blog():
    return render_template("/pages/blog.html", year=year)

@app.route('/blog_sample')
def get_blog_sample():
    return render_template("/working_files/blog_template.html")

#TODO move non routing functions to new py file
def send_email(email):
    # TODO update mail to use Flask-mail instead of smtplib
    # TODO change email to autosend welcome email to new member
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=environ.get('MY_EMAIL'), password=environ.get('PASSWORD'))
        connection.sendmail(
            from_addr=environ.get('MY_EMAIL'),
            to_addrs= environ.get('MY_EMAIL'),
            msg=f"Subject: New Subscriber to Newsetter!\n\n"
                f"Your new subscriber's email is {email}"
        )

# Run app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
