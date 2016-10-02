# noinspection PyPep8
import datetime
import os
import sys
import time
import discord
import logging
from config import StartupType, dsc_email, dsc_password, sigma_version

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

print('Starting up...')
start_time = time.time()
time = time.time()
current_time = datetime.datetime.now().time()
current_time.isoformat()

if not os.path.isfile('config.py'):
    sys.exit(
        'Fatal Error: config.py is not present.\nIf you didn\'t already, rename config.example.json to config.json and try again.')
else:
    print('config.py present, continuing...')
# Data
from config import Token as token

if token == '': sys.exit('Token not provided, please open config.json and place your token.')

from config import Prefix as pfx
from config import cmd_help
# from config import Pushbullet as pb_key
# pb = pushbullet.Pushbullet(pb_key)

from plugin_manager import PluginManager
from plugins.help import Help
from plugins.league import LeagueOfLegends
from plugins.bns import BladeAndSoul
from plugins.osu import OSU
from plugins.urbandictionary import UrbanDictionary
from plugins.weather import Weather
from plugins.hearthstone import Hearthstone
from plugins.pokemon import Pokemon
from plugins.joke import Joke
from plugins.overwatch import Overwatch
from plugins.rip import Rip
from plugins.lastfm import LastFM
from plugins.cleverbot import Cleverbot
from plugins.echo import Echo
from plugins.nsfwperms import NSFWPermission
from plugins.gelbooru import Gelbooru
from plugins.r34 import R34
from plugins.nhentai import NHentai
from plugins.ehentai import EHentai
from plugins.e621 import E621
from plugins.hentaims import HentaiMS
from plugins.isthereanydeal import ITAD
from plugins.imdb import IMDB
from plugins.nihongo import WK
from plugins.nihongo import WKKey
from plugins.nihongo import Jisho
from plugins.mal import MAL
from plugins.unflip import Table
from plugins.vindictus import VindictusScrollSearch
from plugins.sonarr import Sonarr
from plugins.karaoke import VoiceChangeDetection
from plugins.karaoke import Control
from plugins.vndb import VNDBSearch
from plugins.utils import Reminder
from plugins.utils import Donators
from plugins.utils import OtherUtils
from plugins.reddit import Reddit
from plugins.utils import BulkMSG
# from plugins.nihongo import WaniKaniAutoCheck
# from plugins.nihongo import WKReviewFiller
# from plugins.reward import RewardOnMessage
# from plugins.reward import LevelCheck
from plugins.utils import PMRedirect
from plugins.selfrole import SelfRole
from plugins.world_of_warcraft import World_Of_Warcraft
from plugins.rocket_league import RocketLeague


# I love spaghetti!
class sigma(discord.Client):
    def __init__(self):
        super().__init__()
        self.plugin_manager = PluginManager(self)
        self.plugin_manager.load_all()

    async def on_voice_state_update(self, before, after):
        enabled_plugins = await self.get_plugins()
        for plugin in enabled_plugins:
            self.loop.create_task(plugin._on_voice_state_update(before, after))

    async def get_plugins(self):
        plugins = await self.plugin_manager.get_all()
        return plugins

    async def on_ready(self):
        gamename = pfx + cmd_help
        game = discord.Game(name=gamename)
        await client.change_status(game)
        server_amo = 0
        member_amo = 0
        for server in client.servers:
            server_amo += 1
            for member in server.members:
                member_amo += 1

        print('-----------------------------------')
        print('Logged in as: ' + client.user.name)
        print('Bot User ID: ' + client.user.id)
        print('Running discord.py version: ' + discord.__version__)
        print('Authors: AXAz0r, Awakening')
        print('Contributors: Mirai, Chaeldar')
        print('Bot Version: ' + sigma_version)
        print('Build Date: 25. September 2016.')
        print('-----------------------------------')
        print('Connected to [ ' + str(server_amo) + ' ] servers.')
        print('Serving [ ' + str(member_amo) + ' ] users.')
        print('\nSuccessfully connected to Discord!')
        # try:
        # if notify == 'Yes':
        #    pb.push_note('Sigma', 'Sigma Activated!')
        # else: print(client.user.name + ' activated.')
        # except: pass
        folder = 'cache/ow'
        try:
            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)
        except FileNotFoundError:
            pass

        if not os.path.exists('cache/lol/'):
            os.makedirs('cache/lol/')
        if not os.path.exists('cache/ow/'):
            os.makedirs('cache/ow/')
        if not os.path.exists('cache/rip/'):
            os.makedirs('cache/rip/')
        if not os.path.exists('cache/ani/'):
            os.makedirs('cache/ani/')

    async def on_message(self, message):
        # Static Strings
        # initiator_data = ('by: ' + str(message.author) + '\nUserID: ' + str(message.author.id) + '\nContent: [' + str(
        #    message.content) + ']\nServer: ' + str(message.server.name) + '\nServerID: ' + str(
        #    message.server.id) + '\n-------------------------')
        client.change_status(game=None)

        enabled_plugins = await self.get_plugins()
        for plugin in enabled_plugins:
            self.loop.create_task(plugin._on_message(message, pfx))


client = sigma()
if StartupType == '0':
    client.run(token)
elif StartupType == '1':
    client.run(dsc_email, dsc_password)
else:
    print('Failed loading connection settings.\nCheck your StartupType and make sure it\'s either 0 or 1.')
