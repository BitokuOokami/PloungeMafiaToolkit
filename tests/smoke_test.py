# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.insert(0, '../mafia')

from game import Game
from game import Player

from testclient.testmessenger import TestMessenger

class SmokeTest(unittest.TestCase):
    def setUp(self):
        self.messenger = TestMessenger()
        
    def test_smoke_test(self):
        game = Game('t,c,c,m', self.messenger)
        player_one = Player('one', 'one')
        player_two = Player('two', 'two')
        player_three = Player('three', 'three')
        player_four = Player('four', 'four')
        game.join(player_one)
        game.join(player_two)
        game.join(player_three)
        game.join(player_four)
        game.vote('one', 'three')
        game.vote('three', 'one')
        game.vote('two', 'three')
        game.vote('four', 'three')
        game.target('one', 'two')
        game.target('two', 'one')
        game.target('four', 'one')

if __name__ == '__main__':
    unittest.main()
