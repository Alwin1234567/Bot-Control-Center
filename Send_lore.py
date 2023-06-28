"""
Header
"""
from SubBot import SubBot
from discord.ext import commands, tasks
import datetime
"""
Body
"""
time = datetime.time(hour = 15)

class Send_lore(SubBot):
    
    def __init__(self, client, token):
        super().__init__(client, token)

    async def start_bot(self):
        await self.client.add_cog(Send_lore_events(self.client))
        await super().start_bot()
        self.cog = self.client.get_cog("Send_lore_events")
    
    
    async def trigger(self): 
        print(1)
        print(type(self.cog))
        await self.cog.send_message()
        
class Send_lore_events(commands.Cog):
    def __init__(self, client):
        self.input = 1123226096763142144
        self.output = 1123226125569634355
        self.client = client
        self.trigger = False
    
    @tasks.loop(time = time)
    async def timed_send(self):
        if datetime.now().weekday() != 5: return
        await self.send_message()
            
    
    async def send_message(self):
        async for message in self.client.get_channel(self.input).history(limit=1,oldest_first=True):
            last_message_content=message.content
            await message.delete()
            await self.client.get_channel(self.output).send(last_message_content)