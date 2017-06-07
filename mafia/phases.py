# -*- coding: utf-8 -*-

from queue import PriorityQueue

class Phase(object):
    _priority = 0
    _actions = PriorityQueue()
    _log = []
    _ended = False
    _clearing = False

    def add_action(self, action):
        self._actions.put(action)
        self.clear_queue()

    def clear_queue(self):
        if not self._clearing:
            self._clearing = True
            while (not self._actions.empty()
                   and self._actions.queue[0].get_priority() <= self._priority):
                action = self._actions.get()
                action.resolve()
                self._log.append(action)
            self._clearing = False

    def increase_priority(self, priority=100):
        self._priority += priority
        self.clear_queue()

    def is_ended(self):
        return self._ended

class Signup(Phase):
    """Represents the Signup Phase."""
    def advance_phase(self):
        next_phase = Day(1)
        self._ended = True
        self.increase_priority()
        while not self._actions.empty():
            action = self._actions.get()
            action.set_priority(action.get_priority() - 100)
            Day(1).add_action(action)
        return next_phase

    def is_phase_end(self, game):
        return game.player_count() == game.role_count()

class Day(Phase):
    def __init__(self, day_count):
       self._day_count = day_count

class Night(Phase):
    pass
