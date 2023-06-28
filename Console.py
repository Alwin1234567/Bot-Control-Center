"""
Header
"""
import json
import logging
from logger import setup_logger
from asyncio import sleep as asleep
from asyncio import create_task
import sys
import requests
from discord.ui import Button, View
import discord
from Send_lore import Send_lore
import discord.ext.commands as dec
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
        self.console_msg = None
        self.msg_wait = list()
        self.bot_classes = dict()
        
        
    
    async def event_on_ready(self):
        self.logger.info("bot is now online")
        self.logger.info("bot started with name: {} and id: {}".format(self.client.user.name, self.client.user.id))
        self.console_channel = discord.utils.get(self.client.guilds[0].channels, name = "console")
        self.status_category = discord.utils.get(self.client.guilds[0].categories, name = "Status")
        await self.create_status()
        await self.create_console_msg() #end of on_ready due to infinite loop
    
    
    async def remove_msg(self, msg, delay = 0):
        if delay > 0: 
            task = create_task(self.delayed_remove_msg(msg, delay))
            self.msg_wait.append(task)
            asleep(delay)
            self.msg_wait.remove(task)
        else: await msg.delete()
    
    async def delayed_remove_msg(self, msg, delay):
        try: asleep(delay)
        except: pass
        await msg.delete()
    
    
    async def command_stop(self, context = None):
        try:
            for bot in self.bot_classes: await bot.stop_server() # stop all bots
        except: pass
        try:
            for bot in self.bots.values(): await self.client.get_channel(bot["status_channel_id"]).delete()
        except: pass
        for task in self.msg_wait: task.cancel() # instantly run all pending msg removals
        if context != None: await self.remove_msg(context.message) # remove console msg
        try:
            if self.console_msg != None: await self.remove_msg(self.console_msg)
        except: pass
        self.stop_server()
        await asleep(1)
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
            view.add_item(Button(style = discord.ButtonStyle.primary, label = bot["name"], custom_id = bot["name"]))#, emoji = bot["emoji"]))
        view.add_item(Button(style = discord.ButtonStyle.danger, label = "stop", custom_id = "stop", emoji = "⛔"))
        self.console_msg = await self.console_channel.send("button?", view = view)
        while True:
            interaction = await self.client.wait_for("interaction", check=lambda interaction: interaction.data["component_type"] == 2 and interaction.channel == self.console_channel)
            await self.button_trigger(interaction.data["custom_id"])
            await interaction.response.defer()

    async def button_trigger(self, ID):
        if ID == "stop":
            await self.command_stop()
            return
        if ID in self.bots.keys():
            if ID in self.bot_classes.keys(): await self.stop_bot(ID)
            else: await self.start_bot(ID)
                
    
    async def start_bot(self, name):
        bot = eval('{0}(self.get_client(), self.tokens["{0}"])'.format(name))
        self.bot_classes[name] = bot
        task = create_task(bot.start_bot())
        bot.task = task
        await self.client.get_channel(self.bots[name]["status_channel_id"]).edit(name = "{} 🟢".format(name))
        return self.bot_classes[name]
    
    
    async def stop_bot(self, name):
        await self.bot_classes[name].stop_bot()
        del self.bot_classes[name]
        await self.client.get_channel(self.bots[name]["status_channel_id"]).edit(name = "{} 🔴".format(name))
        
    def get_client(self): return dec.Bot(command_prefix = self.config["BOT_PREFIX"], intents=discord.Intents.all())
            
    async def create_status(self):
        for key in self.bots.keys():
            status = await self.status_category.create_voice_channel("{} 🔴".format(key))
            self.bots[key]["status_channel_id"] = status.id

