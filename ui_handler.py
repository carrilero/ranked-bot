import discord
from discord import ui
from queue_manager import add_player, remove_player, get_queue, is_ready

class QueueView(ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @ui.button(label="Unirse a la cola", style=discord.ButtonStyle.green, custom_id="join_queue")
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user.id
        add_player(user)
        await interaction.response.send_message("Te has unido a la cola.", ephemeral=True)
        await self.update_message(interaction)

    @ui.button(label="Salir de la cola", style=discord.ButtonStyle.red, custom_id="leave_queue")
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user.id
        remove_player(user)
        await interaction.response.send_message("Has salido de la cola.", ephemeral=True)
        await self.update_message(interaction)

    async def update_message(self, interaction):
        queue = get_queue()
        await interaction.message.edit(content=f"**Cola de rankeds:** {len(queue)}/8 jugadores", view=self)
