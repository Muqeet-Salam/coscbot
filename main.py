import discord
from discord.ext import commands

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



@bot.tree.command(name="claim", description="Claim your team role (e.g., team-3)")
@app_commands.describe(team_number="The team number you want to claim")
async def claim(interaction: discord.Interaction, team_number: int):
    guild = interaction.guild
    member = interaction.user
    team_name = f"team-{team_number}"

    if team_number < 1:
        await interaction.response.send_message("⚠️ Invalid team number. Must be 1 or higher.", ephemeral=True)
        return

    # Try to find the role
    role = discord.utils.get(guild.roles, name=team_name)
    if not role:
        await interaction.response.send_message(f"❌ Role `{team_name}` not found. Please check the number.", ephemeral=True)
        return

    # Check if user already has it
    if role in member.roles:
        await interaction.response.send_message(f"ℹ️ You already have the `{team_name}` role.", ephemeral=True)
        return

    # Assign role
    try:
        await member.add_roles(role, reason="Claimed via /claim command")
        await interaction.response.send_message(f"✅ You have been added to `{team_name}`!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to assign that role.", ephemeral=True)


@bot.tree.command(name="unclaim", description="Remove your team role (e.g., team-3)")
@app_commands.describe(team_number="The team number you want to unclaim")
async def unclaim(interaction: discord.Interaction, team_number: int):
    guild = interaction.guild
    member = interaction.user
    team_name = f"team-{team_number}"

    if team_number < 1:
        await interaction.response.send_message("⚠️ Invalid team number. Must be 1 or higher.", ephemeral=True)
        return

    # Try to find the role
    role = discord.utils.get(guild.roles, name=team_name)
    if not role:
        await interaction.response.send_message(f"❌ Role `{team_name}` not found.", ephemeral=True)
        return

    # Check if user actually has the role
    if role not in member.roles:
        await interaction.response.send_message(f"ℹ️ You don't have the `{team_name}` role.", ephemeral=True)
        return

    # Remove role
    try:
        await member.remove_roles(role, reason="Unclaimed via /unclaim command")
        await interaction.response.send_message(f"✅ You have been removed from `{team_name}`.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("❌ I don't have permission to remove that role.", ephemeral=True)
bot.run('')
