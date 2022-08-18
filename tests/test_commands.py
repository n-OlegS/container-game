import unittest
import json

from modules import *
from game import *
from port import *


class MyTestCase(unittest.TestCase):
    def return_state(self):
        with open('/Users/oleg/PycharmProjects/container_v2/tests/states/manufacture.json', 'r') as f:
            state = json.load(f)

        return state

    def test_manufacture(self):
        class_tup = parse(self.return_state())

        player = class_tup[0][1]
        cache = class_tup[1]
        player.money = 1
        p2 = class_tup[0][0]

        player.port.plants = {"0": 1, "1": 1, "2": 0, "3": 0, "4": 0}

        self.assertEqual(player.manufacture(), 0)
        self.assertEqual(player.money, 0)
        self.assertEqual(p2.money, 1)
        self.assertEqual(cache.containers["0"], 9)
        self.assertEqual(cache.containers["1"], 8)
        self.assertEqual(cache.containers["2"], 9)
        self.assertEqual(player.port.factoryShop.total_items, 3)
        self.assertEqual(len(player.port.factoryShop.items["2"]), 1)
        self.assertEqual(len(player.port.factoryShop.items["1"]), 2)


if __name__ == '__main__':
    unittest.main()
