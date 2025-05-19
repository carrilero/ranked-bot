import discord
from config import CATEGORY_NAME
import time


async def create_private_channels(guild, team1, team2):
    overwrites = {guild.default_role: discord.PermissionOverwrite(view_channel=False)}

    suffix = str(int(time.time()))[-4:]  # 4 dígitos únicos de la hora Unix
    category = await guild.create_category(f"{CATEGORY_NAME}-{suffix}")

    text_channel = await guild.create_text_channel(f"game-{suffix}", category=category, overwrites=overwrites)
    voice1 = await guild.create_voice_channel(f"team1-{suffix}", category=category, overwrites=overwrites)
    voice2 = await guild.create_voice_channel(f"team2-{suffix}", category=category, overwrites=overwrites)

    for member_id in team1 + team2:
        member = guild.get_member(member_id)
        if member:
            for channel in [text_channel, voice1 if member_id in team1 else voice2]:
                await channel.set_permissions(member, view_channel=True, connect=True, send_messages=True)

    return text_channel, voice1, voice2

async def delete_private_channels(text_channel: discord.TextChannel, voice_channels: list[discord.VoiceChannel]):
    try:
        await text_channel.delete()
        for vc in voice_channels:
            await vc.delete()
    except Exception as e:
        logging.error(f"[Voice/Text] Error borrando canales: {e}")