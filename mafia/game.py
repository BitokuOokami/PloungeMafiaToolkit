import random
from collections import deque
from .roles import Townie
from .roles import Cop
from .roles import Mafioso

next_phase = {'signup': 'day',
              'day': 'night',
              'night': 'day'}

legal_roles = {'t': Townie,
               'm': Mafioso,
               'c': Cop}

class Player(object):
    _role = None
    _status = None

    @property
    def role(self):
        return self._role

    def __init__(self, contact, nickname):
        self.contact = contact
        self.nickname = nickname
        self._status = 'alive'
        self.night_message = None

    def is_dead(self):
        return self._status == 'dead'

    def is_alive(self):
        return self._status == 'alive'

    def kill(self):
        self._status = 'dead'

    def set_role(self, role):
        self._role = role

    def __eq__(self, other):
        return isinstance(other, Player) and other.contact == self.contact

    def __ne__(self, other):
        return not self.__eq__(other)

    def resolve_action(self, target):
        self.role.resolve_action(self, target)

    def append_to_night_message(self, message: str):
        if self.night_message:
            self.night_message = self.night_message + ' ' + message
        else:
            self.night_message = message

    def get_night_message(self):
        return self.night_message

    def clear_night_message(self):
        self.night_message = None

class Game:
    messenger = None
    phase = None
    day_number = 0
    players = []
    roles = []
    votes = {}
    actions = {}
    public_message = None

    def __init__(self, game_setup: str, messenger):
        assert Game.is_valid_setup(game_setup), (
            'Please validate the setup before creating a game.')
        self.roles = Game.parse_roles(game_setup)
        self.phase = 'signup'
        self.day_number = 0
        self.players = []
        self.messenger = messenger
        self.messenger.message_all_players(
            'A new game has started, join with "!join"')

    def join(self, player) -> bool:
        '''Returns True if the player was able to join the game. '''
        if self.phase != "signup":
            return False
        if player not in self.players:
            self.players.append(player)
            self.messenger.message_all_players(
                '{name} has joined the fray!'.format(name=player.nickname))
        if len(self.players) == len(self.roles):
            self.assign_roles()
            self.advance_phase()
        return True

    def vote(self, player_name: str, target_name: str) -> bool:
        '''Returns True if the vote was cast.'''
        player = self.get_player(player_name)
        target = self.get_player(target_name)
        if self.phase != 'day':
            return False
        if player in self.players and target in self.players:
            self.votes[player.nickname] = target
            vote_count = 0
            for vote_target in self.votes.values():
                if target == vote_target:
                    vote_count += 1
            self.messenger.message_all_players(
                '{name} has voted for {target}, '
                'bringing the total to {count}'
                .format(name=player.nickname,
                        target=target.nickname,
                        count=vote_count))
            if vote_count > len(self.players)/2:
                target.kill()
                self.messenger.message_all_players(
                    'The crowd has spoken and {name} has been lynched! '
                    'They were a {role}.'.format(name=target.nickname,
                                                 role=target.role.name()))
                self.advance_phase()
            return True
        return False

    def target(self, player_name: str, target_name: str) -> bool:
        '''Returns True if the action was accepted.'''
        player = self.get_player(player_name)
        target = self.get_player(target_name)
        if (self.phase != 'night'
            or player.is_dead()
            or not player.role.has_night_action()):
            return False
        if player in self.players and target in self.players:
            self.actions[player.nickname] = target
            if self.all_actions_submitted():
                self.resolve_actions()
                self.send_night_messages()
                self.advance_phase()
            return True
        return False

    def is_valid_setup(game_setup: str) -> bool:
        roles =  game_setup.split(',')
        for role in roles:
            if role not in legal_roles:
                return False
        return True

    def parse_roles(game_setup: str):
        roles = []
        for role in game_setup.split(','):
            roles.append(legal_roles[role])
        return roles

    def assign_roles(self):
        assert len(self.roles) == len(self.players), (
            'Cannot assign roles if unequal to number of players')
        randomized_roles = random.sample(self.roles, len(self.players))
        for player in self.players:
            player.set_role(randomized_roles.pop())
        for player in self.players:
            self.messenger.message_player(player,
                                          player.role.get_role_message(self))

    def _assign_players_for_testing(self, *players):
        '''Add players to the game and assign roles deterministically.'''
        assert not self.players, 'Use this function instead of "join".'
        assert len(self.roles) == len(players), (
            '{role_count} roles, but {player_count} players'
            .format(role_count=len(self.roles), player_count=len(players)))
        players = deque(players)
        for role in self.roles:
            player = players.popleft()
            player.set_role(role)
            self.players.append(player)
            self.messenger.message_player(player,
                                          player.role.get_role_message(self))

    def unrecognized_roles(roles: str) -> list:
        roles = roles.split(',')
        unrecognized_roles = []
        for role in roles:
            if role not in legal_roles:
                unrecognized_roles.append(role)
        return unrecognized_roles

    def advance_phase(self):
        self.votes = {}
        self.actions = {}
        self.phase = next_phase[self.phase]
        if self.public_message:
            self.messenger.message_all_players(self.public_message)
            self.public_message = None
        if self.phase == 'day':
            self.day_number += 1
        if self.is_game_end():
            self.phase = None
        else:
            self.messenger.message_all_players(
                'It is now {phase} {number}'.format(
                    phase=self.phase, number=self.day_number))

    def is_game_end(self):
        for player in self.players:
            game_end_message = player.role.game_ending_message(self)
            if game_end_message:
                self.messenger.message_all_players(game_end_message)
                return True
        return False

    def get_player(self, name: str):
        for player in self.players:
            if player.nickname.lower() == name.lower():
                return player
            if player.contact == name:
                return player

    def count_faction(self, faction: str):
        count = 0
        for player in self.players:
            if player.role.get_faction() == faction:
                count += 1
        return count

    def count_living(self):
        count = 0
        for player in self.players:
            if player.is_alive():
                count += 1
        return count

    def get_team(self, faction: str):
        team = []
        for player in self.players:
            if player.role.get_faction() == faction:
                team.append(player.nickname)
        return team

    def all_actions_submitted(self):
        for player in self.players:
            if (player.is_alive()
                and player.role.has_night_action()
                and player.nickname not in self.actions):
                return False
        return True

    def resolve_actions(self):
        mafia_votes = {}
        mafia_target = None
        mafia_count = 0
        for player in self.players:
            if player.nickname in self.actions and player.role == Mafioso:
                target = self.actions[player.nickname]
                if target.nickname in mafia_votes:
                    mafia_votes[target.nickname] += 1
                else:
                    mafia_votes[target.nickname] = 1
                if mafia_votes[target.nickname] > mafia_count:
                    mafia_target = target
                    mafia_count += 1
        if mafia_target:
            mafia_target.kill()
            self.public_message = ('You all awake, but there is someone missing... '
                                   'looks like {name} has been killed during '
                                   'the night!'
                                   .format(name=mafia_target.nickname))
            mafia_target.append_to_night_message('You have been killed! =(')
        for player in self.players:
            if player.role.get_faction() == 'Mafia':
                player.append_to_night_message(
                    'You recieve word that {target} has been dispatched.'
                    .format(target=mafia_target.nickname))
        for player in self.players:
            if (player.is_alive()
                and player.role.has_night_action()
                and player.role != Mafioso):
                player.resolve_action(self.actions[player.nickname])

    def send_night_messages(self):
        for player in self.players:
            night_message = player.get_night_message()
            if night_message:
                self.messenger.message_player(player, night_message)
                player.clear_night_message()
            elif player.is_alive():
                self.messenger.message_player(player,
                                              'You have an uneventful night.')
