# app/robo_advisor.py

import csv
import json
import os

import requests


def to_usd(my_price):
    return "${0:.2f}".format(my_price)


#INFO INPUTS

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

response = requests.get(request_url)
#print(type(response))
#print(response.status_code)
#print(response.text)

parsed_response = json.loads(response.text) #convert response variable from a string to a dictionary

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) #TODO need to sort to ensure latest day is first
latest_day = dates[0] #pulls latest day 
latest_close = tsd[latest_day]["4. close"]

#recent_high = max of all high prices
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
    low_price = tsd[date]["3. low"]
    low_prices.append(float(low_price))
    
recent_high = max(high_prices)
recent_low = min(low_prices)



csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["city","name"])
    writer.writeheader()
    writer.writerow({"city": "New York", "name": "Yankees"})

#INFO OUTPUTS

#print("-------------------------")
#print("SELECTED SYMBOL: XYZ")
#print("-------------------------")
#print("REQUESTING STOCK MARKET DATA...") 
#print("REQUEST AT: 2018-02-20 02:00pm") #look at shopping cart
#print("-------------------------")
print("LATEST DAY: " + last_refreshed)
print("LATEST CLOSE: " + to_usd(float(latest_close)))
print("RECENT HIGH: " + to_usd(float(recent_high)))
print("RECENT LOW: " + to_usd(float(recent_low)))
#print("-------------------------")
#print("RECOMMENDATION: BUY!")
#print("RECOMMENDATION REASON: TODO")
#print("-------------------------")
print("WRITING DATA TO " + csv_file_path) #use pandas package
print("-------------------------")
#print("HAPPY INVESTING!")
#print("-------------------------")

