"""
Header
"""
from abc import ABC, abstractmethod
"""
Body
"""

class SubBot(ABC):
    
    def __init__(self, client, token):
        self.on = False
        self.client = client
        self.token = token
        self.task = None
    
    async def start_bot(self):
        self.on = True
        self.client.run(self.token)
    
    async def stop_bot(self):
        if not self.on: return
        self.on = False
        await self.client.close()
        if self.task != None: self.task.cancel
    
    async def switch_state(self):
        if self.on: await self.stop_bot()
        else: self.start_bot()