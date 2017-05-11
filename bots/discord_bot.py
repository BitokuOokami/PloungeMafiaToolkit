import sys
sys.path.insert(0, '../')

import asyncio
import configparser
import discord

from mafia.game import Game
from mafia.game import Player
from mafiaclients.discord.messenger import Messenger

client = discord.Client()
games = {}
players = {}

class DiscordPlayer(Player):
    def __init__(self, member):
        nickname = member.nick if member.nick else member.name
        super(DiscordPlayer, self).__init__(member, nickname)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('----------')

@client.event
async def on_message(message):
    print(message.content)
    if message.content.startswith('!hi'):
        await client.send_message(message.author, "Hi!")
    if message.content.startswith('!game'):
        await new_game(message)
    if message.content.startswith('!join'):
        await join(message)
    if message.content.startswith('!vote'):
        await vote(message)
    if message.content.startswith('!target'):
        await target(message)

async def new_game(message):
    if message.channel.is_private:
        await client.send_message(
            message.channel,
            'Why are you trying to create a game in a private channel?')
        return
    if message.channel in games and games[message.channel].phase:
        await client.send_message(
            message.channel, 
            ('Please wait before the current game is over '
             'before starting a new game.'))
        return
    game_setup = message.content[len('!game'):].strip()
    if Game.is_valid_setup(game_setup):
        games[message.channel] = Game(
            game_setup, Messenger(client, message.channel))
    else:
        for role in Game.unrecognized_roles(game_setup):
            await client.send_message(
                message.channel,
                '{role} is not a recognized role.'.format(role=role))

async def join(message):
    if message.channel.is_private:
        await client.send_message(
            message.author,
            'Please join in the same channel as the game.')
        return
    if message.channel not in games:
        await client.send_message(
            message.channel,
            'Start a new game with \'!game\'.')
        return
    player = message.author
    if games[message.channel].join(DiscordPlayer(player)):
        players[player.name] = message.channel
    else:
        print('Signups are currently closed.')

async def vote(message):
    if message.channel.is_private:
        await client.send_message(
            message.author,
            'Please send votes through the public channel.')
        return
    if message.channel not in games:
        await client.send_message(
            message.channel,
            'Start a new game with \'!game\'.')
        return
    player_name = message.author.name
    target_name = message.content[len('!vote'):].strip()
    games[message.channel].vote(player_name, target_name)

async def target(message):
    if not message.channel.is_private:
        await client.send_message(
            message.author,
            'Pst... You might want to send night messages privately.')
        return
    if message.author.name not in players:
        await client.send_message(
            message.author,
            'Either join a game or start a new game using \'!game\'.')
        return
    player_name = message.author.name
    channel = players[player_name]
    target_name  = message.content[len("!target"):].strip()
    if target_name:
        player.target(player_name, target_name)

config = configparser.ConfigParser()
config.read('config.cfg')

client.run(config.get('OAuth2', 'token'))
