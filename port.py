class Container:
    # Color types: 0 - black, 1 - yellow, 2 - gray, 3 - blue, 4 - brown

    def __init__(self, color):
        self.color = color


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
        self.items = {
            "1": [],
            "2": [],
            "3": [],
            "4": []
        }

        self.total_items = 0

        for price in color_d:
            if len(color_d[price]) == 0: continue
            out = [Container(color) for color in color_d[price]]
            self.items[price] = out

        self.total_items = sum(len(self.items[x]) for x in self.items)

    def balance(self, prices):
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

    def add_containers(self, containers):
        self.items["1"] += containers
        self.total_items += len(containers)


class portShop:
    def __init__(self, color_d):
        self.total_items = 0
        self.items = {
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": []
        }

        for price in color_d:
            if len(color_d[price]) == 0: continue
            out = [Container(color) for color in color_d[price]]
            self.items[price] = out


def dump_dict(d: dict):
    l = []
    for key in d:
        if not isinstance(d[key], list):
            l.append(d[key])
        else:
            l += d[key]

    return l