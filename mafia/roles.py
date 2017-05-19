# -*- coding: utf-8 -*-

class Role:
    pass
    
class Town(Role):
    faction = 'Town'
    def game_ending_message(game):
        for player in game.players:
            if player.is_alive() and player.role.is_hostile():
                return None
        team = ', '.join(game.get_team(Town.faction))
        return ('All the hostiles have been defeated! '
                'Congratulations to the town: {team}'
                .format(team=team))

    def get_faction():
        return Town.faction

class Mafioso(Role):
    faction = 'Mafia'
    def name():
        return 'mafioso'

    def get_role_message(game):
        team = ', '.join(game.get_team(Mafioso.faction))
        return ('You are a mafioso! The mafia team consists of: {team}'
                .format(team=team))

    def is_hostile():
        return True

    def has_night_action():
        return True

    def game_ending_message(game):
        if game.count_faction(Mafioso.get_faction()) >= game.count_living()/2:
            team = ', '.join(game.get_team(Mafioso.faction))
            return ('The Mafia have taken over the town! '
                    'Congratulations to the mafia team: {team}'
                    .format(team=team))
        return None

    def get_faction():
        return Mafioso.faction

class Townie(Town):
    def name():
        return 'townie'

    def get_role_message(game):
        return 'You are a Townie!'

    def is_hostile():
        return False

    def has_night_action():
        return False

class Cop(Town):
    def name():
        return 'cop'

    def get_role_message(game):
        return 'You are the cop. You can investigate one player each night.'

    def is_hostile():
        return False

    def has_night_action():
        return True

    def resolve_action(player, target):
        if player.is_alive():
            player.append_to_night_message(
                'You follow {name} throughout the night '
                'and conclude that they are definitely {faction}!'
                .format(name=target.nickname, faction=target.role.get_faction()))
                
