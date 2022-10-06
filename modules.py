from port import *


class Bank:
    def __init__(self, players, island, card_list, secret_list, cache):
        self.players = players
        self.cache = cache
        self.card_list = card_list
        self.secret_list = secret_list
        self.island = island

    def transact(self, pid_1, pid_2, amount):
        assert int(pid_1) < len(self.players) and int(pid_2) < len(self.players)

        self.players[int(pid_1)].money -= amount
        self.players[int(pid_2)].money += amount

    def fact_to_port(self, pid_1, pid_2, containers):
        for elem in containers:
            self.players[int(pid_1)].port.factoryShop.items[str(elem[0])].remove(int(elem[1]))
            self.players[int(pid_2)].port.portShop.items["2"].append(elem[1])

    def port_to_ship(self, pid_1, pid_2, containers):
        for elem in containers:
            self.players[pid_1].port.portShop.items[str(elem[0])].remove(int(elem[1]))
            self.players[int(pid_2)].ship.cargo.append(elem[1])

    def to_island(self, pid, cargo):
        self.island.stock[str(pid)] += cargo

    def calculate_endgame(self):
        totals = {}
        prices = {0: 10, 11: 10, 12: 5, 2: 6, 3: 4, 4: 2}

        for pid in range(len(self.players)):
            player = self.players[pid]
            card = self.card_list[self.secret_list[pid]]
            total = 0

            count = len(set(self.island.stock[str(pid)]))
            if count == 5:
                double = True
            else:
                double = False

            max_col = -1
            max_count = 0
            counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}

            for color in self.island.stock[str(pid)]:
                counts[color] += 1
                if counts[color] > max_count:
                    max_count = counts[color]
                    max_col = color

            self.island.stock[str(pid)] = [x for x in self.island.stock[str(pid)] if x != max_col]

            for i in range(len(card)):
                color = card[i]
                if i == 1:
                    if double:
                        i = 11
                    else:
                        i = 12

                total += prices[i] * self.island.stock[str(pid)].count(color)

            total += player.money
            total += 3 * len(player.ship.cargo)
            total += 2 * len(dump_dict(player.port.portShop.items))
            total -= 11 * player.debts

            totals[str(pid)] = total

        return totals


class Cache:
    def __init__(self, containers, plants, warehouses):
        self.containers = containers
        self.plants = plants
        self.warehouses = warehouses

    def pop_old(self, order):
        if isinstance(order, list):
            # accepts [0, 0, 0, 1, 2, 2, 3] etc
            out = []
            for elem in order:
                if self.containers[str(elem)] == 0:
                    return None
                else:
                    out.append(self.containers[str(elem)])
                    self.containers[str(elem)] -= 1

            return out

        elif len(self.containers[order]) == 0:
            return None
        else:
            out = self.containers[order][0]
            del self.containers[order][0]
            return out

    def pop(self, order):
        if isinstance(order, list):
            for elem in order:
                if elem not in self.containers: raise Exception
                self.containers[elem] -= 1
        else:
            if order not in self.containers: raise Exception
            self.containers[order] -= 1

        return order


class Ship:
    def __init__(self, location, cargo):
        self.location = location
        self.cargo = cargo


class Island:
    def __init__(self, stock):
        self.stock = stock

    def pack(self):
        out = []
        for i in self.stock:
            out.append(self.stock[i])

        return out


class Player:
    def __init__(self, player_num, pid, debts, warehouse_prices, plant_prices, ship_state, port_state, cache):
        self.pid = pid
        self.debts = debts
        self.money = 0
        self.card = None
        self.bank = None
        self.cache = cache
        self.player_num = player_num
        self.warehouse_prices = warehouse_prices
        self.plant_prices = plant_prices

        self.port = Port(cache, port_state["plants"], port_state["warehouses"], port_state["port shop"],
                         port_state["factory shop"])

        self.ship = Ship(ship_state["location"], ship_state["cargo"])

    def purchase_warehouse(self):
        if bool(len(self.warehouse_prices)):
            if self.money >= self.warehouse_prices[0] and self.cache.warehouses > 0:
                self.money -= self.warehouse_prices[0]
                self.port.warehouses += 1
                self.cache.warehouses -= 1
                del self.warehouse_prices[0]

                return 0

            return 2

        return 1

    def purchase_plant(self, color):
        if bool(len(self.plant_prices)):
            if color not in self.cache.plants: return 3
            if self.money >= self.plant_prices[0] and self.port.plants[color] == 0 and self.cache.plants[color] > 0:
                self.money -= self.plant_prices[0]
                self.port.plants[color] = 1
                self.cache.plants[color] -= 1
                del self.plant_prices[0]
                return 0

            return 2

        return 1

    def take_debt(self):
        if self.debts < 2:
            self.debts += 1
            self.money += 10
            return 0

        return 1

    def return_debt(self):
        if self.debts <= 0: return 1

        if self.money >= 11:
            self.debts -= 1
            self.money -= 11

            return 0

        return 2

    def pay_debt(self):
        if self.debts == 0: return 0

        if self.money >= 1:
            self.money -= 1

            return 0

        elif self.debts < 2:
            self.take_debt()
            self.money -= 1

            return 1

        else:
            pass

            # write

    def manufacture(self, preffered=None):
        if self.money == 0: return 1

        if self.pid == 0:
            pay_pid = self.player_num - 1
        else:
            pay_pid = int(self.pid) - 1

        if self.bank is None: return 2

        if self.port.factoryShop.total_items() + self.port.get_active_plants()[0] <= 2 * self.port.plant_amount():
            self.bank.transact(int(self.pid), pay_pid, 1)
            package = self.cache.pop(self.port.get_active_plants()[1])
            self.port.factoryShop.add_containers(package)
        else:
            if preffered is None or len(
                    preffered) + self.port.factoryShop.total_items() != 2 * self.port.plant_amount():
                return 3

            package = []

            for c in preffered:
                if not (self.port.plants[c] == 1 and len(self.cache.containers[c]) >= 1): return 3
                package.append(c)

            package = self.cache.pop(package)  # Maybe?
            self.port.factoryShop.add_containers(package)

            self.bank.transact(self.pid, pay_pid, 1)

        # RUN ENDGAME CHECK

        empty = 0
        for color in self.cache.containers:
            if self.cache.containers[color] == 0:
                empty += 1

        if empty >= 2:
            return 4

        return 0

    def balance_fshop(self, prices):
        if self.port.factoryShop.balance(prices) == 1: return 1
        return 0

    def balance_pshop(self, prices):
        if self.port.portShop.balance(prices) == 1: return 1
        return 0

    def purchase_to_p(self, pid, colors):
        if len(colors) > self.port.warehouses - self.port.portShop.total_items(): return 3
        if self.bank.players[int(pid)].port.factoryShop.check_stock(colors): return 1
        package_tup = self.bank.players[int(pid)].port.factoryShop.package(colors)
        if package_tup[0] > self.money: return 2

        self.bank.transact(self.pid, pid, package_tup[0])
        self.bank.fact_to_port(pid, self.pid, package_tup[1])

        return 0

    def accept_auction(self, max_tup, cargo):
        pid = max_tup[0]
        self.bank.transact(pid, self.pid, max_tup[1])
        self.money += max_tup[1]
        self.bank.island.stock[str(pid)] += cargo

    def decline_auction(self, price, cargo):
        if self.money < price: return 1

        self.money -= price
        self.bank.to_island(self.pid, cargo)
        return 0

    def get_own_stats(self):
        stats = f'\n\n\n----YOUR GENERAL STATS----\nMoney: {self.money}\nDebts:{self.debts}'
        if bool(len(self.warehouse_prices)):
            stats += f'\nPid: {self.pid}\n\nNext warehouse will cost ${self.warehouse_prices[0]}\n'
        else:
            stats += "Unable to purchase any more warehouses\n"

        if bool(len(self.plant_prices)):
            stats += f'Next plant will cost ${self.plant_prices[0]}\n'
        else:
            stats += f'Unable to purchase any more plants\n'

        stats += '\n-------CACHE STATS-------\n'

        for container in self.cache.containers:
            stats += f"Containers of color {container} left: {self.cache.containers[container]}\n"

        stats += '\n'

        for plant in self.cache.plants:
            stats += f"Plants of color {plant} left: {self.cache.plants[plant]}\n"

        stats += f'\nWarehouses left: {self.cache.warehouses}\n'

        stats += '\n-----ISLAND STATS-----'

        for pid in range(self.player_num):
            stats += f'\nPlayer {pid}:\n\t'
            stats += '\n\t'.join(f'{x}: {self.bank.island.stock[str(pid)].count(x)}' for x in range(5))

        stats += '\n\n--------PORT STATS--------'

        for pid in range(self.player_num):
            stats += f'\n\nPort of player {pid} stats\n'
            stats += f'Factory Shop:\n'
            for price in self.bank.players[pid].port.factoryShop.items:
                stats += f'\t${price}: {self.bank.players[pid].port.factoryShop.items[price]}\n'

            stats += '\nPort Shop:\n'
            for price in self.bank.players[pid].port.portShop.items:
                stats += f'\t${price}: {self.bank.players[pid].port.portShop.items[price]}\n'

            stats += f'Manufacturing plants: {", ".join([key for key in self.bank.players[pid].port.plants if self.bank.players[pid].port.plants[key] == 1])}\n'
            stats += f'Warehouses: {self.bank.players[pid].port.warehouses}\n'

        stats += '\n--------SHIP STATS--------\n\n'

        for pid in range(self.player_num):
            stats += f"Player {pid}'s ship is in zone {self.bank.players[pid].ship.location}\n"

        for pid in range(self.player_num):
            stats += f"Player {pid}'s ship cargo: {self.bank.players[pid].ship.cargo}\n"


        stats += '\nContainer colors:\n\t0-Black\n\t1-Brown\n\t2-Purple\n\t3-Yellow\n\t4-Gray\n'
        stats += f'\nYour card:\n\t$10: {self.card[0]}\n\t$5/10: {self.card[1]}\n\t$6: {self.card[2]}\n\t'
        stats += f'$4: {self.card[3]}\n\t$2: {self.card[4]}\n'

        return stats

    def purchase_to_s(self, pid, colors):
        if self.bank.players[pid].port.portShop.check_stock(colors): return 1
        package_tup = self.bank.players[pid].port.portShop.package(colors)
        if package_tup[0] > self.money: return 2

        self.bank.transact(self.pid, pid, package_tup[0])
        self.bank.port_to_ship(pid, self.pid, package_tup[1])

        return 0

    def move_ship(self, zone):
        current = self.ship.location

        if current != 5 and zone != 5:
            return -1
        elif current == 5 == zone:
            return -1
        else:
            self.ship.location = zone
            return zone
