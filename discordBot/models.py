from typing import Any
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser

# Create your models here.


# User model 
class DiscordUser(AbstractUser):
    userid = models.IntegerField("User ID",name="userid",primary_key=True)
    username = models.CharField("Username",name="username",max_length=100,unique=True)
    email = models.EmailField("Email",name="email")
    accesstoken = models.CharField("Access Token",name="accesstoken",max_length=100)
    

    def __str__(self) -> str:
        return self.username

@admin.register(DiscordUser)
class AdminDiscordUser(admin.ModelAdmin):
    pass



# Guild model
class DiscordGuild(models.Model):
    
    guildid = models.IntegerField("ID",name='guildid',primary_key=True)
    name = models.CharField("Name",name="name",max_length=100)
    icon = models.CharField("Icon Hash",name="iconhash",null=True,max_length=100)

    def __str__(self) -> str:
        return self.name

@admin.register(DiscordGuild)
class AdminDiscordGuild(admin.ModelAdmin):
    def __init__(self, model: type, admin_site: admin.AdminSite | None) -> None:
        super().__init__(model, admin_site)
        self.list_display = ['name','guildid']


# Ticket model
class Ticket(models.Model):
    guildID = models.ForeignKey("DiscordGuild",on_delete=models.CASCADE)
    creator = models.IntegerField
    
# Channel model
class Channel(models.Model):
    channels = [
        (0,"GUILD_TEXT"),
        (1,"DM"),
        (2,"GUILD_VOICE"),
        (3,"GROUP_DM"),
        (4,"GUILD_CATEGORY"),
        (5,"GUILD_ANNOUNCEMENT"),
        (10,"ANNOUNCEMENT_THREAD"),
        (11,"PUBLIC_THREAD"),
        (12,"PRIVATE_THREAD"),
        (13,"GUILD_STAGE_VOICE"),
        (14,"GUILD_DIRECTORY"),
        (15,"GUILD_FORUM"),
        (16,"GUILD_MEDIA"),
    ]
    id = models.IntegerField("ID",name="id",primary_key=True)
    # type = models.CharField("Channel Type",name='type',choices=channels,default=0,max_length=50)
    type = models.CharField("Channel Type",name='type',max_length=50)
    name = models.CharField("Name",name="name",max_length=100)
    guildid = models.ForeignKey(DiscordGuild, on_delete=models.CASCADE,name='guildid')
    
    def __str__(self) -> str:
        return self.name
    
@admin.register(Channel)
class AdminChannel(admin.ModelAdmin):
    def __init__(self, model: type, admin_site: admin.AdminSite | None) -> None:
        super().__init__(model, admin_site)
        self.list_display = ['id','name','type','guildid']

    
# Message model
class Message(models.Model):
    id = models.IntegerField("ID",name="id",primary_key=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE,name='channel')
    content = models.TextField('Content',name='content')
    guild = models.ForeignKey(DiscordGuild,on_delete = models.PROTECT,name='guildID')

    def __str__(self) -> str:
        return str(self.id)


@admin.register(Message)
class AdminMessage(admin.ModelAdmin):
    pass