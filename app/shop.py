class Shop:
    shops_list = []

    @classmethod
    def __init__(cls, shops: list) -> None:
        for shop in shops:
            cls.shops_list.append(shop)
