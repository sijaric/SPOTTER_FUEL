from dieselFetchAPI import FuelAPI
from haversine import Haversine
import reverse_geocoder as rg
import us


class FuelPriceCalculator():
    def __init__(self):
        self.fuel_api = FuelAPI()
        self.savedOutput = self.fuel_api.loadDBDieselPrices()

    def midpoint(self, lat1, long1, lat2, long2, per):
        return (lat1 + (lat2 - lat1) * per, long1 + (long2 - long1) * per)

    def calculate_fuel_price(self, src_lat, src_lng, dst_lat, dst_lng, mpg=6.5, interval=200):
        distance = Haversine((src_lat, src_lng), (dst_lat, dst_lng)).miles
        refuelTimes = int((distance/interval))
        latestpercent = interval/distance

        points = [(src_lat, src_lng)]
        while refuelTimes > 0:
            result = self.midpoint(src_lat, src_lng, dst_lat, dst_lng, latestpercent)
            points.append(result)
            latestpercent += interval/distance
            refuelTimes = refuelTimes-1
        results = rg.search(points)

        state_names = []
        for state in results:
            state_names.append(state["admin1"])

        state_codes = []
        for state_name in state_names:
            state = us.states.lookup(state_name)
            nameState = state.abbr
            state_codes.append(nameState)

        gallonsPerInterval = interval / mpg
        totalCost = 0
        for state_code in state_codes:
            totalCost += gallonsPerInterval * self.savedOutput[str(state_code)]

        return totalCost