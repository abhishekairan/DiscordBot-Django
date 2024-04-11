from discord.ext import ipc
from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest as Request
from asgiref.sync import sync_to_async


ipc_client = ipc.Client(secret_key="Keniv2.0")
# Embed page loading
async def embed(request: Request):
    session = await sync_to_async(request.session.get)('some_key')
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        fields = request.POST.get('field')
        print(fields)
        embedset = {
            'title':title,
            'description':description
        }
        await ipc_client.request('send_embed',embed = embedset)


    # return await render(request, 'embed.html')
    return await render(request, 'embed.html', {'session_data': session})




# Ticket page
async def ticket(request: Request):
    if request.method == 'POST':
        dataset = request.POST
        await ipc_client.request('sendPrimaryTicketMessage',dataset = dataset)
        
    return render(request, 'ticket.html',context={'page':'Ticket'})