# -*- coding: utf-8 -*-

import asyncio

class Messenger:
    def __init__(self, client: "discord client", channel, loop=None):
        self.client = client
        self.channel = channel
        self.event_loop = asyncio.get_event_loop()

    def message_all_players(self, message: str):
        asyncio.ensure_future(self._message_internal(self.channel, message),
                              loop=self.event_loop)

    def message_player(self, player, message:str):
        asyncio.ensure_future(self._message_internal(player.contact, message),
                              loop=self.event_loop)

    async def _message_internal(self, channel, message: str):
        await self.client.send_message(channel, message)
