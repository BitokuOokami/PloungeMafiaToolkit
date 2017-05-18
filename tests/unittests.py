# -*- coding: utf-8 -*-

import unittest
import sys
sys.path.insert(0, '../')

from mafia.game import Game
from mafia.game import Player
from testclient.testmessenger import TestMessenger

class NewGameTest(unittest.TestCase):
    def setUp(self):
        self.messenger = TestMessenger()

    def test_role_messages_sent_to_each_player(self):
        self.game = Game('t,c,m', self.messenger)

        self.game.join(Player('one', 'one'))
        self.game.join(Player('two', 'two'))
        self.game.join(Player('three', 'three'))

        assert 'one' in [name for (name, message) in self.messenger.get_messages()]
        assert 'two' in [name for (name, message) in self.messenger.get_messages()]
        assert 'three' in [name for (name, message) in self.messenger.get_messages()]

    def test_message_not_sent_before_full(self):
        self.game = Game('t,c,m'), self.messenger)

        self.game.join(Player('one', 'one'))
        assert 'one' not in [name for (name, message) in self.messenger.get_messages()]

    def test_roles_match_setup(self):
        # TODO: Make some test roles and a modular role parser.
        pass

    def test_target_fails_during_signup(self):
        self.game = Game('t,c,m', self.messenger)
        assert not self.target('one', 'two')

    def test_voting_fails_during_signup(self):
        self.game = Game('t,c,m', self.messenger)
        assert not self.vote('one', 'two')

    def test_join_fails_if_player_is_already_in_game(self):
        self.game = Game('t,c,m', self.messenger)
        assert self.join('one')
        assert self.join('one')

class VotingTest(unittest.TestCase):
    '''Currently unused.'''
    def setUp(self):
        self.messenger = TestMessenger()
        self.game = Game('t,t,m', self.messenger)
        self.join(Player('one', 'one'))
        self.join(Player('two', 'two'))
        self.join(Player('three', 'three'))

    def test_pass(self):
        pass
    
class NightActionTest(unittest.TestCase):
    def setUp(self):
        pass
        
if __name__ == '__main__':
    unittest.main()
