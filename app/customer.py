from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from app.car import Car
from app.shop import Shop


class Customer:
    def __new__(
            cls,
            customers: list,
            shops: Shop,
            fuel_price: float
    ) -> list:
        instances = []
        for customer in customers:
            instance = super(Customer, cls).__new__(cls)
            instance.__init__(customer, shops, fuel_price)
            instances.append(instance)
        return instances

    def __init__(self, customer: dict, shops: Shop, fuel_price: float) -> None:
        self.first_name = customer["name"]
        self.product_cart = customer["product_cart"]
        self.location = customer["location"]
        self.money = Decimal(customer["money"])
        self.fuel = Car(
            fuel_price,
            customer["car"]["brand"],
            Decimal(
                customer["car"]["fuel_consumption"]).quantize(Decimal("0.00"))
        )
        self.shops = shops

    @staticmethod
    def format_price(price: Decimal) -> str:
        if price == price.to_integral():
            return f"{price:.0f}"
        else:
            return f"{price:.1f}"

    def return_(self) -> str:
        full_cost_for_every_shop = self.shops.total_cost(
            self.product_cart,
            self.location,
            self.fuel)
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
            result.append("Date: 04/01/2021 12:33:41")
            result.append(f"Thanks, {self.first_name}, for your purchase!")
            result.append("You have bought:")

            selected_shop = self.get_shop_by_name(min_shop)

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
            remaining_money = (self.money - min_value).quantize(
                Decimal("0.00"))
            result.append(f"{self.first_name} rides home")
            result.append(f"{self.first_name} now has "
                          f"{remaining_money} dollars\n")

        return "\n".join(result)

    def get_shop_by_name(self, shop_name: str) -> Any | None:
        for shop in self.shops.shops_list:
            if shop["name"] == shop_name:
                return shop
        return None
