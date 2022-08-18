from port import *


class Bank:
    def __init__(self, players):
        self.players = players

    def transact(self, pid_1, pid_2, amount):
        assert self.players[pid_1].money >= amount
        assert pid_1 < len(self.players) and pid_2 < len(self.players)

        self.players[pid_1].money -= amount
        self.players[pid_2].money += amount

    def fact_to_port(self, pid_1, pid_2, containers):
        for elem in containers:
            self.players[pid_1].port.factoryShop.items[elem[0]].remove(elem[1])
            self.players[pid_2].port.portShop.items[2].append(elem[1])


class Cache:
    def __init__(self, containers, plants, warehouses):
        self.containers = containers
        self.plants = plants
        self.warehouses = warehouses

    def pop(self, order):
        if isinstance(order, list):
            # accepts [0, 0, 0, 1, 2, 2, 3] etc
            out = []
            for elem in order:
                if self.containers[elem] == 0:
                    return None
                else:
                    out.append(self.containers[elem])
                    self.containers[elem] -= 1

            return out

        elif len(self.containers[order]) == 0: return None
        else:
            out = self.containers[order][0]
            del self.containers[order][0]
            return out


class Ship:
    def __init__(self, location, cargo):
        self.location = location
        self.cargo = [Container(color) for color in cargo]


class Island:
    def __init__(self, colors):
        self.stock = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: []
        }

        pid = 0
        for color in colors:
            self.stock[pid] += color


class Player:
    def __init__(self, player_num, pid, debts, warehouse_prices, plant_prices, ship_state, port_state, cache):
        self.pid = pid
        self.debts = debts
        self.money = 0
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

        return 1

    def purchase_plant(self, color):
        if bool(len(self.plant_prices)):
            if self.money >= self.plant_prices[0] and self.port.plants[color] == 0 and self.cache.plants[color] > 0:
                self.money -= self.plant_prices[0]
                self.port.plants[color] = 1
                self.port.plant_amount += 1
                self.cache.plants[color] -= 1
                del self.plant_prices[0]

            return 1

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

        return 1

    def pay_debt(self):
        if self.money >= 1:
            self.money -= 1

            return 0

        elif self.debts < 2:
            self.take_debt()
            self.money -= 1

        else:
            pass

            # write

    def manufacture(self, preffered=None):
        if self.money == 0: return 1

        if self.pid == 0:
            pay_pid = self.player_num - 1
        else:
            pay_pid = int(self.pid) - 1

        if self.bank is None: return 1

        if self.port.factoryShop.total_items() + self.port.get_active_plants()[0] <= 2 * self.port.plant_amount():
            self.bank.transact(int(self.pid), pay_pid, 1)
            package = self.cache.pop(self.port.get_active_plants()[1])
            self.port.factoryShop.add_containers(package)
        else:
            if preffered is None or len(
                    preffered) + self.port.factoryShop.total_items() != 2 * self.port.plant_amount():
                return 1

            package = []

            for c in preffered:
                if not (self.port.plants[c] == 1 and len(self.cache.containers[c]) >= 1): return 1
                package.append(c)

            package = self.cache.pop(package)  # Maybe?
            self.port.factoryShop.add_containers(package)

            self.bank.transact(self.pid, pay_pid, 1)

        return 0

    def balance_fshop(self, prices):
        if self.port.factoryShop.balance(prices) == 1: return 1
