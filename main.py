from game import *
from ui import UI
import sys

import json

if len(sys.argv) > 1:
    if sys.argv[1] == '-generate':
        print(f"Generating new state for {sys.argv[2]} players...\n")
        state = init_state(sys.argv[2])
else:
    while 1:
        path = input("Enter state path: ")

        try:
            file = open(path, 'r')
            break
        except FileNotFoundError:
            print("Invalid file path.")

    state = json.load(file)

turn_type = state["turn type"]

class_tuple = parse(state)

secret_f = open('secret.json', 'r')
secret = json.load(secret_f)

pid = state["pid"]
players = class_tuple[0]
cache = class_tuple[1]
island = class_tuple[2]
bank = class_tuple[3]
player_num = state["playernum"]

player = players[pid]

player.money += state["pending"][str(pid)] + secret["money"]
state["pending"][str(pid)] = 0

# Begin command loop

ui = UI(player)

print(player.get_own_stats())

command_dict = {
    "take": lambda: ui.take_debt(),
    "return": lambda: ui.return_debt(),
    "man": lambda: ui.manufacture(),
    "manufacture": lambda: ui.manufacture(),
    "admin": lambda: [0, 1],
    "r 0": lambda: 0,
    "": lambda: 2
}

if turn_type == 1:
    if secret["doing_auction"] == 0:
        print("----DOING AUCTION----")
        bid = ui.auction_req(state["auction cargo"])
        cargo = state["auction cargo"]
        game_type = 1
    else:
        game_type = 0
        cargo = []
        bid = 0

        maxx = (-1, -1)
        for au_pid in state["bids"]:
            if not isinstance(state["bids"][au_pid], int): continue
            if state["bids"][au_pid] > maxx[1]:
                maxx = (au_pid, state["bids"][au_pid])

        ui.auction_do(maxx, state["auction cargo"])
        state["auction cargo"] = []
        state["bids"] = {}
        secret["doing_auction"] = 0


elif turn_type == 2:
    ui.showendgame()
    quit()


else:
    bid = None
    game_type = 0
    cargo = []

    for _ in range(player.debts):
        ui.pay_debt()

    i = 0
    while i < 2:
        command = input("Enter command: ")

        try:
            """
            0 - OK, deduct turn
            1 - FAILED
            2 - OK, no need to deduct turn
            3 - starting auction
            """

            code = command_dict[command]()

            if code == 0:
                i += 1
            elif code not in [0, 1, 2]:
                game_type = 1
                secret["doing_auction"] = 1
                cargo = code
                break

        except KeyError:
            print("Invalid command.")

players[pid] = player
tup = (players, cache, island, bank)

output = package(game_type, tup, bid, player.pid, state)

secret["money"] = player.money
output["pending"][str(player.pid)] = 0

output["auction cargo"] = cargo
json.dump(output, open('111.json', 'w'))
json.dump(secret, open('secret.json', 'w'))
