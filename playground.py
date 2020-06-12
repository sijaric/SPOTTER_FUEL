from calculateFuelPrice import FuelPriceCalculator


if __name__ == '__main__':
    fuel_calc = FuelPriceCalculator()

    result = fuel_calc.calculate_fuel_price(31.000000, -100.000000, 43.000000, -75.000000)
    print(result)