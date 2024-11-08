import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect, abort
import pygal
import csv
from api_service import *
from graph_generator import generate_graph
import requests

# make a Flask application object called app
app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'


# use the app.route() decorator to create a Flask view function called index()
@app.route('/', methods=('GET','POST'))
def index():
    #create empty list for rows of csv stock data
    stocks = []
    #initialize empty chart variable
    chart = None

    #open csv file
    with open("stocks.csv", "r") as file:
        #create reader object
        csvreader = csv.DictReader(file)

        #convert csv data into list
        stocks = [row for row in csvreader]

    #if page was requested with POST
    if request.method == 'POST':

        #get the form data
        #display errors if no selections are made
        stock_symbol = request.form.get('stock')
        if not stock_symbol:
            flash("You must select a stock symbol!")

        chart_type = request.form.get('graph')
        if not chart_type:
            flash("You must select a chart type!")

        time_series_function = request.form.get('time_series')
        if not time_series_function:
            flash("You must select a time series!")
        
        begin_date = request.form.get('start_date')
        if not begin_date:
            flash("You must select a start date!")

        end_date = request.form.get('end_date')
        if not end_date:
            flash("You must select an end date!")

        #add error-checking for begin and end dates
        print(stock_symbol, chart_type, time_series_function, begin_date, end_date)
    
        #generate url for api
        time_series_name = convert_time_series(time_series_function)
        url = construct_url(BASE_URL, time_series_name, stock_symbol, INTERVAL, API_KEY)

        try:
            # Get JSON data from API
            response = requests.get(url)
            # Raise an HTTPError if the HTTP request gives unsuccessful status code
            response.raise_for_status() 
            stock_data = response.json()
            
            # Check to see if full json stock data loaded
            # If full json stock data is loaded, generate graph with user's selections
            if not stock_data:
                print("Error fetching stock data: please check the stock symbol and try again.")
            else:
                chart = generate_graph(stock_symbol, stock_data, chart_type, begin_date, end_date)
                
        except:
            print("Failed to gather necessary inputs. Please restart the program.")


    return render_template('index.html', stock_list=stocks, chart=chart)

    

app.run(port=5008)