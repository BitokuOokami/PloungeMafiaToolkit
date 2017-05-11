# -*- coding: utf-8 -*-

class TestMessenger:
    def message_all_players(self, message: str):
        print ('public: {message}'.format(message=message))

    def message_player(self, player, message: str):
        print ('{name}: {message}'.format(name=player.nickname, message=message))
