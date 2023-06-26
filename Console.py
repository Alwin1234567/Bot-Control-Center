"""
Header
"""
import discord
import discord.ext.commands as dec
import json
import logging
from logger import setup_logger
"""
Body
"""

client = dec.Bot(command_prefix = json.load(open("config.json"))["BOT_PREFIX"])

@client.event
async def on_ready():
    logger.warning("bot is now online")
    logger.info("bot started with name: {} and id: {}".format(client.user.name, client.user.id))

setup_logger("main")
logger = logging.getLogger("main")
TOKEN = json.load(open("tokens.json"))["Eden"]
client.run(TOKEN)