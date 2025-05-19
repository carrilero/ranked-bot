import discord
from discord.ext import commands
from config import GAME_MODES, MAPS
import random

async def start_mode_voting(bot, channel, players):
    await channel.send("Votad el **modo de juego**:")
    view = VotingView(GAME_MODES)
    await channel.send(view=view)

class VotingView(discord.ui.View):
    def __init__(self, options):
        super().__init__()
        for opt in options:
            self.add_item(VoteButton(opt))

class VoteButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=label, style=discord.ButtonStyle.primary)

    async def callback(self, interaction):
        await interaction.response.send_message(f"Has votado: {self.label}", ephemeral=True)
