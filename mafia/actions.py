# -*- coding: utf-8 -*-

class Action(object):
    _resolved = False
    
    def __init__(self, game, player, target=None):
        self._game = game
        self._player = player
        self._target = target

    def get_priority(self):
        return self._priority

    def set_priority(self, priority):
        self._priority = priority

    def __eq__(self, other):
        return self.get_priority() == other.get_priority()

    def __ne__(self, other):
        return not self == other
    
    def __lt__(self, other):
        return self.get_priority() < other.get_priority()

    def __gt__(self, other):
        return self.get_priority() > other.get_priority()

    def __le__(self, other):
        return not self > other

    def __ge__(self, other):
        return not self < other
    
class JoinAction(Action):
    def __init__(self, game, player):
        self._game = game
        self._player = player
        self._priority = 0

    def resolve(self):
        print("Resolving Join action for {name}.".format(name=self._player.nickname))
        # TODO: make this less of a hack (probably use a decorator)
        if self._player not in self._game.players:
            self._game.add_player(self._player)
            self._game.add_action(AssignRoleAction(self._game, self._player))
        else:
            self._game.add_action(
                MessageAction(self._game, self._player,
                              "You are already in this game.", priority=0))
        self._resolved = True

class AssignRoleAction(Action):
    def __init__(self, game, player):
        self._game = game
        self._player = player
        self._priority = 90

    def resolve(self):
        print("Resolving Assign action for {name}.".format(name=self._player.nickname))
        assert not self._resolved
        self._player.set_role(self._game.get_next_role())
        self._game.add_action(RoleMessageAction(
            self._game,
            self._player))
        self._resolved = True

class RoleMessageAction(Action):
    def __init__(self, game, player, priority=99):
        self._game = game
        self._player = player
        self._priority = priority

    def resolve(self):
        print("Resolving Message action for {name}.".format(name=self._player.nickname))
        self._game.message_player(
            self._player,
            self._player.get_role().get_role_message(self._game))
        self._resolve = True

class MessageAction(Action):
    def __init__(self, game, player, message, priority=99):
        self._game = game
        self._player = player
        self._message = message
        self._priority = priority

    def resolve(self):
        self._game.message_player(self._player, self._message)
        self._resolved = True

class DayAction(Action):
    pass

class VotingAction(DayAction):
    pass

class NightAction(Action):
    pass
