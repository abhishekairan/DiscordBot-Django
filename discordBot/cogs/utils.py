import random
import discord
import traceback
from discord.ext import commands,ipc
from discord.ext.ipc.server import Server
from discord.ext.ipc.errors import BaseException
from discord.ext.ipc.objects import ClientPayload
from django.core.handlers.wsgi import WSGIRequest as Request


# Generating random custom id
def get_custom_id() -> str:
    lst = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9','.',',','/']
    id = ''
    for a in range(25):
        id += random.choice(lst)
    return id




# Cog Class for Utils
class Utils(commands.Cog,name="Utils"):
    # Init function to set bot in class
    def __init__(self,bot:commands.Bot):
        self.bot=bot
        self.ipcClient = ipc.Client(secret_key="Keniv2.0")
        
# Setting up cog
async def setup(bot):
    await bot.add_cog(Utils(bot))
    print("Utils cog is loaded")
