from math import sqrt
from decimal import Decimal, ROUND_HALF_UP
from app.shop import Shop
from app.car import Car


class Customer:
    def __init__(self, customer: dict, shops: Shop, fuel_price: float) -> None:
        self.first_name = customer["name"]
        self.product_cart = customer["product_cart"]
        self.location = customer["location"]
        self.money = Decimal(customer["money"])
        self.fuel = Car(
            fuel_price,
            customer["car"]["brand"],
            Decimal(customer["car"]["fuel_consumption"]).
            quantize(Decimal("0.00"))
        )
        self.shops = shops.shops_list

    def cost_for_products_in_every_store(self) -> dict:
        sum_total = {}
        for shop in self.shops:
            sum_ = Decimal("0.00")
            for product, quantity in self.product_cart.items():
                if product in shop["products"]:
                    sum_ += (Decimal(quantity)
                             * Decimal(shop["products"][product]))
            sum_total[shop["name"]] = sum_
        return sum_total

    def cost_of_fuel(self, fuel_price: float) -> dict:
        fuel_price = Decimal(fuel_price)
        cost_fuel_every_shop = {}
        for shop in self.shops:
            distance = Decimal(
                sqrt(((shop["location"][0] - self.location[0]) ** 2)
                     + ((shop["location"][1] - self.location[1]) ** 2)))
            amount_of_liters_per_distance = (distance * self.fuel.consumption
                                             / Decimal("100"))
            cost_full_distance_with_return = (amount_of_liters_per_distance
                                              * fuel_price * Decimal("2"))
            cost_fuel_every_shop[shop["name"]] = cost_full_distance_with_return
        return cost_fuel_every_shop

    def total_cost(self) -> dict:
        cost_of_products = self.cost_for_products_in_every_store()
        cost_of_fuel = self.cost_of_fuel(self.fuel.fuel_price)
        full_cost_every_shop = {}
        for name_shop, cash in cost_of_products.items():
            if name_shop in cost_of_fuel.keys():
                full_cost_every_shop[name_shop] = (cash
                                                   + cost_of_fuel[name_shop])
        return full_cost_every_shop

    @staticmethod
    def format_price(price: Decimal) -> str:
        if price == price.to_integral():
            return f"{price:.0f}"
        else:
            return f"{price:.1f}"

    def return_(self) -> str:
        full_cost_for_every_shop = self.total_cost()
        result = [f"{self.first_name} has {self.money} dollars"]
        for name_shop, cash in full_cost_for_every_shop.items():
            result.append(
                f"{self.first_name}'s trip to the "
                f"{name_shop} costs "
                f"{cash.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}")
        min_shop = min(full_cost_for_every_shop,
                       key=full_cost_for_every_shop.get)
        min_value = full_cost_for_every_shop[min_shop]
        if min_value >= self.money:
            result.append(
                f"{self.first_name} "
                f"doesn't have enough money to make a purchase in any shop")
        else:
            result.append(f"{self.first_name} rides to {min_shop}\n")
            # now = datetime.now()
            # formatted_time = now.strftime("%d/%m/%Y, %H:%M:%S")
            result.append("Date: 04/01/2021 12:33:41")
            result.append(f"Thanks, {self.first_name}, for your purchase!")
            result.append("You have bought:")

            selected_shop = next(
                shop for shop in self.shops if shop["name"] == min_shop)

            total_cost = Decimal("0.00")
            for name, amount in self.product_cart.items():
                product_cost = Decimal(
                    selected_shop["products"][name]) * Decimal(amount)
                total_cost += product_cost
                formatted_cost = self.format_price(product_cost)
                result.append(f"{amount} {name}s for {formatted_cost} dollars")

            formatted_total_cost = self.format_price(total_cost)
            result.append(f"Total cost is {formatted_total_cost} dollars")
            result.append("See you again!\n")
            remaining_money = (self.money
                               - min_value).quantize(Decimal("0.00"))
            result.append(f"{self.first_name} "
                          f"rides home")
            result.append(f"{self.first_name} "
                          f"now has {remaining_money} dollars\n")

        return "\n".join(result)
