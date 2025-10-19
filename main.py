import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.guild_messages = True
intents.message_content = True
intents.members = True
from discord import app_commands
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} command(s) globally.")
    except Exception as e:
        print(f"❌ Failed to sync slash commands: {e}")



@bot.tree.command(name="claim", description="Grants you access to your team's voice channel (without roles).")
@app_commands.describe(
    team_number="The team number (e.g., 3 for team-3-voice)"
)
async def claim(interaction: discord.Interaction, team_number: int):
    guild = interaction.guild
    user = interaction.user

    if team_number < 1:
        await interaction.response.send_message("⚠️ Invalid team number. Must be 1 or higher.", ephemeral=True)
        return

    voice_channel_name = f"team-{team_number}-voice"
    voice_channel = discord.utils.get(guild.voice_channels, name=voice_channel_name)

    if not voice_channel:
        await interaction.response.send_message(f"❌ Voice channel `{voice_channel_name}` not found.", ephemeral=True)
        return

    try:
        await voice_channel.set_permissions(user, view_channel=True, connect=True)
        await interaction.response.send_message(f"✅ You've been granted access to `{voice_channel_name}`.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to modify that channel.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)

@bot.tree.command(name="unclaim", description="Revokes your access to your team's voice channel.")
@app_commands.describe(
    team_number="The team number (e.g., 3 for team-3-voice)"
)
async def unclaim(interaction: discord.Interaction, team_number: int):
    guild = interaction.guild
    user = interaction.user

    if team_number < 1:
        await interaction.response.send_message("⚠️ Invalid team number. Must be 1 or higher.", ephemeral=True)
        return

    voice_channel_name = f"team-{team_number}-voice"
    voice_channel = discord.utils.get(guild.voice_channels, name=voice_channel_name)

    if not voice_channel:
        await interaction.response.send_message(f"❌ Voice channel `{voice_channel_name}` not found.", ephemeral=True)
        return

    try:
        # Remove specific overwrite for this user
        await voice_channel.set_permissions(user, overwrite=None)
        await interaction.response.send_message(f"✅ Your access to `{voice_channel_name}` has been revoked.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to modify that channel.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ An error occurred: {e}", ephemeral=True)


bot.run(os.getenv('DISCORD_TOKEN'))
