# voting_system.py
import discord
from discord import ui
from config import MAPS
from utils import pick_random_host
import asyncio

class MapVotingView(ui.View):
    def __init__(self, channel, players, on_complete):
        """
        channel: discord.TextChannel donde publicar mensajes
        players: lista de IDs de usuario que deben votar
        on_complete: callback async(map_name, players) que lanza siguiente fase
        """
        super().__init__(timeout=60)  # 60 segundos
        self.channel = channel
        self.players = set(players)
        self.votes = {m: 0 for m in MAPS}
        self.voted = set()
        self.on_complete = on_complete

        # añade un botón por cada mapa
        for mapa in MAPS:
            self.add_item(MapVoteButton(label=mapa, parent=self))

    async def on_timeout(self):
        # Timeout: identifica quiénes no votaron
        non_voters = [self.channel.guild.get_member(uid).mention
                      for uid in self.players - self.voted]
        await self.channel.send(
            f"⏰ Tiempo agotado. Partida cancelada.\n"
            f"No votaron: {', '.join(non_voters)}"
        )
        # Aquí podrías limpiar estado o canales
        self.stop()

    async def vote(self, interaction: discord.Interaction, choice: str):
        user_id = interaction.user.id
        if user_id in self.voted:
            await interaction.response.send_message(
                "Ya has votado.", ephemeral=True
            )
            return
        if user_id not in self.players:
            await interaction.response.send_message(
                "No estás en esta votación.", ephemeral=True
            )
            return

        # registra el voto
        self.votes[choice] += 1
        self.voted.add(user_id)
        await interaction.response.send_message(
            f"Voto registrado por **{choice}**", ephemeral=True
        )

        # si todos han votado, forzamos el cierre anticipado
        if self.voted == self.players:
            self.stop()
            await self.finish()

    async def finish(self):
        # determina mapa ganador
        winner = max(self.votes.items(), key=lambda x: x[1])[0]
        await self.channel.send(f"🗺️ El mapa ganador es **{winner}**")

        # el Equipo 1 hostea
        await self.channel.send("👑 El **Equipo 1** hostea la partida.")

        # elige host aleatorio (opcional si quieres override)
        # host = pick_random_host(list(self.players))
        # await self.channel.send(f"👑 El jugador <@{host}> será host.")

        # lanza la siguiente fase de votación de resultado
        await start_result_voting(self.channel, self.players)

    @ui.button(label="Cancelar votación", style=discord.ButtonStyle.red, custom_id="cancel_map_vote")
    async def cancel_button(self, interaction: discord.Interaction, button: ui.Button):
        await self.channel.send("❌ Votación cancelada por decisión del bot.")
        # Aquí podrías limpiar estado o canales
        self.stop()


class MapVoteButton(ui.Button):
    def __init__(self, label, parent: MapVotingView):
        super().__init__(label=label, style=discord.ButtonStyle.primary, custom_id=f"map_{label}")
        self.parent = parent

    async def callback(self, interaction: discord.Interaction):
        await self.parent.vote(interaction, self.label)


async def start_map_voting(channel: discord.TextChannel, players: list[int]):
    """
    Inicia la votación de mapas.
    """
    await channel.send("🗳️ Empieza la votación de mapas. Tienes 1 minuto para votar.")
    view = MapVotingView(channel, players, on_complete=None)
    await channel.send(view=view)


async def start_result_voting(channel: discord.TextChannel, players: list[int]):
    """
    Lanza la votación para elegir equipo ganador.
    """
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
            # Si expira el tiempo
            await self.finish()

        async def finish(self):
            winner = max(self.votes, key=self.votes.get)
            await channel.send(f"🏆 La partida ha terminado. Ha ganado **{winner}**.")
            # Aquí registra en BD si quieres usando utils.get_db_connection()

    await channel.send("🗳️ Votación final: ¿Qué equipo ha ganado?", view=ResultView())
