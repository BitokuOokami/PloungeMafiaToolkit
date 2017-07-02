# -*- coding: utf-8 -*-

from queue import PriorityQueue

class Phase(object):
    def __init__(self):
        self._priority = 0
        self._actions = PriorityQueue()
        self._log = []
        self._ended = False
        self._checking = False

    def add_action(self, action):
        self._actions.put(action)
        self.check_queue()

    def check_queue(self):
        if not self._checking:
            self._checking = True
            while(not self._actions.empty()
                  and self._actions.queue[0].get_priority() <= self._priority):
                action = self._actions.get()
                action.resolve()
                self._log.append(action)
            self._checking = False

    def increase_priority(self, priority=100):
        self._priority += priority
        self.check_queue()

    def is_ended(self):
        return self._ended

    def is_checking(self):
        return self._checking

class Signup(Phase):
    """Represents the Signup Phase."""
    def advance_phase(self):
        next_phase = Day(1)
        self._ended = True
        self.increase_priority()
        while not self._actions.empty():
            action = self._actions.get()
            action.set_priority(action.get_priority() - 100)
            next_phase.add_action(action)
        return next_phase

    def is_phase_end(self, game):
        return game.player_count() == game.role_count()

class Day(Phase):
    def __init__(self, day_count):
       self._day_count = day_count
       super(Day, self).__init__()

    def advance_phase(self):
        next_phase = Night(self._day_count)
        self._ended = True
        (vote_count, target) = self.compile_votes()
        self.increase_priority()
        while not self._actions.empty():
            action = self.actions.get()
            action.set_priority(aciton.get_priority() - 100)
            next_phase.add_action(action)
        return next_phase

    def is_phase_end(self, game):
        (vote_count, target) = self.compile_votes()
        return vote_count > game.player_count()/2

    def compile_votes(self):
        votes_by_player = {}
        for action in self._log:
            player = action.get_player()
            target = action.get_target()
            votes[player] = target
        votes_for_player = {}
        for vote_target in votes_by_player.values():
            if vote_target in votes_for_player:
                votes_for_player[vote_target] += 1
            else:
                votes_for_player[vote_target] = 1
        return votes_for_player

class Night(Phase):
    def __init__(self, day_count):
        self.day_count = 1
