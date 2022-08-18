from game import *
from modules import *
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

print(class_tuple)