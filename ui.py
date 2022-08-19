from modules import *


class UI:
    """
            0 - OK, deduct turn
            1 - FAILED
            2 - OK, no need to deduct turn
            """

    def __init__(self, active_pl: Player):
        self.active_pl = active_pl

    def take_debt(self):
        code = self.active_pl.take_debt()

        if code == 0:
            print("Debt taken.")
            return 2
        else:
            print("Failed to take debt. Exceeded Maximum amount of debts.")
            return 1

    def pay_debt(self):
        code = self.active_pl.pay_debt()

        if code == 0:
            print("Payed 1 dollar")
        elif code == 1:
            print("Taken 1 debt to pay 1 dollar.")

    def return_debt(self):
        code = self.active_pl.return_debt()

        if code == 1:
            print("No debts to return!")
            return 1
        elif code == 2:
            print("Not enough money.")
            return 1
        else:
            print("Returned 1 debt for 11 dollars.")
            return 2

    def manufacture(self):
        if self.active_pl.port.factoryShop.total_items() + self.active_pl.port.get_active_plants()[
            0] > 2 * self.active_pl.port.plant_amount():
            pref = input(
                "You do not have enough space to manufacture all containers. Enter your preffered colors, seperated by a space: ").split()
        else:
            pref = None

        code = self.active_pl.manufacture(preffered=pref)

        if code == 1:
            print("Cant manufacture: not enough money.")
            return 1
        elif code == 2:
            print("Error: self.bank is not assigned.")
            raise ValueError
        elif code == 3:
            print(
                "Invalid preferred containers. This could be becuase:\n\t-You do not have the necessary plants\n\t-The containers you are trying to manufacture have run out\n\t-You have not entered enough containers\n\t")
            self.manufacture()
        else:
            print("Successfully manufactured all containers!")
            self.balance_f()
            return 0

    def balance_f(self):
        print(
            "Please assign prices to all containers in the factory shop. For each price, enter:\n\ttab + enter to keep same\n\tenter to clear\n\tany colors seperated by a space to assign those colors to a price")
        prices = []
        for i in range(1, 5):
            prices.append(input(f"Assign colors for price {i}: "))

        code = self.active_pl.balance_fshop(prices)

        if code == 1:
            print("Invalid colors. Try again.")
            self.balance_f()
        else:
            print("Prices assigned!")
