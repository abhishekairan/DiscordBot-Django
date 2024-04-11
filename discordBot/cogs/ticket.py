import discord
from discord.ext import commands,ipc
from typing import Union
import discordBot.cogs.views as Views
from discord.ext.ipc.server import Server
from discord.ext.ipc.objects import ClientPayload
import traceback
from django.core.handlers.wsgi import WSGIRequest as Request
from discord.ext.ipc.errors import BaseException


# Cog Class for ticket managment
class Ticket(commands.Cog,name="Tickets"):
    # Init function to set bot in class
    def __init__(self,bot:commands.Bot):
        self.bot=bot
        self.ipcClient = ipc.Client(secret_key="Keniv2.0")
        
    # Server route for sending primary ticket message
    @Server.route()
    async def sendPrimaryTicketMessage(self,data: ClientPayload):
        try:
            dataset = data.dataset
            embedAttributes = ["author","colour","description","fields","footer","image","provider","thumbnail","timestamp","title","type","url","video"]
            embedset = {}
            for key, value in dataset.items():
                # print(key,value)
                if key in embedAttributes:
                    embedset[key] =  value
            # print(embedset)
            embed = discord.Embed.from_dict(embedset)
            # print(dataset.get('channel'))
            channel = self.bot.get_channel(int(dataset.get('channel')))
            ticketview = Views.TicketView()
            await channel.send(embed=embed,view=ticketview)
        except Exception as e:
            traceback.print_exc()







    @commands.command()
    async def tt(self,ctx):
        ticketview = Views.TicketView()
        embed= discord.Embed(description="test")
        await ctx.send(view=ticketview,embed=embed)
        
    @commands.command()
    async def getuser(self,ctx,userid):
        user = await self.bot.fetch_user(883016982990061588)
        print(user.display_name)
        
    @commands.command()
    async def avatar(self,ctx,userid):
        user = await self.bot.fetch_user(userid)
        embed = discord.Embed(
            description=f"# {user.display_name}'s avatar",
        )
        embed.set_image(url=user.display_avatar.url)
        print(user.display_avatar.url)
        await ctx.send(embed = embed)







# Setting up cog
async def setup(bot):
    await bot.add_cog(Ticket(bot))
    print("ticket cog is loaded")
