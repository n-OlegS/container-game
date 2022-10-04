from game import *
from ui import UI
from logger import Logger
import sys
import json

if len(sys.argv) > 2:
    if sys.argv[1] == '-generate':
        print(f"Generating new state for {sys.argv[2]} players...\n")
        state = init_state(sys.argv[2])
else:
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = input("Enter state path: ")

    while 1:
        try:
            file = open(path, 'r')
            break
        except FileNotFoundError:
            if path:
                print("Invalid file path.")
            path = input("Enter state path: ")

    state = json.load(file)

turn_type = state["turn type"]

class_tuple = parse(state)

pid = state["pid"]
change_generated = False
auction_completed = False

if state["generated"][str(pid)] == 0:
    card = random.choice(state['card list'])
    state['card list'].remove(card)
    state['secret'].append(state['card list copy'].index(card))
    secret_d = {'money': 20, 'doing_auction': 0,
                'card': card, 'pid': int(pid)}
    secret_f = open('secret.json', 'w')
    json.dump(secret_d, secret_f)
    secret_f.close()
    change_generated = True

players = class_tuple[0]
cache = class_tuple[1]
island = class_tuple[2]
bank = class_tuple[3]
player_num = state["playernum"]

secret_f = open('secret.json', 'r')
secret = json.load(secret_f)

player = players[pid]

if pid != secret["pid"]:
    print("Not your turn!")
    quit()

player.money = state["pending"][str(pid)] + secret["money"]
player.card = secret["card"]
state["pending"][str(pid)] = 0

logger = Logger(state, pid)

# Begin command loop

ui = UI(player, logger)

command_dict = {
    "take": lambda: ui.take_debt(),
    "return": lambda: ui.return_debt(),
    "man": lambda: ui.manufacture(),
    "manufacture": lambda: ui.manufacture(),
    "purchase": lambda: ui.purchase_to_p(),
    "move": lambda: ui.move_ship(),
    "warehouse": lambda: ui.purchase_warehouse(),
    "plant": lambda: ui.purchase_plant(),
    "stats": lambda: ui.stats(),
    "log": lambda: logger.display_short(),
    "Log": lambda: logger.display_full(),
    "r": lambda: 0,
    "?": lambda: ui.help(),
    "help": lambda: ui.help(),
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
        auction_completed = True


elif turn_type == 2:
    ui.showendgame(state['results'])
    quit()


else:

    print(player.get_own_stats())

    bid = None
    game_type = 0
    cargo = []

    for _ in range(player.debts):
        ui.pay_debt()

    i = 0
    while i < 2:
        command = input("Enter command: ")

        if command not in command_dict:
            print("Invalid command.")
            continue

        """
        0 - OK, deduct turn
        1 - FAILED
        2 - OK, no need to deduct turn
        3 - starting auction
        4 - starting endgame
        """

        code = command_dict[command]()

        if code == 0:
            i += 1
        elif code == 4:
            total_score = bank.calculate_endgame()
            state['results'] = total_score
            game_type = 2
            break
        elif code not in [1, 2]:
            game_type = 1
            secret["doing_auction"] = 1
            cargo = code
            break
players[pid] = player
tup = (players, cache, island, bank)
logger.write(state)

output = package(game_type, tup, bid, player.pid, state, change_pid=(not auction_completed))

secret["money"] = player.money
output["pending"][str(player.pid)] = 0
turn = state["turn"] + 1
output["turn"] = turn

output["auction cargo"] = cargo
if change_generated: output["generated"][str(player.pid)] = 1
json.dump(output, open(f'{turn}.json', 'w'), indent=4)
print(f"Created {turn}.json!")
json.dump(secret, open('secret.json', 'w'))
