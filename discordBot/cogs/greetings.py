import discord
from discord.ext import commands
from discordBot.models import DiscordGuild, DiscordUser


class Greatings(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    # member join event
    @commands.command
    async def on_member_join(member:discord.Member):
        guild = member.guild
        guildModel = DiscordGuild.objects.get(guildid = guild.id)
        welcome_channel_id = guildModel.greeting_welcome_channel
        deafult_role_id = guildModel.default_joining_role
        welcome_channel = guild.get_channel(welcome_channel_id)
        if deafult_role_id!=None:
            default_role = guild.get_role(deafult_role_id)
            await member.add_roles(default_role)
        background=Editor('assets/welcome_card.jpg')
        try:
            profile_img = await load_image_async(str(member.avatar.url))
        except:
            profile_img = await load_image_async(str(member.default_avatar.url))
        profile = Editor(profile_img).resize((150,150)).circle_image()
        font = Font.poppins(variant="bold", size=50)
        font_small = Font.poppins(variant="regular", size=25)
        background.paste(profile,(325,90))
        background.ellipse((325,90), 150,150,outline="white",stroke_width=5)
        if len(guild.name)>15:
            background.text((402,262),f"Welcome to",font=font,color="gray",align="center")
            background.text((400,260),f"Welcome to",font=font,color="White",align="center")
            background.text((402,302),f"{guild.name}",font=font,color="gray",align="center")
            background.text((400,300),f"{guild.name}",font=font,color="White",align="center")
        else:
            background.text((402,262),f"Welcome to {guild.name}",font=font,color="gray",align="center")
            background.text((400,260),f"Welcome to {guild.name}",font=font,color="White",align="center")
        background.text((402,52),f"{member.display_name}#{member.discriminator}",font=font_small,align='center',color="gray")
        background.text((400,50),f"{member.display_name}#{member.discriminator}",font=font_small,align='center')

        file = discord.File(fp=background.image_bytes , filename="img1.jpg")

        welcome_msg: str = database.get_connection().cursor().execute('select welcome from msg where guild_id = {}'.format(guild.id)).fetchone()[0]
        if welcome_msg != None:
            welcome_msg=welcome_msg.replace('<member>',r'{}').format(member.mention)
            welcome_msg=welcome_msg.replace('<name>',r'{}').format(member.display_name)
            await welcome_channel.send(content=welcome_msg,file=file)
        else:
            await welcome_channel.send(file=file)
        
        await fammy.Execute.setTotalMembers(bot,guild.id)












async def setup(bot:commands.Bot):
    await bot.add_cog(Greatings(bot))
    print("Greading cog loaded")


