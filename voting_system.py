# voting_system.py
import discord
from discord import ui
from config import MAPS
from utils import pick_random_host
from voice_text_channels import delete_private_channels
import asyncio

async def cancel_match(channel: discord.TextChannel):
    """Elimina la categoría y todos los canales de la partida."""
    category = channel.category
    if category:
        for c in list(category.channels):
            try:
                await c.delete()
            except Exception as e:
                print(f"Error eliminando canal {c.name}: {e}")
        try:
            await category.delete()
        except Exception as e:
            print(f"Error eliminando categoría {category.name}: {e}")
    await channel.send("📛 La partida ha sido cancelada.")

class MapVotingView(ui.View):
    def __init__(self, channel, players: list[int], on_complete=None):
        super().__init__(timeout=60)
        self.channel = channel
        self.players = set(players)
        self.votes = {m: 0 for m in MAPS}
        self.voted = set()
        self.on_complete = on_complete

        for mapa in MAPS:
            self.add_item(MapVoteButton(label=mapa, parent=self))

    async def on_timeout(self):
        # Avisar quiénes no votaron
        non_voters = [
            self.channel.guild.get_member(uid).mention
            for uid in self.players - self.voted
        ]
        await self.channel.send(
            f"⏰ Tiempo agotado. Partida cancelada.\n"
            f"No votaron: {', '.join(non_voters)}"
        )
        await cancel_match(self.channel)
        # Llamar callback de cancelación si existe
        if self.on_complete:
            await self.on_complete(None, list(self.players), cancelled=True)
        self.stop()

    async def vote(self, interaction: discord.Interaction, choice: str):
        uid = interaction.user.id
        if uid not in self.players:
            await interaction.response.send_message("No estás en esta votación.", ephemeral=True)
            return
        if uid in self.voted:
            await interaction.response.send_message("Ya has votado.", ephemeral=True)
            return

        self.votes[choice] += 1
        self.voted.add(uid)
        await interaction.response.send_message(f"Voto registrado por **{choice}**", ephemeral=True)

        if self.voted == self.players:
            self.stop()
            await self.finish()

    async def finish(self):
        # Determinar ganador
        winner = max(self.votes.items(), key=lambda x: x[1])[0]
        await self.channel.send(f"🗺️ El mapa ganador es **{winner}**")
        await self.channel.send("👑 El **Equipo 1** hostea la partida.")

        # Callback de finalización
        if self.on_complete:
            await self.on_complete(winner, list(self.players), cancelled=False)

    @ui.button(label="Cancelar votación", style=discord.ButtonStyle.red, custom_id="cancel_map_vote")
    async def cancel_button(self, interaction: discord.Interaction, button: ui.Button):
        player_name = interaction.user.display_name
        await interaction.response.send_message(f"❌ Votación cancelada por **{player_name}**.")
        await cancel_match(self.channel)
        if self.on_complete:
            await self.on_complete(None, list(self.players), cancelled=True)
        self.stop()

class MapVoteButton(ui.Button):
    def __init__(self, label, parent: MapVotingView):
        super().__init__(label=label, style=discord.ButtonStyle.primary, custom_id=f"map_{label}")
        self.parent = parent

    async def callback(self, interaction: discord.Interaction):
        await self.parent.vote(interaction, self.label)

async def start_map_voting(
    channel: discord.TextChannel,
    players: list[int],
    on_complete=None
):
    """
    lanza la votación de mapas; on_complete será llamado como:
      on_complete(winner_map: str|None, players: list[int], cancelled: bool)
    """
    await channel.send("🗳️ Empieza la votación de mapas. Tienes 1 minuto para votar.")
    view = MapVotingView(channel, players, on_complete=on_complete)
    await channel.send(view=view)

async def start_result_voting(channel: discord.TextChannel, players: list[int]):
    """Votación final: qué equipo ganó."""
    class ResultView(ui.View):
        def __init__(self):
            super().__init__(timeout=1800)
            self.votes = {"Equipo 1": 0, "Equipo 2": 0}
            self.voted = set()

        @ui.button(label="Ganó Equipo 1", style=discord.ButtonStyle.green)
        async def team1(self, interaction: discord.Interaction, button: ui.Button):
            await self.register(interaction, "Equipo 1")

        @ui.button(label="Ganó Equipo 2", style=discord.ButtonStyle.blurple)
        async def team2(self, interaction: discord.Interaction, button: ui.Button):
            await self.register(interaction, "Equipo 2")

        async def register(self, interaction, choice):
            uid = interaction.user.id
            if uid not in players:
                await interaction.response.send_message("No participaste en esta partida.", ephemeral=True)
                return
            if uid in self.voted:
                await interaction.response.send_message("Ya has votado.", ephemeral=True)
                return

            self.votes[choice] += 1
            self.voted.add(uid)
            await interaction.response.send_message(f"Voto registrado: {choice}", ephemeral=True)

            if self.voted == set(players):
                self.stop()
                await self.finish()

        async def on_timeout(self):
            self.stop()
            await self.finish()

        async def finish(self):
            winner = max(self.votes, key=self.votes.get)
            await channel.send(f"🏆 La partida ha terminado. Ha ganado **{winner}**.")

    await channel.send("🗳️ Votación final: ¿Qué equipo ha ganado?", view=ResultView())
