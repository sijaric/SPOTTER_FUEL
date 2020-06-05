
# import http.client
# please excuse all these imports, the regular import math just wouldn't work for some reason that I haven't figured out
import math
from math import asin
from math import sqrt
from math import sin
from math import cos
from math import atan2
from math import degrees
import json
import http.client
from config import *
import us
from haversine import Haversine
import reverse_geocoder as rg

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


def loadDBDieselPrices():
    # fetching all available information about gas prices for all 50 US states
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type': "application/json",
        'authorization': APIKEY
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


# OUTPUT FOR DIESELPRICES
print(loadDBDieselPrices())

# HAVERSINE - DISTANCE AND CALCULATION OF POINTS ALONG ROUTES:


class Haversine:
    '''
    use the haversine class to calculate the distance between
    two lon/lat coordnate pairs.
    output distance available in kilometers, meters, miles, and feet.
    example usage: Haversine([lon1,lat1],[lon2,lat2]).feet

    '''

    def __init__(self, coord1, coord2):
        lon1, lat1 = coord1
        lon2, lat2 = coord2

        R = 6371000                               # radius of Earth in meters
        phi_1 = math.radians(lat1)
        phi_2 = math.radians(lat2)

        delta_phi = math.radians(lat2-lat1)
        delta_lambda = math.radians(lon2-lon1)

        a = math.sin(delta_phi/2.0)**2 +\
            math.cos(phi_1)*math.cos(phi_2) *\
            math.sin(delta_lambda/2.0)**2
        c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))

        self.meters = R*c                         # output distance in meters
        self.km = self.meters/1000.0              # output distance in kilometers
        self.miles = self.meters*0.000621371      # output distance in miles
        self.feet = self.miles*5280               # output distance in feet


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

refuelTimes = (int((distance/500)))

points = [origin]
latestpercent = 500/distance
while refuelTimes > 0:
    result = midpoint(o[0], o[-1], d[0], d[-1], latestpercent)
    points.append(result)
    latestpercent += 500/distance
    refuelTimes = refuelTimes-1
print(points)
print()
results = rg.search(points)
print(results)

# How many gallons? 5 miles/gallon
