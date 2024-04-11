import os
import sys
import django

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Keni_V2.settings')
django.setup()

# Import Django models and other components
from discordBot.models import Message, DiscordGuild, Channel
from discord.ext import commands, ipc
from asgiref.sync import sync_to_async
from config import BOT_TOKEN
import discord
import asyncio
import traceback

# Your remaining code goes here...

# Define the bot
class KeniBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ipc = ipc.Server(self, secret_key="Keniv2.0")

    async def setup_hook(self) -> None:
        await self.ipc.start()
        
    async def on_ready(self):
        print("Bot is ready")

        cogs = [
            # 'discordBot.cogs.greetings',
            'discordBot.cogs.embed',
            'discordBot.cogs.ticket',
            'discordBot.cogs.utils',
            'discordBot.cogs.routes',
        ]
        for extension in cogs:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(f"Error loading {extension}")
                traceback.print_exc()

        for guild in self.guilds:
            await add_guild(guild)

    async def on_ipc_ready(self):
        print("IPC server is ready.")

    async def on_ipc_error(self, endpoint, error):
        print(type(error))
        print(endpoint, "raised", error)
    
    async def on_guild_join(self,guild: discord.Guild):
        await add_guild(guild)
        for channel in guild.channels:
            await sync_to_async(add_channel)(channel)
    async def on_guild_remove(self,guild: discord.Guild):
        await remove_guild(guild)
    async def on_message_delete(self,message: discord.Message):
        guild = message.guild
        for channel in guild.channels:
            await sync_to_async(add_channel)(channel)
        await sync_to_async(remove_message)(message)

bot = KeniBot(command_prefix=">", intents=discord.Intents.all())

# Define bot commands and functions
@bot.command(name='guild')
async def guilds(ctx):
    await ctx.send(bot.guilds)



@bot.command(name="rc")
async def reload_cogs(ctx):
    cogs = [
        'discordBot.cogs.embed',
        'discordBot.cogs.ticket',
        'discordBot.cogs.utils',
    ]
    for cog in cogs:
        await bot.unload_extension(cog)
        await bot.load_extension(cog)



def start_bot():
    asyncio.run(bot.run(BOT_TOKEN))



@sync_to_async
def add_guild(guild: discord.Guild):
    if not DiscordGuild.objects.filter(guildid=guild.id).exists():
        try:
            iconhash = guild.icon.key
        except:
            iconhash = None
        DiscordGuild.objects.create(guildid=guild.id, name=guild.name, iconhash=iconhash)
        print(f'Guild {guild.name} is added into database with id {guild.id} and iconHash {iconhash}')



# Add channel into database
def add_channel(channel):
    if type(channel)==dict:
        if not Channel.objects.filter(id=channel['id']):
            # print(f"id={channel.id},type={channel.type},name={channel.name},guildid={channel.guild_id}")
            createdChannel = Channel.objects.create(
                id=channel['id'],
                type=channel['type'],
                name=channel['name'],
                guildid=channel['guild_id']
            )
            print(f'Channel {channel["name"]} has been added to database with channel id {channel["id"]}')
            discord.enums._EnumValue_ChannelType
            return createdChannel
    else:
        if not Channel.objects.filter(id=channel.id):
            id=channel.id
            # print(id)
            name=channel.name
            # print(name)
            channelType=channel.type
            # print(channelType)
            try:
                guildid=channel.guild_id
            except:
                guildid=channel.guild.id
            # print(guildid)
            guild = DiscordGuild.objects.filter(guildid=(guildid)).first()
            # print(guild)
            createdChannel = Channel.objects.create(
                id=id,
                type=channelType,
                name=name,
                guildid=guild
            )
            print(f'Channel {channel.name} has been added to database with channel id {channel.id}')
            return createdChannel
        
        
        
@sync_to_async
def remove_guild(guild: discord.Guild):
    if DiscordGuild.objects.filter(guildid=guild.id).exists():
        DiscordGuild.objects.filter(guildid=guild.id).delete()
        print(f'Guild {guild.name} is deleted from database with id {guild.id}')



def remove_message(message: discord.Message):
    if Message.objects.filter(id=message.id).exists():
        Message.objects.filter(id=message.id).delete()
        print(f'Message with if {message.id} and content {message.content} has been deleted')
        


if __name__ == "__main__":
    start_bot()
