# app/robo_advisor.py

import csv
import json
import os
import datetime
import requests

from dotenv import load_dotenv

load_dotenv()

def to_usd(my_price):
    return "${0:.2f}".format(my_price)

ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", "OOPS, please set env var called 'ALPHAVANTAGE_API_KEY'")

date_start = datetime.datetime.now()
formated_date_start = date_start.strftime("%Y-%m-%d %I:%M %p")

#INFO INPUTS

while True:
    stock_symbol = input("Please Enter a Valid Stock Symbol: ")
    request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+stock_symbol+"&"+"apikey="+ALPHAVANTAGE_API_KEY
    response = requests.get(request_url)
    if 'Error' in response.text:
        print("You entered an invalid stock symbol. Please try again ")
    else:
        break


parsed_response = json.loads(response.text) #convert response variable from a string to a dictionary

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) #TODO need to sort to ensure latest day is first
sorted_dates = sorted(dates, reverse=True)
latest_day = sorted_dates[0] #pulls latest day 
#print("LATEST DAY", latest_day) #use print to test the sorting function
latest_close = tsd[latest_day]["4. close"]


#recent_high = max of all high prices
high_prices = []
low_prices = []
close_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))
    close_price = tsd[date]["4. close"]
    close_prices.append(float(close_price))
    
recent_high = max(high_prices)
recent_low = min(low_prices)
average_close = sum(close_prices)/len(close_prices)



csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]

with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()
    for date in dates:
        daily_pries = tsd[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_pries["1. open"],
            "high": daily_pries["2. high"],
            "low": daily_pries["3. low"],
            "close": daily_pries["4. close"],
            "volume": daily_pries["5. volume"],
            })

#INFO OUTPUTS

print("-------------------------")
print("SELECTED SYMBOL: " + stock_symbol)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...") 
print("REQUEST AT: " + formated_date_start)
print("-------------------------")
print("DATA LAST REFRESHED: " + last_refreshed)
print("LATEST CLOSE: " + to_usd(float(latest_close)))
print("RECENT HIGH: " + to_usd(float(recent_high)))
print("RECENT LOW: " + to_usd(float(recent_low)))
print("-------------------------")

#RECOMMENDATION
if average_close > float(latest_close):
    print("RECOMMENDATION: BUY!")
    print("RECOMMENDATION REASON: The average close price is greater than the most recent close price")
else:
    print("RECOMMENDATION: SELL!")
    print("RECOMMENDATION REASON: The stock is over valued. The average close price is lower than the most recent close price")
#print("-------------------------")
print("WRITING DATA TO " + csv_file_path)
print("-------------------------")
#print("HAPPY INVESTING!")
#print("-------------------------")

