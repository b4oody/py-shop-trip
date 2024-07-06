from decimal import Decimal
from math import sqrt


class Car:
    def __init__(
            self,
            fuel_price: float,
            brand: str,
            consumption: Decimal
    ) -> None:
        self.fuel_price = Decimal(fuel_price)
        self.brand = brand
        self.consumption = consumption

    def cost_of_fuel(
            self,
            location: tuple,
            shops_list: list
    ) -> dict:
        cost_fuel_every_shop = {}
        for shop in shops_list:
            distance = Decimal(
                sqrt(((shop["location"][0] - location[0]) ** 2)
                     + ((shop["location"][1] - location[1]) ** 2)))
            amount_of_liters_per_distance = (distance * self.consumption
                                             / Decimal("100"))
            cost_full_distance_with_return = (amount_of_liters_per_distance
                                              * self.fuel_price * Decimal("2"))
            cost_fuel_every_shop[shop["name"]] = cost_full_distance_with_return
        return cost_fuel_every_shop
