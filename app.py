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
    #initialize chart
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
        stock_symbol = request.form.get('stock')
        chart_type = request.form.get('graph')
        time_series_function = request.form.get('time_series')
        begin_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        print(stock_symbol, chart_type, time_series_function, begin_date, end_date)
    
        #generate url for api
        time_series_name = convert_time_series(time_series_function)
        url = construct_url(BASE_URL, time_series_name, stock_symbol, INTERVAL, API_KEY)

        try:
            # Get JSON data from API
            response = requests.get(url)
            response.raise_for_status()  # Raises an HTTPError if the HTTP request in the case of an unsuccessful status code
            stock_data = response.json()
            

            # Check if the expected data structure is present
            if not stock_data:
                print("Error fetching stock data: please check the stock symbol and try again.")
            else:
                chart = generate_graph(stock_symbol, stock_data, chart_type, begin_date, end_date)
                

        except:
            print("Failed to gather necessary inputs. Please restart the program.")


    return render_template('index.html', stock_list=stocks, chart=chart)

    







app.run(port=5008)