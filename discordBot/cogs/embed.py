import discord
from discord.ext import commands,ipc
from typing import Union
from discord.ext.ipc.server import Server
from discord.ext.ipc.objects import ClientPayload
from discord.ext.ipc.errors import BaseException
from django.core.handlers.wsgi import WSGIRequest as Request



class Embeds(commands.Cog,name = "Discord Info"):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    # Server route for sending embed from website to discord
    @Server.route()
    async def send_embed(self,data: ClientPayload) -> discord.Message:
        """Send raw embed or dictionary embed to channel
        Attributes:

        embed:
        | Embed variable [discord.Embed, dict]
        channel:
        | Channel id [int]
        """
        if type(data.embed)==dict:
            embed = discord.Embed.from_dict(data.embed)
        else:
            embed = data.embed
        if type(data.channel) == int:
            channel =self.bot.get_channel(data.channel)
        elif type(data.channel) == discord.TextChannel:
            channel = data.channel
        message = await channel.send(embed=embed)
        





# Setting up cog
async def setup(bot):
    await bot.add_cog(Embeds(bot))
    print("discord cog is loaded")
