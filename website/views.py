import json
import config
import requests
from discord.ext.ipc import Client
from asgiref.sync import sync_to_async, async_to_sync
from django.contrib.auth import logout, login
from django.http import HttpResponse
from discordBot.models import DiscordGuild, DiscordUser, Message,Channel
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from config import BOT_TOKEN
from django.core.handlers.wsgi import WSGIRequest as Request

ipc = Client(secret_key="Keniv2.0")


# Create your views here.



# Getting user data and logging
async def authenticateUser(request:Request):
    if request.method =="GET":
        code = request.GET.get('code')
        access_token = exchange_code(code)
        userdata = exchange_access_token(access_token)
        user =await createOrUpdateUser(request,userdata,access_token)
        # print(user)
        await sync_to_async(login)(request,user)
        # request.session.cycle_key()
        return redirect('/home')
    if request.method == "POST":
        print("Method is post")
    return HttpResponse("Hello")




# Exchanging code got from discord auth api for user
def exchange_code(code):
    API_ENDPOINT = config.API_ENDPOINT
    CLIENT_ID = config.CLIENT_ID
    CLIENT_SECRET = config.CLIENT_SECRET
    REDIRECT_URI = config.REDIRECT_URI
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))
    r.raise_for_status()
    access_token = r.json()['access_token']
    return access_token




# Exchanging access token for user details
def exchange_access_token(access_token):
    user = requests.get('https://discord.com/api/v10/users/@me', headers={
        'Authorization': 'Bearer %s' % access_token
    })
    user.raise_for_status()
    return user.json()

# Example Response from api
# {'id': '910848806625607710','username': 'fammyplayer', 'avatar': '4e5f8d7e81326c2d0f96df9d26c8c49f', 'discriminator': '0', 'public_flags': 128, 'premium_type': 0, 'flags': 128, 'banner': None, 'accent_color': 108714, 'global_name': 'Fammy player', 'avatar_decoration_data': None, 'banner_color': '#01a8aa', 'mfa_enabled': True, 'locale': 'en-US', 'email': 'cubicfammy@gmail.com', 'verified': True} 


# Exchanging code got from discord auth api for guilds
def exchange_guild(access_token):
    guilds = requests.get('https://discord.com/api/v10/users/@me/guilds', headers={
        'Authorization': 'Bearer %s' % access_token
    })
    guilds.raise_for_status()
    accessableGuilds = [guild for guild in guilds.json() if(int(guild['permissions']) & 0x20 == 32)] # -> [{'id': '910860626837004308', 'name': 'Club Colony SMP', 'icon': '9e53b893f48b4dca63b4d53c7532e66f', 'owner': False, 'permissions': '562949953421311', 'features': ['AUTO_MODERATION', 'COMMUNITY', 'CHANNEL_ICON_EMOJIS_GENERATED', 'THREE_DAY_THREAD_ARCHIVE', 'DISOVERABLE', 'TEXT_IN_VOICE_ENABLED', 'MEMBER_VERIFICATION_GATE_ENABLED', 'WELCOME_SCREEN_ENABLED', 'NEWS', 'INVITE_SPLASH', 'ANIMATED_ICON', 'SOUNDBOARD', 'PREVIEW_ENABLED', 'ENABLED_DISCOVERABLE_BEFORE']}]
    return accessableGuilds


# function to get joinned guilds ids in a list
def get_joined_guilds():
    joinedGuildsInt = list(DiscordGuild.objects.values_list('guildid',flat=True))
    joinedGuilds = list(map(str, joinedGuildsInt))
    # print(joinedGuilds)
    return joinedGuilds
    


@sync_to_async
def createOrUpdateUser(request: Request, user: dict,accesstoken: str):
    username = user['username']
    userid = user['id']
    email = user['email']
    if DiscordUser.objects.all().filter(userid=userid).exists():
        DiscordUser.objects.all().filter(userid=userid).update(accesstoken= accesstoken)
        user = DiscordUser.objects.get(userid=userid)
        return user
    else:
        user = DiscordUser.objects.create(userid = userid,username = username,email = email,accesstoken = accesstoken)
        return user


# Function to get channels of a guild
def getGuildChannels(request: Request,guildID: int):
    if request.user.is_authenticated:
        r =requests.get(f'{config.API_ENDPOINT}/guilds/{guildID}/channels',headers={
            'Authorization': 'Bot %s' % BOT_TOKEN
        })
        return r.json()
        # print(r.json()) => [{'id': '1061154580890648636', 'type': 4, 'flags': 0, 'guild_id': '913827207355441193', 'name': 'Airport', 'parent_id': None, 'position': 1, 'permission_overwrites': [{'id': '913827207355441193', 'type': 0, 'allow': '0', 'deny': '377957124096'}]},]
        
        
# function to send a message into discord
def sendMessage(request: Request,channel,message):
    if request.user.is_authenticated:
        message_content = {
            'content': message
        }
        response = requests.post(f'{config.API_ENDPOINT}/channels/{channel}/messages',     headers={
            'Authorization': 'Bot %s' % BOT_TOKEN,
            'Content-Type': 'application/json'
        },data=json.dumps(message_content))
        if response.status_code == 200:
            print('Message sent successfully!')
        else:
            print('Failed to send message. Status code:', response.status_code)
            print('Response:', response.text)
        return response.json() # -> {'id': '1222916826153877546', 'type': 0, 'content': 'this is a test messsgae', 'channel_id': '1061156604583624734', 'author': {'id': '911086684135895040', 'username': 'keni', 'avatar': 'f75f5e7c1785bc607a07ceaf82dd6ef8', 'discriminator': '7175', 'public_flags': 0, 'premium_type': 0, 'flags': 0, 'bot': True, 'banner': None, 'accent_color': None, 'global_name': None, 'avatar_decoration_data': None, 'banner_color': None}, 'attachments': [], 'embeds': [], 'mentions': [], 'mention_roles': [], 'pinned': False, 'mention_everyone': False, 'tts': False, 'timestamp': '2024-03-28T14:34:52.051000+00:00', 'edited_timestamp': None, 'flags': 0, 'components': [], 'referenced_message': None}


def add_message(message:json,guildID:int):
    guilddata = DiscordGuild.objects.filter(guildid=guildID).first()
    channel = Channel.objects.filter(id=message['channel_id']).first()
    msg = Message.objects.create(id=message['id'],channel = channel, content = message['content'],guildID=guilddata)
    return msg



def main(request: Request):
    if request.user.is_authenticated:
        user = request.user
        access_token = user.accesstoken
        accessableGuilds = exchange_guild(access_token)
        joinedGuilds = get_joined_guilds()
        return render(request,'welcome-cnf.html',context={'user':user,'guilds':accessableGuilds,'page':"welcome",'joinedGuilds':joinedGuilds})
    else:
        return render(request, 'base.html',context={'page':'Home'})

def Discordlogin(request: Request):
    return redirect("https://discord.com/api/oauth2/authorize?client_id=911086684135895040&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fauth&scope=identify+guilds+email")

def discordLogout(request):
    logout(request)
    return redirect('/home')
    
@login_required
def guild(request: Request, id: int):
    guilddata = DiscordGuild.objects.filter(guildid=id).first()
    return render(request, 'guild.html', context={'guild': guilddata})

@login_required
def guild_message(request: Request,id:int):
    guilddata = DiscordGuild.objects.filter(guildid=id).first()
    messsages = Message.objects.filter(guildID = id)
    channels = getGuildChannels(request,id)
    if request.method == "POST":
        message = request.POST.get('description')
        channel = request.POST.get('channels')
        r = sendMessage(request,channel,message)
        add_message(r,id)
        return redirect(f'/guild/message/{id}',context={'guild': guilddata,"channels":channels,"messages": messsages})
    return render(request,'guild-message.html',context={'guild': guilddata,"channels":channels,"messages": messsages})

@login_required
def deleteMessage(request: Request,channelid: int, messageid:int,guildid:int):
    try:
        
        Message.objects.filter(id=messageid).first().delete()

        response = requests.delete(
            f'{config.API_ENDPOINT}/channels/{channelid}/messages/{messageid}',
            headers = {
                'Authorization': f'Bot {BOT_TOKEN}',
            }
        )
        if response.status_code == 204:
            print("Message deleted successfully!")
        else:
            print(f"Failed to delete message. Status code: {response.status_code}")
        return redirect(f'/guild/message/{guildid}')
    except:
        pass
    
@login_required
def guild_channels(request: Request,id:int):
    guilddata = DiscordGuild.objects.filter(guildid=id).first()
    # messsages = Message.objects.filter(guildID = id)
    channels = Channel.objects.filter(guildid = id)
    return render(request,'guild-channels.html',context={"channels":channels,'guild': guilddata})
