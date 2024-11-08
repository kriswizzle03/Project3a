import pygal
from lxml import etree
from datetime import datetime

def generate_graph(stock_symbol, stock_data, chart_type, begin_date, end_date):
    """Generates and displays a graph based on the stock data and user inputs."""
    
    # create empty variables to hold JSON data from api
    #api returns data from dates outside specified range
    #need variable to hold only needed data
    processed_data = {}
    dates = []
    opening_prices = []
    high_prices = []
    low_prices = []
    closing_prices = []

    # Determine the time series to use
    if 'Time Series (5min)' in stock_data: 
        time_series = stock_data['Time Series (5min)']
    elif 'Time Series (Daily)' in stock_data:
        time_series = stock_data['Time Series (Daily)']
    elif 'Weekly Time Series' in stock_data:
        time_series = stock_data['Weekly Time Series']
    elif 'Monthly Time Series' in stock_data:
        time_series = stock_data['Monthly Time Series']
    else:
        print("No valid time series found in the stock data.")
        return
    

    # Filter data by date range
    for date, data in time_series.items():
        if date >= begin_date and date <= end_date:
            dates.append(date)
            processed_data[date] = data
            
            # debugging
            print(processed_data[date])
            print(date)
        
            try:
                opening_prices.append(float(data['1. open']))  # Change this to the price you want to plot
                high_prices.append(float(data['2. high']))
                low_prices.append(float(data['3. low']))
                closing_prices.append(float(data['4. close']))

            except KeyError:
                    print(f"Missing data for date: {date}")
    #debugging
    print(opening_prices)

    # Generate the graph
    if chart_type == "1":
        graph = pygal.Bar(x_label_rotation=45)
        graph.title = f"Stock Data for {stock_symbol}: {begin_date} to {end_date}"
    else:
        graph = pygal.Line(x_label_rotation=45)
        graph.title = f"Stock Data for {stock_symbol}: {begin_date} to {end_date}"

    # Set x_labels and add data
    graph.x_labels = dates
    graph.add('Open', opening_prices)
    graph.add('High', high_prices)
    graph.add('Low', low_prices)
    graph.add('Close', closing_prices)

    # Save the graph
    graph.render_to_file('stock_prices_graph.svg')
    return graph.render_data_uri()

    # Open the graph in the default web browser
    # webbrowser.open('stock_prices_graph.svg')
