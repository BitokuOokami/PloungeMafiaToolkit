# -*- coding: utf-8 -*-

class Action(object):
    _resolved = False

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
        assert not self._resolved
        self._player.set_role(self._game.get_next_role())
        self._game.add_action(RoleMessageAction(
            self._game,
            self._player))
        self._resolved = True

class RoleMessageAction(Action):
    def __init__(self, game, player):
        self._game = game
        self._player = player
        self._priority = 99

    def resolve(self):
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

class PublicPost(Action):
    def __init__(self, game, message, priority=99):
        self._game = game
        self._message = message
        self._priority = priority

    def resolve(self):
        self._game.message_all_players(self._message)
        self._resolved = True
        
class DayAction(Action):
    pass

class VoteAction(DayAction):
    def __init__(self, game, player, target):
        self._game = game
        self._player = player
        self._target = target
        self._priority = 0

    def resolve(self):
        vote_count = self._game.vote_count(self._target)
        if vote_count > self._game.count_living()/2:
            self._game.add_action(Lynch(self._game, self._target))
        self._resolved = True

    def get_target(self):
        return self._target

class Lynch(DayAction):
    def __init__(self, game, target):
        self._game = game
        self._target = target
        self._priority = 90

    def resolve(self):
        self._target.lynch()
        self._resolved = True

class NightAction(Action):
    pass
