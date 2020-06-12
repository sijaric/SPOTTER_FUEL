import os
import math
from math import asin, sqrt, sin, cos, atan2, degrees
import json
import http.client
import us


'''
INPUT: NOTHING
OUTPUT is a 
    DICTIONARY:
        KEY: STATE ABBREV. 2 LETTER CODE
        VALUE: DIESEL PRICE IN USD (TYPE: FLOAT)

        IF SUCCESSFUL WILL HAVE:
            {"success": True}
        ELSE WILL HAVE: 
            {"success": False}

API WEBSITE:
    https://collectapi.com/api/gasPrice/gas-prices-api/stateUsaPrice
'''

class FuelAPI():
    def __init__(self):
        self.APIKEY = os.environ.get('APIKEY')
        self.savedOutput = self.loadDBDieselPrices()

    def loadDBDieselPrices(self):
        # fetching all available information about gas prices for all 50 US states
        conn = http.client.HTTPSConnection("api.collectapi.com")
        headers = {
            'content-type': "application/json",
            'authorization': self.APIKEY
        }
        conn.request("GET", "/gasPrice/allUsaPrice", headers=headers)
        res = conn.getresponse()
        # WE RECIEVE A RESPONSE > DECODE INTO A STRING > CONVERTS JSON INTO DICTIONARY
        data = res.read()
        string = data.decode('utf-8')
        dict_res = json.loads(string)  # load into dictionary
        successCheck = dict_res["success"]  # TRUE/FALSE
        '''
        Dictionaries:
        Methods:
        .keys() - returns keys
        .items() - keys and values

        EXPLORE A DICTIONARY
        WHEN YOU GET A RESULT YOU WANT TO SEE WHAT ARE THE KEYS SO THAT YOU CAN FIGURE OUT
        WHAT DATA YOU NEED

        .keys() -> SO THAT WE KNEW SUCCESS AND RESULT

        type() -> TYPE OF RESPONSE

        results : [{}, {}]

        API CAN FAIL: 
        CHECK AGAINST THAT
        '''

        if successCheck:
            output = {"success": True}
            for state_dictionary in dict_res["result"]:
                name = state_dictionary['name']
                state = us.states.lookup(name)
                name = state.abbr
                dieselPrice = state_dictionary['diesel']
                output[name] = float(dieselPrice)
            return output
        else:
            # EITHER API REQUEST FAILED or LIMIT of 100 requests a month was hit
            return {"success": False}


if __name__ == '__main__':
    # I'm experimenting with a route Texas --> New York, but will replace these two inputs with
    # user inputs later on once the system is ready!
    print(Haversine((31.000000, -100.000000), (43.000000, -75.000000)).miles)

    origin = (31.000000, -100.000000)
    destination = (43.000000, -75.000000)

    o = list(origin)
    d = list(destination)

    distance = Haversine(origin, destination).miles


    def midpoint(lat1, long1, lat2, long2, per):
        return (lat1 + (lat2 - lat1) * per, long1 + (long2 - long1) * per)


    # This tells me how many (equally spaced) points along the route I need to find,
    # considering that the initial point of refueling happens at the origin
    # 3 refuelling along the route in this case!

    intervals = 200

    refuelTimes = (int((distance/intervals)))

    points = [origin]
    latestpercent = intervals/distance
    while refuelTimes > 0:
        result = midpoint(o[0], o[-1], d[0], d[-1], latestpercent)
        points.append(result)
        latestpercent += intervals/distance
        refuelTimes = refuelTimes-1
    print(points)
    print()
    results = rg.search(points)
    print(results)

    states = []
    for i in results:
        states.append(i["admin1"])

    states2 = []
    for i in states:
        state = us.states.lookup(i)
        nameState = state.abbr
        states2.append(nameState)

    print(states2)

    # our interval is 200 miles, and one gallon takes you 5 miles, so we need 40 gallons per interval
    gallonsPerInterval = 40
    totalCost = 0
    API = FuelAPI()
    print(API.savedOutput)
    for i in states2:
        totalCost += gallonsPerInterval*API.savedOutput[str(i)]

    print(totalCost)

    # How many gallons? 5 miles/gallon

    # Canada exceptions

    # save API output into a file that we can access later
