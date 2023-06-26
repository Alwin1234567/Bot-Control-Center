"""
Header
"""
import json
import logging
from logger import setup_logger
from asyncio import sleep as asleep
import sys
import requests
from discord.ui import Button, View
import discord
"""
Body
"""


class Console:
    instance = None
    
    def __new__(cls, client):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
    
    def __init__(self, client):
        setup_logger("main")
        Console.global_self = self
        self.logger = logging.getLogger("main")
        self.config = json.load(open("config.json"))
        self.tokens = json.load(open("tokens.json"))
        self.client = client
        self.bots = self.config["Bots"]
        
    
    async def event_on_ready(self):
        self.logger.info("bot is now online")
        self.logger.info("bot started with name: {} and id: {}".format(self.client.user.name, self.client.user.id))
        print(self.client.guilds[0])
        self.console_channel = discord.utils.get(self.client.guilds[0].channels, name = "console")
        await self.create_console_msg()
    
    
    async def remove_msg(self, msg, delay = 0):
        if delay > 0: asleep(delay)
        await msg.delete()
    
    
    async def command_stop(self, context):
        await self.remove_msg(context.message)
        self.stop_server()
        await asleep(5)
        sys.exit()
    
    def stop_server(self):
        TOKEN = self.tokens["DBH_TOKEN"]
        url = self.tokens["DBH_URL"]
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN),
            'Content-Type': 'application/json',
            'Accept': 'Application/vnd.pterodactyl.v1+json'
        }
        data = '{ "signal": "kill" }'
        requests.post(url, headers=headers, data=data)
        
    
    async def create_console_msg(self):
        view = View()
        for bot in self.bots.values():
            view.add_item(Button(style = discord.ButtonStyle.secondary, label = bot["name"], emoji = bot["emoji"]))
        await self.console_channel.send("button?", view = view)

