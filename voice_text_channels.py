import discord
from config import CATEGORY_NAME

async def create_private_channels(guild, team1, team2):
    overwrites = {guild.default_role: discord.PermissionOverwrite(view_channel=False)}

    category = await guild.create_category(CATEGORY_NAME)

    text_channel = await guild.create_text_channel("partida-privada", category=category, overwrites=overwrites)
    voice1 = await guild.create_voice_channel("Equipo 1", category=category, overwrites=overwrites)
    voice2 = await guild.create_voice_channel("Equipo 2", category=category, overwrites=overwrites)

    for member_id in team1 + team2:
        member = guild.get_member(member_id)
        if member:
            for channel in [text_channel, voice1 if member_id in team1 else voice2]:
                await channel.set_permissions(member, view_channel=True, connect=True, send_messages=True)

    return text_channel, voice1, voice2
