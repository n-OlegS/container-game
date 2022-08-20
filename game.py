from modules import *
import json
import random


def parse(state: dict):
    cache = Cache(state["cache"]["containers"], state["cache"]["plants"], state["cache"]["warehouses"])
    island = Island(state["island"])
    players = []

    for pid in state["entities"]:
        entity_dict = state["entities"][pid]
        player = Player(state["playernum"], pid, entity_dict["general"]["debts"],
                        entity_dict["general"]["warehouse prices"],
                        entity_dict["general"]["plant prices"], entity_dict["ship"], entity_dict["port"], cache)

        players.append(player)

    bank = Bank(players, island)
    for player in players: player.bank = bank

    players[int(state["pid"])].money += state["pending"][str(state["pid"])]

    return players, cache, island, bank


def package(game_type, class_tuple, bid, pid, old_state):
    print("PACKAGING WITH PID", pid)
    players = class_tuple[0]
    cache = class_tuple[1]
    island = class_tuple[2]
    state = old_state
    state["turn type"] = game_type

    if game_type == 0:
        for i in range(len(players)):
            state["pending"][str(i)] += players[i].money

    else:
        state["bids"][str(pid)] = bid

    state["cache"]["containers"] = cache.containers
    state["cache"]["plants"] = cache.plants
    state["cache"]["warehouses"] = cache.warehouses

    state["island"] = island.pack()
    state["pid"] = int(pid)

    state["playernum"] = len(players)
    state["entities"] = {}

    for i in range(len(players)):
        player = players[i]
        p_dict = {}

        p_dict["general"] = {
            "debts": player.debts,
            "warehouse prices": player.warehouse_prices,
            "plant prices": player.plant_prices
        }

        p_dict["ship"] = {
            "location": player.ship.location,
            "cargo": player.ship.cargo
        }

        p_dict["port"] = {
            "plants": player.port.plants,
            "warehouses": player.port.warehouses,
            "factory shop": player.port.factoryShop.items,
            "port shop": player.port.portShop.items
        }

        state["entities"][str(i)] = p_dict

    pid = int(pid)
    pid += 1
    if pid == len(players): pid = 0

    state["pid"] = pid

    return state


def init_state(player_num):
    player_num = int(player_num)

    state = {"turn type": 0, "auction cargo": [], "bids": {}}

    # Turn types: 0 - regular turn   1 - auction   2 - endgame results

    key = {
        "containers": [0, 0, 0, 10, 13, 16],
        "plants": [0, 0, 0, 2, 3, 4],
        "warehouses": [0, 0, 0, 12, 16, 20]
    }

    state["cache"] = {
        "containers": {
            "0": key["containers"][player_num],
            "1": key["containers"][player_num],
            "2": key["containers"][player_num],
            "3": key["containers"][player_num],
            "4": key["containers"][player_num]
        },
        "plants": {
            "0": key["plants"][player_num],
            "1": key["plants"][player_num],
            "2": key["plants"][player_num],
            "3": key["plants"][player_num],
            "4": key["plants"][player_num]
        },
        "warehouses": key["warehouses"][player_num]
    }

    state["island"] = [[] for _ in range(player_num)]
    state["pid"] = 0
    state["playernum"] = player_num
    state["pending"] = {}
    state["entities"] = {}
    random_color = list(range(5))

    for i in range(player_num):
        state["bids"][str(i)] = 0
        state["pending"][str(i)] = 0
        color = random_color.pop(random.randint(0, len(random_color) - 1))
        state["entities"][str(i)] = {
            "general": {
                "debts": 0,
                "warehouse prices": [4, 5, 6, 7],
                "plant prices": [6, 9, 12]
            },
            "ship": {
                "location": 5,
                "cargo": []
            },
            "port": {
                "plants": {
                    "0": 0,
                    "1": 0,
                    "2": 0,
                    "3": 0,
                    "4": 0
                },

                "warehouses": 1,

                "factory shop": {
                    "1": [],
                    "2": [],
                    "3": [],
                    "4": []
                },

                "port shop": {
                    "2": [],
                    "3": [],
                    "4": [],
                    "5": [],
                    "6": []
                }
            }
        }

        state["entities"][str(i)]["port"]["plants"][str(color)] = 1
        state["entities"][str(i)]["port"]["factory shop"]["2"] = [color]

        state["cache"]["containers"][str(color)] -= 1
        state["cache"]["plants"][str(color)] -= 1
        state["cache"]["warehouses"] -= 1

    return state


with open("/Users/oleg/PycharmProjects/container_v2/state_3p.json", 'w') as f:
    json.dump(init_state(3), f)
