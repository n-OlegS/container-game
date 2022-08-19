from game import *
from modules import *
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

class_tuple = parse(state)

pid = state["pid"]
players = class_tuple[0]
cache = class_tuple[1]
island = 2
player_num = state["playernum"]

player = players[pid]

player.money += state["pending"][str(pid)]
state["pending"][str(pid)] = 0

# Begin command loop

ui = UI(player)

command_dict = {
    "take": lambda: ui.take_debt(),
    "return": lambda: ui.return_debt(),
    "man": lambda: ui.manufacture(),
    "manufacture": lambda: ui.manufacture()
}

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

print(class_tuple)
