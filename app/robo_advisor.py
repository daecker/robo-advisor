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
latest_close = parsed_response["Time Series (Daily)"]["2019-02-20"]["4. close"]


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
#print("RECENT HIGH: $101,000.00")
#print("RECENT LOW: $99,000.00")
#print("-------------------------")
#print("RECOMMENDATION: BUY!")
#print("RECOMMENDATION REASON: TODO")
#print("-------------------------")
#print("HAPPY INVESTING!")
#print("-------------------------")