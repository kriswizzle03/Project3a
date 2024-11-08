import pygal
from lxml import etree
from datetime import datetime

def generate_graph(stock_symbol, stock_data, chart_type, begin_date, end_date):
    """Generates and displays a graph based on the stock data and user inputs."""
    
    # api returns data from dates outside specified range
    # create empty dictionary to hold only needed JSON data from api
    # create empty lists for different price types
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
            #add dates to date list (will be used later for x-axis on graph)
            dates.append(date)
            processed_data[date] = data
            
            #add each price to its respective list
            opening_prices.append(float(data['1. open']))  
            high_prices.append(float(data['2. high']))
            low_prices.append(float(data['3. low']))
            closing_prices.append(float(data['4. close']))

    #sort data based on date (oldest to newest)
    sorted_dates = sorted(dates)
    sorted_opening_prices = [opening_prices[dates.index(date)] for date in sorted_dates]
    sorted_high_prices = [high_prices[dates.index(date)] for date in sorted_dates]
    sorted_low_prices = [low_prices[dates.index(date)] for date in sorted_dates]
    sorted_closing_prices = [closing_prices[dates.index(date)] for date in sorted_dates]

    print(sorted_dates)     
            #except KeyError:
              #  print(f"Missing data for date: {date}")

            

    # Generate the graph
    if chart_type == "1":
        graph = pygal.Bar(x_label_rotation=45, height=400)
        graph.title = f"Stock Data for {stock_symbol}: {begin_date} to {end_date}"
    else:
        graph = pygal.Line(x_label_rotation=45, height=400)
        graph.title = f"Stock Data for {stock_symbol}: {begin_date} to {end_date}"

    # Set x_labels and add data to graph
    graph.x_labels = sorted_dates
    graph.add('Open', sorted_opening_prices)
    graph.add('High', sorted_high_prices)
    graph.add('Low', sorted_low_prices)
    graph.add('Close', sorted_closing_prices)

    # return graph
    return graph.render_data_uri()

