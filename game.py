from modules import *
import json
import random


def parse(state: dict):
    cache = Cache(state["cache"]["containers"], state["cache"]["plants"], state["cache"]["warehouses"])
    island = Island(state["island"])
    players = []

    for pid in state["entities"]:
        entity_dict = state["entities"][pid]
        player = Player(state["playernum"], pid, entity_dict["general"]["debts"], entity_dict["general"]["warehouse prices"],
                        entity_dict["general"]["plant prices"], entity_dict["ship"], entity_dict["port"], cache)

        players.append(player)

    bank = Bank(players)
    for player in players: player.bank = bank

    return players, cache, island, bank


def init_state(player_num):
    player_num = int(player_num)

    state = {}
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