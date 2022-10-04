class Logger:
    def __init__(self, state_d, pid):
        self.log = state_d["log"]
        self.current_log = [f"Player {pid}:"]

    def write(self, state_d):
        self.log.append('\n\t'.join(self.current_log))
        state_d["log"] = self.log
        return state_d

    def display_short(self):
        for log in self.log[-2:]:
            print(log)
        return 2

    def display_full(self):
        print('\n'.join(log for log in self.log))
        return 2

    def log_debt_taken(self):
        self.current_log.append("Took a loan.")

    def log_debt_returned(self):
        self.current_log.append("Returned a loan.")

    def log_warehouse_purchased(self):
        self.current_log.append("Purchased a warehouse")

    def log_plant_purchased(self, color):
        self.current_log.append(f"Purchased a plant of color {color}")

    def log_manufactured(self, colors):
        self.current_log.append(f"Manufactured containers of colors {' '.join([str(x) for x in colors])}")

    def log_purchased_to_p(self, pid, colors):
        self.current_log.append(
            f"Purchased containers {', '.join([str(x) for x in colors])} from player {pid}'s factory shop.")

    def log_purchased_to_s(self, pid, colors):
        self.current_log.append(
            f"Purchased containers of colors {', '.join([str(x) for x in colors])} from player {pid}'s port shop.")

    def log_moved_ship(self, zone):
        if zone == 5:
            self.current_log.append("Moved ship to the open sea")
        elif zone == 6:
            self.current_log.append("Moved ship to the island. Started auction")
        else:
            self.current_log.append(f"Moved ship to player {zone}'s port")
