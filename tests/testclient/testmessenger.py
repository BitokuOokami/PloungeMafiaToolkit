# -*- coding: utf-8 -*-

class TestMessenger:
    def __init__(self):
        self.messages = []

    def message_all_players(self, message: str):
        self.messages.append(('public', message))
        print ('public: {message}'.format(message=message))

    def message_player(self, player, message: str):
        self.messages.append((player.nickname, message))
        print ('{name}: {message}'.format(name=player.nickname, message=message))

    def get_messages(self):
        return self.messages

    def clear_messages(self):
        self.messages = []
