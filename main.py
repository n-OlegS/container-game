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

command_dict = {
    "take": lambda: ui.take_debt(),
    "return": lambda: ui.return_debt(),
    "man": lambda: ui.manufacture(),
    "manufacture": lambda: ui.manufacture()
}

if turn_type == 1:
    if secret["doing_auction"] == 0:
        bid = ui.auction_req(state["auction cargo"])
        game_type = 1
    else:
        game_type = 0

        maxx = (-1, -1)
        for au_pid in state["bids"]:
            if state["bids"][au_pid] > maxx[1]:
                maxx = (au_pid, state["bids"][au_pid])

        ui.auction_do(maxx, state["auction cargo"])


elif turn_type == 2:
    ui.showendgame()
    quit()


else:
    bid = None
    game_type = 0

    for _ in range(player.debts):
        ui.pay_debt()

    i = 0
    while i < 2:
        print(
            f"\n\n\nMoney: {player.money}\nShip in zone {player.ship.location}\nDebts: {player.debts}\nID: {player.pid}\nNext warehouse will cost ${player.warehouse_prices[1]}\nNext plant will cost ${player.plant_prices[0]}")

        command = input("Enter command: ")

        try:
            """
            0 - OK, deduct turn
            1 - FAILED
            2 - OK, no need to deduct turn
            """

            code = command_dict[command]()

            if code == 0:
                i += 1

        except KeyError:
            print("Invalid command.")

players[str(pid)] = player
tup = (players, cache, island, bank)
pid += 1
if pid == player_num: pid = 0
package(game_type, bank, bid)
