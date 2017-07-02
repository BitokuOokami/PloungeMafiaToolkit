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

    def test_no_players_in_new_game(self):
        game = Game('t,c,m', self.messenger)
        assert game.player_count() == 0

    def test_player_count_increases_after_each_join(self):
        game = Game('t,c,m', self.messenger)
        game.join(Player('one', 'one'))
        assert game.player_count() == 1
        game.join(Player('two', 'two'))
        assert game.player_count() == 2
        game.join(Player('three', 'three'))
        assert game.player_count() == 3

    def test_player_only_joins_once(self):
        game = Game('t,c,m', self.messenger)
        game.join(Player('one', 'one'))
        game.join(Player('one', 'one'))
        assert game.player_count() == 1

    def test_role_messages_sent_to_each_player(self):
        game = Game('t,c,m', self.messenger)

        game.join(Player('one', 'one'))
        game.join(Player('two', 'two'))
        game.join(Player('three', 'three'))

        assert 'one' in [name for (name, message) in self.messenger.get_messages()]
        assert 'two' in [name for (name, message) in self.messenger.get_messages()]
        assert 'three' in [name for (name, message) in self.messenger.get_messages()]

    def test_message_not_sent_before_full(self):
        game = Game('t,c,m', self.messenger)

        game.join(Player('one', 'one'))
        assert 'one' not in [name for (name, message) in self.messenger.get_messages()]

    def test_roles_match_setup(self):
        # TODO: Make some test roles and a modular role parser.
        pass

    def test_target_fails_during_signup(self):
        game = Game('t,c,m', self.messenger)
        assert not game.target('one', 'two')

    def test_voting_fails_during_signup(self):
        game = Game('t,c,m', self.messenger)
        assert not game.vote('one', 'two')

    def test_all_actions_resolve_before_phase_advances(self):
        game = Game('t,t,m', self.messenger)
        game.join(Player('one', 'one'))
        game.join(Player('two', 'two'))
        game.join(Player('three', 'three'))

        assert len(game.get_current_phase()._log) == 0

class VotingTest(unittest.TestCase):
    def setUp(self):
        self.messenger = TestMessenger()
        self.game = Game('t,t,m', self.messenger)
        self.game.join(Player('one', 'one'))
        self.game.join(Player('two', 'two'))
        self.game.join(Player('three', 'three'))

    def test_vote_target_dies(self):
        assert self.game.get_player('three').is_alive()
        self.game.vote('one', 'three')
        self.game.vote('two', 'three')
        assert self.game.get_player('three').is_dead()
    
class NightActionTest(unittest.TestCase):
    def setUp(self):
        self.messenger = TestMessenger()
        self.game = Game('t,c,m', self.messenger)
        self.game._assign_players_for_testing(
            Player('one', 'one'),
            Player('two', 'two'),
            Player('three', 'three'))
        # Advance the phases twice to start tests in the night phase.
        self.game.advance_phase()
        self.game.advance_phase()

    def test_night_messages_sent_to_each_player(self):
        self.messenger.clear_messages()
        self.game.target('three', 'one')
        self.game.target('two', 'one')
        assert 'one' in [name for (name, message) in self.messenger.get_messages()]
        assert 'two' in [name for (name, message) in self.messenger.get_messages()]
        assert 'three' in [name for (name, message) in self.messenger.get_messages()]

    def test_mafia_mafia_kill_happens_before_cop(self):
        self.messenger.clear_messages()
        self.game.target('three', 'two')
        self.game.target('two', 'one')
        assert ('two', 'You have been killed! =(') in self.messenger.get_messages()
        

if __name__ == '__main__':
    unittest.main()
