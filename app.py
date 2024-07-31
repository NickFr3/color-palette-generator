from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session


# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Main Page"""
    return render_template("index.html")


@app.route("/get-palette")
def output():
    """Show generated palette"""
    #TODO

    # Open image using Pillow
    # (Optional) Resize image to lower computational load
    # Iterate over each pixel
    # Cluster pixel to gather macro groups (5 colors hardcoded for now)
    # Return palette codes