from flask import Flask, redirect, render_template, request, send_from_directory
from db import DatabaseWrapper
from shorten import shorten_url

app = Flask(__name__)
db_wrapper = DatabaseWrapper()
server_part = "http://localhost:5000/"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<short>")
def redirect_short(short):
    if (url := db_wrapper.lookup_short(short)) is not None:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"http://{url}"
        return redirect(url, 301)
    return render_template("error.html", server_part=server_part, short=short)


@app.route("/_shorten", methods=("POST",))
def shorten():
    url = request.form['url']
    short = shorten_url(url, db_wrapper)
    return render_template("index.html", server_part=server_part, short=short)


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])
