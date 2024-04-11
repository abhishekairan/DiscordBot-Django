from django.core.management.base import BaseCommand, CommandError
from discordBot.views import start_bot

# Django command for initiating `runbot` command
class Command(BaseCommand):
    help = 'This is bot help'

    def handle(self, *args, **options) -> None:
        bot = start_bot()
        
        # Assuming start_bot() returns the bot instance
        print("Testing...")
