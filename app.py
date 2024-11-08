import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
import pygal

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'



# use the app.route() decorator to create a Flask view function called index()
@app.route('/')
def index():

    return render_template('index.html')

    







app.run(port=5008)