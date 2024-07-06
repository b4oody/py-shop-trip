from decimal import Decimal
from app.car import Car


class Shop:
    shops_list = []

    def __init__(self, shops: list) -> None:
        for shop in shops:
            self.shops_list.append(shop)

    def cost_for_products_in_every_store(self, product_cart: dict) -> dict:
        sum_total = {}
        for shop in self.shops_list:
            sum_ = Decimal("0.00")
            for product, quantity in product_cart.items():
                if product in shop["products"]:
                    sum_ += Decimal(
                        quantity) * Decimal(shop["products"][product])
            sum_total[shop["name"]] = sum_
        return sum_total

    def total_cost(
            self,
            product_cart: dict,
            location: tuple,
            car: Car
    ) -> dict:
        cost_of_products = self.cost_for_products_in_every_store(product_cart)
        cost_of_fuel = car.cost_of_fuel(location, self.shops_list)
        full_cost_every_shop = {}
        for name_shop, cash in cost_of_products.items():
            if name_shop in cost_of_fuel.keys():
                full_cost_every_shop[name_shop] = (cash
                                                   + cost_of_fuel[name_shop])
        return full_cost_every_shop
