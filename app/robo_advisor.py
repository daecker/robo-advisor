# app/robo_advisor.py

import requests
import json




#INFO INPUTS

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

response = requests.get(request_url)
print(type(response))
print(response.status_code)
print(response.text)

parsed_response = json.loads(response.text) #convert response variable from a string to a dictionary

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

tsd = parsed_response["Time Series (Daily)"]
dates = list(tsd.keys()) #TODO need to sort to ensure latest day is first
latest_day = dates[0] #pulls latest day 
latest_close = tsd[latest_day]["4. close"]

#recent_high = max of all high prices
high_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    high_prices.append(float(high_price))
recent_high = max(high_prices)

def to_usd(my_price):
    return "${0:.2f}".format(my_price)

#INFO OUTPUTS

#print("-------------------------")
#print("SELECTED SYMBOL: XYZ")
#print("-------------------------")
#print("REQUESTING STOCK MARKET DATA...") #look at shopping cart
#print("REQUEST AT: 2018-02-20 02:00pm")
#print("-------------------------")
print("LATEST DAY: " + last_refreshed)
print("LATEST CLOSE: " + to_usd(float(latest_close)))
print("RECENT HIGH: " + to_usd(float(recent_high)))
#print("RECENT LOW: $99,000.00")
#print("-------------------------")
#print("RECOMMENDATION: BUY!")
#print("RECOMMENDATION REASON: TODO")
#print("-------------------------")
#print("HAPPY INVESTING!")
#print("-------------------------")