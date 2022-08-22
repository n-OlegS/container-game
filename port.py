# Color types: 0 - black, 1 - yellow, 2 - gray, 3 - blue, 4 - brown

class Port:
    def __init__(self, cache, plants, warehouses, port_stats, fshop_stats):
        self.cache = cache
        self.portShop = portShop(port_stats)
        self.factoryShop = factoryShop(fshop_stats)

        # See container color scheme
        self.plants = plants
        # self.plant_amount = len([x for x in dump_dict(plants) if x == 1])
        self.warehouses = warehouses

    def plant_amount(self):
        total = 0
        for key in self.plants:
            total += self.plants[key]
        return total

    def get_active_plants(self):
        amount = 0
        plant_list = []

        for plant in self.plants:
            if self.plants[plant] == 1 and self.cache.containers[plant] > 0:
                amount += 1
                plant_list.append(plant)

        return amount, plant_list


class factoryShop:
    def __init__(self, color_d):
        self.items = color_d
        # self.total_items = sum(len(self.items[x]) for x in self.items)

    def total_items(self):
        total = 0
        for key in self.items:
            total += len(self.items[key])
        return total

    def balance_old(self, prices):
        containers_d = self.items.copy()
        containers = dump_dict(containers_d)

        new_dict = {
            "1": [],
            "2": [],
            "3": [],
            "4": []
        }

        for price in prices:
            if prices[price] == '\t':
                new_dict[price] = containers_d[price]
                continue

            for color in prices[price]:
                color = int(color)

                for container in containers:
                    if container.color == color:
                        containers.remove(container)
                        new_dict[price].append(container)
                        break

        if len(containers) == 0 and len(dump_dict(containers_d)) == len(dump_dict(new_dict)):
            return new_dict

        return []

    def balance(self, prices_l):
        i = 0
        new_dict = {
            "1": [],
            "2": [],
            "3": [],
            "4": []
        }

        for price in self.items:
            if prices_l[i] == '\t':
                new_dict[price] = self.items[price].copy
            elif prices_l[i] == '':
                new_dict[price] = []
            else:
                new_dict[price] = price[i].split().copy()

            i += 1

        if dump_dict(self.items) == dump_dict(new_dict):
            self.items = new_dict.copy()
            return 0
        else:
            return 1

    def add_containers(self, containers):
        self.items["1"] += containers

    def check_stock(self, request):
        stock = dump_dict(self.items).copy()
        for elem in request:
            if elem not in stock:
                return 1
            else:
                stock.remove(elem)
        return 0

    def package(self, request):
        total = 0
        package = []

        cop = {}

        for price in self.items:
            cop[price] = self.items[price].copy()

        for item in request:
            for price in cop:
                if item in cop[price]:
                    package.append((int(price), item))
                    total += int(price)
                    cop[price].remove(item)
                    break

        # Returns (<total price>, [(price, color)...])
        return total, package


class portShop:
    def __init__(self, color_d):
        self.total_items = 0
        self.items = color_d

    def check_stock(self, request):
        stock = dump_dict(self.items).copy()
        for elem in request:
            if elem not in stock:
                return 1
            else:
                stock.remove(elem)
        return 0

    def package(self, request):
        total = 0
        package = []

        cop = {}

        for price in self.items:
            cop[price] = self.items[price].copy()

        for item in request:
            for price in cop:
                if item in cop[price]:
                    package.append((int(price), item))
                    total += int(price)
                    cop[price].remove(item)
                    break

        # Returns (<total price>, [(price, color)...])
        return total, package

    def balance(self, prices_l):
        i = 0
        new_dict = {
            "1": [],
            "2": [],
            "3": [],
            "4": []
        }

        for price in self.items:
            if prices_l[i] == '\t':
                new_dict[price] = self.items[price].copy
            elif prices_l[i] == '':
                new_dict[price] = []
            else:
                new_dict[price] = price[i].split().copy()

            i += 1

        if dump_dict(self.items) == dump_dict(new_dict):
            self.items = new_dict.copy()
            return 0
        else:
            return 1


def dump_dict(d: dict):
    l = []
    for key in d:
        if not isinstance(d[key], list):
            l.append(d[key])
        else:
            l += d[key]

    return l