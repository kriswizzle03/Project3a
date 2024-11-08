import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
import pygal
import csv

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'




# use the app.route() decorator to create a Flask view function called index()
@app.route('/', methods=('GET','POST'))
def index():
    #create empty list for rows of csv stock data
    stocks = []

    #open csv file
    with open("stocks.csv", "r") as file:
        #create reader object
        csvreader = csv.DictReader(file)

        #convert csv data into list
        stocks = [row for row in csvreader]

    #if page was requested with POST
    if request.method == 'POST':
        #get the form data
        stock_symbol = request.form.get('stock')
        chart_type = request.form.get('graph')
        time_series_function = request.form.get('time_series')
        begin_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        print(stock_symbol, chart_type, time_series_function, begin_date, end_date)
    
    return render_template('index.html', stock_list=stocks)

    







app.run(port=5008)