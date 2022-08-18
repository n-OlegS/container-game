import unittest
import json

from modules import *
from game import *
from port import *


class MyTestCase(unittest.TestCase):
    def test_parse(self):
        with open('/Users/oleg/PycharmProjects/container_v2/state_3p.json', 'r') as f:
            class_tup = parse(json.load(f))
            players = class_tup[0]

        player = players[0]

        self.assertIsInstance(player, Player)
        self.assertEqual(player.pid, '0')
        self.assertEqual(player.debts, 0)
        self.assertEqual(player.money, 0)
        self.assertEqual(player.bank, class_tup[3])
        self.assertEqual(player.cache, class_tup[1])
        self.assertEqual(player.player_num, 3)
        self.assertEqual(player.warehouse_prices, [4, 5, 6, 7])
        self.assertEqual(player.plant_prices, [6, 9, 12])

        port = player.port
        self.assertIsInstance(port, Port)
        self.assertEqual(port.cache, class_tup[1])
        self.assertIsInstance(port.plants, dict)
        self.assertEqual(port.warehouses, 1)
        self.assertIsInstance(port.factoryShop, factoryShop)
        self.assertIsInstance(port.portShop, portShop)

        fshop = port.factoryShop
        self.assertIsInstance(fshop.items, dict)
        self.assertEqual(len(fshop.items["2"]), 1)
        self.assertEqual(fshop.total_items, 1)

        pshop = port.portShop
        self.assertIsInstance(pshop.items, dict)
        self.assertEqual(pshop.total_items, 0)

if __name__ == '__main__':
    unittest.main()
