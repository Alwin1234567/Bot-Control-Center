"""
Header
"""
import discord
import discord.ext.commands as dec
import json
from Console import Console
import nest_asyncio
nest_asyncio.apply()
"""
body
"""
client = dec.Bot(command_prefix = json.load(open("config.json"))["BOT_PREFIX"], intents=discord.Intents.all())

@client.event
async def on_ready():
    console.logger.info("bot is now online")
    console.logger.info("bot started with name: {} and id: {}".format(console.client.user.name, console.client.user.id))


@client.command(brief = "stops all bots", description = "will try to stop all bots, if they don't comply, will force quit in 1 minute")
async def stop(context):
    await console.command_stop(context)
    


"""
commands
"""
console = Console(client)
client.run(console.tokens["Bot Control Center"])