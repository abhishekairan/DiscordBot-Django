import discord
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.ext import commands,ipc
from discord.interactions import Interaction
from discord.partial_emoji import PartialEmoji
from discord.ui import View, Button
from typing import Any, Coroutine, Optional, Union
from discordBot.cogs.utils import get_custom_id


class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(style=discord.ButtonStyle.primary,label="test")
    async def btn(self,interaction, button):
        pass
    
    class TicketButton(Button):
        def __init__(self):
            super().__init__(label="test",custom_id=get_custom_id())

        def callback(self, interaction: Interaction) -> Coroutine[Any, Any, Any]:
            pass