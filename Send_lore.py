"""
Header
"""
from SubBot import SubBot
from discord.ext import commands
"""
Body
"""

class Send_lore(SubBot):
    
    async def __init__(self, client, token):
        super().__init__(client, token)
        await self.client.add_cog(Send_lore_events(self.client))

    
    
        
class Send_lore_events(commands.Cog):
    def __init__(self, client):
        self.input = 1123226096763142144
        self.output = 1123226125569634355
        self.client = client
        
    @commands.Cog.listener()
    async def on_ready(self):
        async for message in self.client.get_channel(self.input).history(limit=1,oldest_first=True):
            last_message_content=message.content
            await message.delete()
            await self.client.get_channel(self.output).send(last_message_content)
        await self.stop_bot()