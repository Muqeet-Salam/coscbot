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
    print(f' Logged in as {bot.user.name}')
    try:
        synced = await bot.tree.sync()
        print(f" Synced {len(synced)} command(s) globally.")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")



@bot.command()
async def createteams(ctx, count: int):
    guild = ctx.guild

    # Restrict @everyone by default
    overwrites_everyone = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False)
    }

    # Organizer role (admin access)
    mod_role = discord.utils.get(guild.roles, name="Organizer")
    if not mod_role:
        await ctx.send("⚠️ Organizer role not found! Please create a role named 'Organizer'.")
        return

    # Shared category (must already exist)
    shared_category = discord.utils.get(guild.categories, name="teams")
    if not shared_category:
        await ctx.send("⚠️ Category 'teams' not found. Please create it first.")
        return

    for i in range(1, count + 1):
        team_name = f"team-{i}"
        text_channel_name = f"{team_name}-chat"
        voice_channel_name = f"{team_name}-voice"

        # Create or get role
        role = discord.utils.get(guild.roles, name=team_name)
        if not role:
            role = await guild.create_role(name=team_name)
            await ctx.send(f'✅ Created role: {team_name}')
        else:
            await ctx.send(f'⚠️ Role already exists: {team_name}')

        # Channel-specific permissions
        overwrites = overwrites_everyone.copy()
        overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)
        overwrites[mod_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)

        # Create text channel
        existing_text_channel = discord.utils.get(guild.text_channels, name=text_channel_name)
        if not existing_text_channel:
            await guild.create_text_channel(
                name=text_channel_name,
                category=shared_category,
                overwrites=overwrites
            )
            await ctx.send(f'💬 Created text channel: {text_channel_name}')
        else:
            await ctx.send(f'⚠️ Text channel already exists: {text_channel_name}')

        # Create voice channel
        existing_voice_channel = discord.utils.get(guild.voice_channels, name=voice_channel_name)
        if not existing_voice_channel:
            await guild.create_voice_channel(
                name=voice_channel_name,
                category=shared_category,
                overwrites=overwrites
            )
            await ctx.send(f'🔊 Created voice channel: {voice_channel_name}')
        else:
            await ctx.send(f'⚠️ Voice channel already exists: {voice_channel_name}')

    await ctx.send("✅ Done creating teams!")

@bot.command()
async def createteamrange(ctx, range_str: str):
    guild = ctx.guild

    # Parse the range string (e.g., "26-50")
    try:
        start_str, end_str = range_str.split('-')
        start = int(start_str)
        end = int(end_str)
        if start > end or start < 1:
            await ctx.send("⚠️ Invalid range. Make sure the start is less than or equal to the end and both are positive.")
            return
    except Exception:
        await ctx.send("⚠️ Please provide a valid range like `26-50`.")
        return

    # Get Organizer role
    mod_role = discord.utils.get(guild.roles, name="Organizer")
    if not mod_role:
        await ctx.send("⚠️ Organizer role not found! Please create a role named 'Organizer'.")
        return

    # Get category
    shared_category = discord.utils.get(guild.categories, name="teams9")
    if not shared_category:
        await ctx.send("⚠️ Category 'teams9' not found. Please create it first.")
        return

    # Overwrites: only Organizer can join
    overwrites = {
    guild.default_role: discord.PermissionOverwrite(
        view_channel=False,  # hides the channel entirely
        connect=False
    ),
    mod_role: discord.PermissionOverwrite(
        view_channel=True,
        connect=True
    ),
}

    # Loop and create voice channels only
    for i in range(start, end + 1):
        voice_channel_name = f"team-{i}-voice"

        existing_voice_channel = discord.utils.get(guild.voice_channels, name=voice_channel_name)
        if not existing_voice_channel:
            await guild.create_voice_channel(
                name=voice_channel_name,
                category=shared_category,
                overwrites=overwrites
            )
            await ctx.send(f'🔊 Created voice channel: {voice_channel_name}')
        else:
            await ctx.send(f'⚠️ Voice channel already exists: {voice_channel_name}')

    await ctx.send(f"✅ Done creating voice channels from team-{start} to team-{end}!")


@bot.command()
async def addteam(ctx, team_number: int):
    guild = ctx.guild

    if team_number < 1:
        await ctx.send("⚠️ Invalid team number. Must be 1 or higher.")
        return

    team_name = f"team-{team_number}"
    text_channel_name = f"{team_name}-chat"
    voice_channel_name = f"{team_name}-voice"

    # Get roles and category
    mod_role = discord.utils.get(guild.roles, name="Organizer")
    if not mod_role:
        await ctx.send("⚠️ Organizer role not found! Please create a role named 'Organizer'.")
        return

    shared_category = discord.utils.get(guild.categories, name="teams9")
    if not shared_category:
        await ctx.send("⚠️ Category 'teams' not found. Please create it first.")
        return

    # Create or get team role
    role = discord.utils.get(guild.roles, name=team_name)
    if not role:
        role = await guild.create_role(name=team_name)
        await ctx.send(f'✅ Created role: {team_name}')
    else:
        await ctx.send(f'⚠️ Role already exists: {team_name}')

    # Set up permissions
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False),
        role: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True),
        mod_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True),
    }

    # Create text channel
    existing_text_channel = discord.utils.get(guild.text_channels, name=text_channel_name)
    if not existing_text_channel:
        await guild.create_text_channel(
            name=text_channel_name,
            category=shared_category,
            overwrites=overwrites
        )
        await ctx.send(f'💬 Created text channel: {text_channel_name}')
    else:
        await ctx.send(f'⚠️ Text channel already exists: {text_channel_name}')

    # Create voice channel
    existing_voice_channel = discord.utils.get(guild.voice_channels, name=voice_channel_name)
    if not existing_voice_channel:
        await guild.create_voice_channel(
            name=voice_channel_name,
            category=shared_category,
            overwrites=overwrites
        )
        await ctx.send(f'🔊 Created voice channel: {voice_channel_name}')
    else:
        await ctx.send(f'⚠️ Voice channel already exists: {voice_channel_name}')

    await ctx.send(f"✅ Team {team_number} setup complete!")

@bot.command()
async def deleteteams(ctx, count: int):
    guild = ctx.guild

    for i in range(1, count + 1):
        team_name = f"team-{i}"
        text_channel_name = f"{team_name}-chat"
        voice_channel_name = f"{team_name}-voice"

        # Delete text channel
        text_channel = discord.utils.get(guild.text_channels, name=text_channel_name)
        if text_channel:
            await text_channel.delete()
            await ctx.send(f'🗑️ Deleted text channel: {text_channel_name}')
        else:
            await ctx.send(f'⚠️ Text channel not found: {text_channel_name}')

        # Delete voice channel
        voice_channel = discord.utils.get(guild.voice_channels, name=voice_channel_name)
        if voice_channel:
            await voice_channel.delete()
            await ctx.send(f'🗑️ Deleted voice channel: {voice_channel_name}')
        else:
            await ctx.send(f'⚠️ Voice channel not found: {voice_channel_name}')

        # Delete category (cleanup from older versions)
        category = discord.utils.get(guild.categories, name=team_name)
        if category:
            await category.delete()
            await ctx.send(f'🗑️ Deleted category: {team_name}')
        else:
            await ctx.send(f'⚠️ Category not found: {team_name}')

        # Delete role
        role = discord.utils.get(guild.roles, name=team_name)
        if role:
            await role.delete()
            await ctx.send(f'🗑️ Deleted role: {team_name}')
        else:
            await ctx.send(f'⚠️ Role not found: {team_name}')

    await ctx.send("✅ Done deleting teams!")
@bot.command()
async def deletevoicerange(ctx, range_str: str):
    guild = ctx.guild

    # Parse the range string (e.g., "5-20")
    try:
        start_str, end_str = range_str.split('-')
        start = int(start_str)
        end = int(end_str)
        if start > end or start < 1:
            await ctx.send("⚠️ Invalid range. Make sure the start is less than or equal to the end and both are positive.")
            return
    except Exception:
        await ctx.send("⚠️ Please provide a valid range like `5-20`.")
        return

    # Loop through range and delete only voice channels
    for i in range(start, end + 1):
        voice_channel_name = f"team-{i}-voice"
        voice_channel = discord.utils.get(guild.voice_channels, name=voice_channel_name)
        if voice_channel:
            await voice_channel.delete()
            await ctx.send(f'🗑️ Deleted voice channel: {voice_channel_name}')
        else:
            await ctx.send(f'⚠️ Voice channel not found: {voice_channel_name}')

    await ctx.send(f"✅ Finished deleting voice channels from team-{start} to team-{end}.")


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

@bot.tree.command(name="grantvoice", description="Grants you access to your team's voice channel (without roles).")
@app_commands.describe(
    team_number="The team number (e.g., 3 for team-3-voice)"
)
async def grantvoice(interaction: discord.Interaction, team_number: int):
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

@bot.tree.command(name="ungrantvoice", description="Revokes your access to your team's voice channel.")
@app_commands.describe(
    team_number="The team number (e.g., 3 for team-3-voice)"
)
async def ungrantvoice(interaction: discord.Interaction, team_number: int):
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


# Replace this with your real bot token
bot.run('')
