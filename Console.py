"""
Header
"""
import json
import logging
from logger import setup_logger
from asyncio import sleep as asleep
import sys
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
        sys.exit()
