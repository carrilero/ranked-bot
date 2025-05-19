import discord
from discord import ui
from queue_manager import add_player, remove_player, get_queue


class QueueView(ui.View):
    def __init__(self, static_message):
        super().__init__(timeout=None)
        self.static_message = static_message  # aquí almacenamos la referencia

    @ui.button(label="Unirse", style=discord.ButtonStyle.green, custom_id="join_queue")
    async def join(self, interaction, button):
        add_player(interaction.user.id, interaction.user.display_name)
        await self.refresh_message()
        await interaction.response.defer()

    @ui.button(label="Salir", style=discord.ButtonStyle.red, custom_id="leave_queue")
    async def leave(self, interaction, button):
        remove_player(interaction.user.id)
        await self.refresh_message()
        await interaction.response.defer()

    async def refresh_message(self):
        queue = get_queue()  # [(id, name), ...]
        if queue:
            desc = "\n".join(f"{i+1}. {name}" for i, (_, name) in enumerate(queue))
        else:
            desc = "No hay jugadores en la cola."

        embed = discord.Embed(
            title="🎮 Cola de Rankeds",
            description=desc,
            color=discord.Color.blue()
        )
        # Aquí static_message ya es el mensaje real
        await self.static_message.edit(embed=embed, view=self)