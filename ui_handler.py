class QueueView(ui.View):
    def __init__(self, static_message):
        super().__init__(timeout=None)
        self.static_message = static_message

    @ui.button(label="Unirse", style=discord.ButtonStyle.green, custom_id="join_queue")
    async def join(self, interaction, button):
        user = interaction.user
        add_player(user.id, user.display_name)
        await self.refresh_message()
        await interaction.response.defer()

    @ui.button(label="Salir", style=discord.ButtonStyle.red, custom_id="leave_queue")
    async def leave(self, interaction, button):
        user = interaction.user
        remove_player(user.id)
        await self.refresh_message()
        await interaction.response.defer()

    async def refresh_message(self):
        queue = get_queue()  # devuelve [(id, name), ...]
        if queue:
            lines = [f"{i+1}. {name}" for i, (_, name) in enumerate(queue)]
            desc = "\n".join(lines)
        else:
            desc = "No hay jugadores en la cola."

        embed = discord.Embed(
            title="🎮 Cola de Rankeds",
            description=desc,
            color=discord.Color.blue()
        )
        await self.static_message.edit(embed=embed, view=self)
