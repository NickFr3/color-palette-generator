from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans


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


@app.route("/get-palette", methods=["GET", "POST"])
def output():
    """Show generated palette"""
    if request.method == "POST":
        # Open image using Pillow
        img = Image.open(request.files("image"))

        # Get size of image
        width, height = img.size

        # Resize image to lower computational load if bigger than 1080p
        if width > 1920 or height > 1080:
            # Calculate new size while maintaining same aspect ratio
            aspect_ratio = width / height

            if width > height:
                new_width = 1920
                new_height = int(new_width / aspect_ratio)

            else:
                new_height = 1080
                new_width = int(new_height * aspect_ratio)

            # Resize the image
            img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Get list of pixels as list of tuples containing RGB values
        pixels = list(img.getdata())
        # Map list of pixels as a 2d array
        pixels = np.array(pixels)  
        # Cluster pixel to gather macro groups (5 colors hardcoded for now)
        cluster = KMeans(n_clusters=5)
        cluster.fit(pixels)
        # Get colors as an Array of RGB values arrays
        colors = cluster.cluster_centers_

        # Convert array or RGBs to array of HEX codes