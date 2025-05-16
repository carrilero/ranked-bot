print("Iniciando bot...")

import discord
print("discord importado")

from discord.ext import commands
print("commands importado")

from match_queue import add_player, remove_player, get_queue, get_next_match
print("funciones de queue importadas")

from dotenv import load_dotenv
print("dotenv importado")

import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
print(f"TOKEN: {TOKEN}")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command()
async def ranked(ctx):
    add_player(ctx.author.name)
    await ctx.send(f"{ctx.author.name} se ha unido a la cola.")
    
    if len(get_queue()) >= 4:
        match = get_next_match()
        await ctx.send(f"🎮 Nueva partida: {', '.join(match)}")

@bot.command()
async def leave(ctx):
    remove_player(ctx.author.name)
    await ctx.send(f"{ctx.author.name} ha salido de la cola.")

@bot.command()
async def queue(ctx):
    current_queue = get_queue()
    if current_queue:
        await ctx.send("Jugadores en cola: " + ", ".join(current_queue))
    else:
        await ctx.send("La cola está vacía.")
try:
    print ("token: ",TOKEN)
    bot.run(TOKEN)
except Exception as e:
    print(f"Error al iniciar el bot: {e}")