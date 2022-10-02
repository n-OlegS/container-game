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

    def purchase_warehouse(self):
        code = self.active_pl.purchase_warehouse()

        if code == 0:
            print("Warehouse purchased.")
            return 0
        elif code == 1:
            print("Maximum amount of warehouses reached.")
            return 1
        else:
            print("Not enough money.")
            return 1

    def purchase_plant(self):
        color = input("What color plant do you want to purchase? ")
        code = self.active_pl.purchase_plant(color)

        if code == 0:
            print("Plant purchased.")
            return 0
        elif code == 1:
            print("Maximum amount of plants reached.")
            return 1
        elif code == 2:
            print(
                "Either you do not have enough money, you already have a plant of this color, or there are no more plants of this color left.")
            return 1
        else:
            print("Invalid color...")
            return 1

    def manufacture(self):
        if self.active_pl.port.factoryShop.total_items() + self.active_pl.port.get_active_plants()[
            0] > 2 * self.active_pl.port.plant_amount():
            pref = input(
                "You do not have enough space to manufacture all containers. Enter your preffered colors, separated by a space: ").split()
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
        elif code == 4:
            return 4
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

    def balance_p(self):
        print(
            "Please assign prices to all containers in the port shop. For each price, enter:\n\ttab + enter to keep same\n\tenter to clear\n\tany colors seperated by a space to assign those colors to a price")
        prices = []
        for i in range(2, 7):
            prices.append(input(f"Assign colors for price {i}: "))

        code = self.active_pl.balance_pshop(prices)

        if code == 1:
            print("Invalid colors. Try again.")
            self.balance_p()
        else:
            print("Prices assigned!")

    def purchase_to_p(self):
        pid = input("What player do you want to purchase from? ")
        colors = [int(x) for x in
                  input("What colors do you want to purchase? Enter the colors, seperated by a space: ").split()]

        if pid == self.active_pl.pid:
            print("Can't purchase from own factory.")
            return 1

        if not 0 <= int(pid) < self.active_pl.player_num:
            print("Invalid player id.")
            return 1

        code = self.active_pl.purchase_to_p(pid, colors)

        if code == 1:
            print("Invalid container colors.")
            return 1
        elif code == 2:
            print("Not enough money.")
            return 1
        elif code == 3:
            print("Not enough warehouse space.")
            return 1
        elif code == 0:
            print("Containers purchased!")
            self.balance_p()
            return 0

    def purchase_to_s(self, pid):
        colors = [int(x) for x in
                  input("What colors do you want to purchase? Enter the colors, seperated by a space: ").split()]
        code = self.active_pl.purchase_to_s(pid, colors)

        if code == 1:
            print("Invalid container colors.")
            self.purchase_to_s(pid)
        elif code == 2:
            print("Not enough money.")
            self.purchase_to_s(pid)
        elif code == 0:
            print("Containers purchased!")

    def auction_req(self, colors):
        print(f"You are: {self.active_pl.pid}")
        bid = input(
            f"How much money are you willing to bid for containers: {colors}? Type take to take a debt. You have ${self.active_pl.money}")
        if bid == "take":
            self.take_debt()
            self.auction_req(colors)
        else:
            try:
                bid = int(bid)
            except ValueError:
                print("Invalid sum.")
                self.auction_req(colors)
                return

            if bid > self.active_pl.money:
                print("Not enough money.")
                self.auction_req(colors)
            else:
                return bid

    def auction_do(self, max_tup, cargo):
        conf = input(
            f"Are you willing to accept ${max_tup[1]} from player {max_tup[0]} for cargo {cargo}? y/n, take to take debt")

        if conf == "take":
            self.take_debt()
            self.auction_do(max_tup, cargo)

        if conf == 'y':
            self.active_pl.accept_auction(max_tup, cargo)
        elif conf == 'n':
            self.decline_auction(max_tup, cargo)
        else:
            print("Invalid input.")
            self.auction_do(max_tup, cargo)

    def decline_auction(self, max_tup, cargo):
        code = self.active_pl.decline_auction(max_tup[1], cargo)

        if code == 0:
            print("Auction declined")
            return 0
        else:
            print("Cant decline auction: not enough money.")
            self.active_pl.accept_auction(max_tup, cargo)

    def move_ship(self):
        stats = ''
        stats += '\nShip Zones:\n\n'
        for i in range(5):
            stats += f'Zone {i}: '
            if i < self.active_pl.player_num:
                stats += f"Player {i}'s port\n"
            else:
                stats += 'unavailable\n'

        stats += 'Zone 5: Open sea\nZone 6: Island\n'

        print(stats)

        zone = int(input("What zone would you like to move your ship to? "))
        if zone == int(self.active_pl.pid):
            print("Cant purchase from own port.")
            return 1

        code = int(self.active_pl.move_ship(zone))

        if code == -1:
            print("You cant move your ship to that zone.")
            return 1
        elif 0 <= code < 5:
            print(f"\nMoved ship to player {zone}'s port.")

            stats = ''
            stats += '\nPort Shop:\n'
            for price in self.active_pl.bank.players[code].port.portShop.items:
                stats += f'\t${price}: {self.active_pl.bank.players[code].port.portShop.items[price]}\n'

            print(stats)

            self.purchase_to_s(code)
            return 0
        elif code == 5:
            print("Moved ship to the open sea.")
            return 0
        elif code == 6:
            conf = input(
                "Are you sure you want to go to the island and start an auction? Doing so will end your turn. Y/n")
            if conf not in 'yY': return 1
            print("Your ship has arrived at the island. Starting auction...")
            cargo = self.active_pl.ship.cargo
            self.active_pl.ship.cargo = []
            return cargo

    def stats(self):
        print(self.active_pl.get_own_stats())
        return 2

    def help(self):
        print("List of commands:")
        print('\ttake: take a loan')
        print('\treturn: return loan\n\tman/manufacture: manufature available containers')
        print("\tpurchase: purchase containers from somebody's factory shop")
        print('\twarehouse: purchase a warehouse\n\tplant: purchase a plant')
        print('\tmove: move your ship from one zone to another\n\tstats: show the game state\n\thelp: show this text\n')

        return 2

    def showendgame(self, totals):
        for i in range(self.active_pl.player_num):
            print(f'Player {i} finished with ${totals[str(i)]}')

        print("GAME OVER!")
