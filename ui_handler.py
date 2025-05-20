import discord
from discord import ui
from queue_manager import add_player, remove_player, get_queue


class QueueView(ui.View):
    def __init__(self, static_message):
        super().__init__(timeout=None)
        self.static_message = static_message

    @ui.button(label="Unirse", style=discord.ButtonStyle.green, custom_id="join_queue")
    async def join(self, interaction, button):
        user = interaction.user
        ok = add_player(user.id, user.display_name)
        if not ok:
            # Error porque ya estaba en cola o en partida
            await interaction.response.send_message(
                "❌ No puedes unirte: ya estás en cola o en partida activa.", 
                ephemeral=True
            )
            return

        await self.refresh_message()
        await interaction.response.send_message("✅ Te has unido a la cola.", ephemeral=True)

    @ui.button(label="Salir", style=discord.ButtonStyle.red, custom_id="leave_queue")
    async def leave(self, interaction, button):
        user = interaction.user
        remove_player(user.id)
        await self.refresh_message()
        await interaction.response.send_message("✅ Has salido de la cola.", ephemeral=True)

    async def refresh_message(self):
        queue = get_queue()
        if queue:
            desc = "\n".join(f"{i+1}. {name}" for i, (_, name) in enumerate(queue))
        else:
            desc = "No hay jugadores en la cola."
        embed = discord.Embed(
            title="🎮 Cola de Rankeds",
            description=desc,
            color=discord.Color.blue()
        )
        await self.static_message.edit(embed=embed, view=self)