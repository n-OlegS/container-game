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
        # TEST CASE 1

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
        self.assertEqual(player.port.factoryShop.total_items(), 3)
        self.assertEqual(len(player.port.factoryShop.items["2"]), 1)
        self.assertEqual(len(player.port.factoryShop.items["1"]), 2)

        # TEST CASE 2

        class_tup = parse(self.return_state())
        player = class_tup[0][1]
        cache = class_tup[1]
        p2 = class_tup[0][0]

        self.assertEqual(player.manufacture(), 1)

        player.port.plants = {"0": 1, "1": 1, "2": 1, "3": 0, "4": 0}
        player.port.factoryShop.items["1"] = [0, 0, 1, 2, 2]
        player.money = 1

        self.assertNotEqual(player.manufacture(), 0)
        self.assertNotEqual(player.manufacture(preffered=[0, 1]), 0)
        self.assertNotEqual(player.manufacture(preffered=[0, 3]), 0)

        cache.containers["0"] = 0

        self.assertNotEqual(player.manufacture(preffered=[0, 1]), 0)
        self.assertNotEqual(player.manufacture(preffered=[0]), 0)
        self.assertNotEqual(player.manufacture(preffered=[3]), 0)

        # TEST CASE 3

        class_tup = parse(self.return_state())
        player = class_tup[0][1]
        cache = class_tup[1]
        p2 = class_tup[0][0]
        player.money = 1

        self.assertEqual(player.manufacture(preffered=[1]), 0)

    def test_purchase_to_p(self):
        # TEST CASE 1

        class_tup = parse(self.return_state())
        player = class_tup[0][1]
        cache = class_tup[1]
        p2 = class_tup[0][0]

        p2.port.factoryShop.items["1"] = [0, 1]
        p2.port.factoryShop.items["2"] = [1]

        p2.money = 0
        player.money = 4
        self.assertEqual(player.purchase_to_p(0, [0, 1, 1]), 0)
        self.assertEqual(player.money, 0)
        self.assertEqual(p2.money, 4)
        self.assertEqual(len(player.port.portShop.items["2"]), 3)
        self.assertEqual(len(p2.port.factoryShop.items["1"]), 0)
        self.assertEqual(len(p2.port.factoryShop.items["2"]), 0)

        # TEST CASE 2

        class_tup = parse(self.return_state())
        player = class_tup[0][1]
        cache = class_tup[1]
        p2 = class_tup[0][0]

        p2.port.factoryShop.items["1"] = [0, 1]
        p2.port.factoryShop.items["2"] = [1]

        p2.money = 0
        player.money = 4
        self.assertEqual(player.purchase_to_p(0, [0, 1]), 0)
        self.assertEqual(player.money, 2)
        self.assertEqual(p2.money, 2)
        self.assertEqual(len(player.port.portShop.items["2"]), 2)
        self.assertEqual(len(p2.port.factoryShop.items["1"]), 0)
        self.assertEqual(len(p2.port.factoryShop.items["2"]), 1)

        # TEST CASE 3

        class_tup = parse(self.return_state())
        player = class_tup[0][1]
        cache = class_tup[1]
        p2 = class_tup[0][0]

        p2.port.factoryShop.items["1"] = [0, 1]
        p2.port.factoryShop.items["2"] = [1, 3]

        p2.money = 0
        player.money = 4

        self.assertEqual(player.purchase_to_p(0, [0, 1, 1, 3]), 2)


if __name__ == '__main__':
    unittest.main()
