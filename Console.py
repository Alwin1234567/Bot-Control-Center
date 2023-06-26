"""
Header
"""
import json
import logging
from logger import setup_logger
from asyncio import sleep as asleep
import sys
import requests
"""
Body
"""


class Console:
    
    
    def __init__(self, client):
        setup_logger("main")
        Console.global_self = self
        self.logger = logging.getLogger("main")
        self.config = json.load(open("config.json"))
        self.tokens = json.load(open("tokens.json"))
        self.client = client
        
    
    async def remove_msg(self, msg, delay = 0):
        if delay > 0: asleep(delay)
        await msg.delete()
    
    
    async def command_stop(self, context):
        await self.remove_msg(context.message)
        await self.stop_server()
        asleep(5)
        sys.exit()
    
    async def stop_server(self):
        TOKEN = self.tokens["DBH_TOKEN"]
        url = self.tokens["DBH_URL"]
        headers = {
            'Authorization': 'Bearer {}'.format(TOKEN),
            'Content-Type': 'application/json',
            'Accept': 'Application/vnd.pterodactyl.v1+json'
        }
        data = '{ "signal": "kill" }'
        requests.post(url, headers=headers, data=data)
