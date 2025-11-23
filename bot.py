import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from epic_games import get_epic_free_games
from steam_games import get_steam_free_games
from keep_alive import keep_alive
import asyncio
import traceback

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

CHANNEL_ID = config['channel_id']
CHECK_INTERVAL = config['check_interval_hours']
PING_ROLE_ID = config.get('ping_role_id', None)

# Database file to track announced games
DB_FILE = 'announced_games.json'

def load_database():
    """Load the database of already announced games"""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {'epic': [], 'steam': []}

def save_database(db):
    """Save the database of announced games"""
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=2)

def create_embed(game, platform):
    """Create a rich embed for game announcement"""
    color = 0x0078F2 if platform == 'Epic Games' else 0x171A21  # Epic blue or Steam dark
    
    embed = discord.Embed(
        title=f"🎉 Free Game Alert!",
        description=f"**{game['title']}** is now FREE on {platform}!",
        color=color,
        timestamp=datetime.now()
    )
    
    if game.get('description'):
        embed.add_field(name="About", value=game['description'][:200] + "..." if len(game['description']) > 200 else game['description'], inline=False)
    
    if game.get('end_date'):
        embed.add_field(name="⏰ Available Until", value=game['end_date'], inline=True)
    
    if game.get('original_price'):
        embed.add_field(name="💰 Original Price", value=game['original_price'], inline=True)
    
    embed.add_field(name="🔗 Get It Now", value=f"[Click here]({game['url']})", inline=False)
    
    if game.get('image'):
        embed.set_image(url=game['image'])
    
    embed.set_footer(text=f"{platform} Free Game Notifier")
    
    return embed

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} server(s)')
    
    # Sync slash commands with Discord
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} slash command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')
    
    if not check_free_games.is_running():
        check_free_games.start()
        print(f'Started checking for free games every {CHECK_INTERVAL} hour(s)')

    # Extra debug: list registered app commands
    for cmd in bot.tree.get_commands():
        print(f"Registered slash command: /{cmd.name} - {cmd.description}")

@bot.event
async def on_guild_join(guild):
    """When bot joins a new server, send current free games to the first available channel"""
    print(f"Bot joined new server: {guild.name} (ID: {guild.id})")
    
    # Find a channel where we can send messages
    target_channel = None
    
    # Try to find system channel first
    if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
        target_channel = guild.system_channel
    else:
        # Find first text channel where bot can send messages
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                target_channel = channel
                break
    
    if not target_channel:
        print(f"  ✗ Could not find a channel to send welcome message in {guild.name}")
        return
    
    # Send welcome message
    welcome_embed = discord.Embed(
        title="🎮 Thanks for adding Free Games Bot!",
        description="I'll automatically notify you when new free games are available on Epic Games and Steam!",
        color=0x00FF00,
        timestamp=datetime.now()
    )
    
    welcome_embed.add_field(
        name="⚙️ Getting Started",
        value=(
            f"I check for free games every **{CHECK_INTERVAL} hour(s)**.\n"
            "Use `/commands` to see all available commands!\n"
            "Or use `!help_freegames` for detailed help."
        ),
        inline=False
    )
    
    welcome_embed.add_field(
        name="📢 Set Up Notifications",
        value=(
            "Want notifications in a specific channel?\n"
            "Edit `config.json` and set your preferred channel ID."
        ),
        inline=False
    )
    
    welcome_embed.set_footer(text="Free Games Notifier")
    
    try:
        await target_channel.send(embed=welcome_embed)
        print(f"  ✓ Sent welcome message to #{target_channel.name}")
    except Exception as e:
        print(f"  ✗ Failed to send welcome message: {e}")
    
    # Fetch and send current free games
    try:
        print(f"  Fetching current free games for {guild.name}...")
        
        # Epic Games
        epic_games = get_epic_free_games()
        if epic_games:
            await target_channel.send("🎮 **Current Epic Games Free Games:**")
            for game in epic_games:
                embed = create_embed(game, 'Epic Games')
                await target_channel.send(embed=embed)
                await asyncio.sleep(0.5)
            print(f"  ✓ Sent {len(epic_games)} Epic game(s)")
        
        # Steam Games
        steam_games = get_steam_free_games()
        if steam_games:
            await target_channel.send("🎮 **Current Steam Free Games:**")
            for game in steam_games:
                embed = create_embed(game, 'Steam')
                await target_channel.send(embed=embed)
                await asyncio.sleep(0.5)
            print(f"  ✓ Sent {len(steam_games)} Steam game(s)")
        
        if not epic_games and not steam_games:
            await target_channel.send("Currently no free games available, but I'll notify you when new ones appear! 👀")
            
    except Exception as e:
        print(f"  ✗ Error fetching/sending free games: {e}")
        await target_channel.send("⚠️ I had trouble fetching current free games, but I'll keep checking automatically!")

@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return
    
    # Debug: print all messages the bot sees
    print(f'[Message Received] {message.author}: {message.content}')
    
    # Process commands
    await bot.process_commands(message)

@tasks.loop(hours=CHECK_INTERVAL)
async def check_free_games():
    """Check for free games periodically"""
    print(f"[{datetime.now()}] Checking for free games...")
    
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"Error: Could not find channel with ID {CHANNEL_ID}")
        return
    
    db = load_database()
    new_games_found = False
    
    # Check Epic Games
    try:
        epic_games = get_epic_free_games()
        for game in epic_games:
            game_id = game['id']
            if game_id not in db['epic']:
                # New free game found!
                embed = create_embed(game, 'Epic Games')
                
                # Prepare message with optional role ping
                message_content = ""
                if PING_ROLE_ID:
                    message_content = f"<@&{PING_ROLE_ID}>"
                
                await channel.send(content=message_content, embed=embed)
                db['epic'].append(game_id)
                new_games_found = True
                print(f"  ✓ Announced Epic game: {game['title']}")
    except Exception as e:
        print(f"  ✗ Error checking Epic Games: {e}")
    
    # Check Steam
    try:
        steam_games = get_steam_free_games()
        for game in steam_games:
            game_id = game['id']
            if game_id not in db['steam']:
                # New free game found!
                embed = create_embed(game, 'Steam')
                
                # Prepare message with optional role ping
                message_content = ""
                if PING_ROLE_ID:
                    message_content = f"<@&{PING_ROLE_ID}>"
                
                await channel.send(content=message_content, embed=embed)
                db['steam'].append(game_id)
                new_games_found = True
                print(f"  ✓ Announced Steam game: {game['title']}")
    except Exception as e:
        print(f"  ✗ Error checking Steam: {e}")
    
    if new_games_found:
        save_database(db)
        print(f"  Database updated!")
    else:
        print(f"  No new free games found.")

@bot.command(name='checkgames')
@commands.has_permissions(administrator=True)
async def manual_check(ctx):
    """Manually trigger a check for free games (Admin only)"""
    await ctx.send("🔍 Checking for free games...")
    await check_free_games()

@bot.command(name='epicgames')
async def show_epic(ctx):
    """Show current Epic Games free games"""
    try:
        games = get_epic_free_games()
        if not games:
            await ctx.send("No free games currently available on Epic Games Store.")
            return
        
        for game in games:
            embed = create_embed(game, 'Epic Games')
            await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error fetching Epic Games: {e}")

@bot.command(name='steamgames')
async def show_steam(ctx):
    """Show current Steam free games"""
    try:
        games = get_steam_free_games()
        if not games:
            await ctx.send("No free games currently available on Steam.")
            return
        
        for game in games:
            embed = create_embed(game, 'Steam')
            await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Error fetching Steam games: {e}")

@bot.command(name='cleardb')
@commands.has_permissions(administrator=True)
async def clear_database(ctx):
    """Clear the database of announced games (Admin only)"""
    db = {'epic': [], 'steam': []}
    save_database(db)
    await ctx.send("✅ Database cleared! All games will be announced again on next check.")

@bot.command(name='help_freegames')
async def help_command(ctx):
    """Show help information"""
    embed = discord.Embed(
        title="🎮 Free Games Bot - Help",
        description="I automatically check for free games on Epic Games Store and Steam!",
        color=0x00FF00
    )
    
    embed.add_field(
        name="📋 Commands",
        value=(
            "`!epicgames` - Show current Epic free games\n"
            "`!steamgames` - Show current Steam free games\n"
            "`!checkgames` - Manually check now (Admin)\n"
            "`!cleardb` - Reset announcement history (Admin)\n"
            "`!help_freegames` - Show this help message\n"
            "`/commands` - Show all commands (slash command)"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⚙️ How it works",
        value=f"I check for new free games every {CHECK_INTERVAL} hour(s) and announce them automatically!",
        inline=False
    )
    
    await ctx.send(embed=embed)

# Slash Commands
##############################
# Helpers & Error Handling
##############################

async def _send_embed_list(interaction: discord.Interaction, games, platform: str):
    """Send a list of game embeds for a platform, chunking to avoid rate limits."""
    if not games:
        await interaction.followup.send(f"No free games currently available on {platform}.")
        return
    # Discord rate limiting: send sequentially
    for game in games:
        embed = create_embed(game, platform)
        await interaction.followup.send(embed=embed)
        await asyncio.sleep(0.3)  # small delay to be gentle

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: Exception):
    """Global error handler for app (slash) commands."""
    print("[Slash Command Error]", repr(error))
    traceback.print_exception(type(error), error, error.__traceback__)
    try:
        if interaction.response.is_done():
            await interaction.followup.send("⚠️ An error occurred while processing that command.", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ An error occurred while processing that command.", ephemeral=True)
    except Exception as send_err:
        print("[Error sending error message]", send_err)
@bot.tree.command(name="commands", description="Show all available bot commands")
async def slash_commands(interaction: discord.Interaction):
    """Show all available commands using slash command"""
    embed = discord.Embed(
        title="🎮 Free Games Bot - Commands",
        description="Here are all the commands you can use!",
        color=0x00FF00,
        timestamp=datetime.now()
    )
    
    # User Commands
    embed.add_field(
        name="👥 Everyone Can Use",
        value=(
            "`!epicgames` - Show current Epic Games free games\n"
            "`!steamgames` - Show current Steam free games\n"
            "`!help_freegames` - Show detailed help\n"
            "`/commands` - Show this command list"
        ),
        inline=False
    )
    
    # Admin Commands
    embed.add_field(
        name="🛡️ Admin Only",
        value=(
            "`!checkgames` - Manually trigger free games check\n"
            "`!cleardb` - Clear announcement history (re-announce all games)"
        ),
        inline=False
    )
    
    # Bot Info
    embed.add_field(
        name="ℹ️ Bot Info",
        value=(
            f"🔄 Checks for games every **{CHECK_INTERVAL} hour(s)**\n"
            f"🎯 Announces only **new** free games\n"
            f"🎮 Supports **Epic Games** & **Steam**"
        ),
        inline=False
    )
    
    embed.set_footer(text="Free Games Notifier", icon_url=bot.user.avatar.url if bot.user.avatar else None)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="epicgames", description="Show current Epic Games free games")
async def slash_epic(interaction: discord.Interaction):
    """Show current Epic Games free games via slash command"""
    print("[/epicgames invoked]")
    try:
        await interaction.response.defer(thinking=True)
        # Timeout the fetch so we always answer
        try:
            games = await asyncio.wait_for(asyncio.to_thread(get_epic_free_games), timeout=12)
        except asyncio.TimeoutError:
            await interaction.followup.send("⏱️ Timed out fetching Epic Games data. Please try again in a moment.", ephemeral=True)
            return
        await _send_embed_list(interaction, games, 'Epic Games')
    except Exception as e:
        print(f"[/epicgames error] {e}")
        traceback.print_exception(type(e), e, e.__traceback__)
        if interaction.response.is_done():
            await interaction.followup.send("⚠️ Error fetching Epic Games.", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ Error fetching Epic Games.", ephemeral=True)

@bot.tree.command(name="steamgames", description="Show current Steam free games")
async def slash_steam(interaction: discord.Interaction):
    """Show current Steam free games via slash command"""
    print("[/steamgames invoked]")
    try:
        await interaction.response.defer(thinking=True)
        try:
            games = await asyncio.wait_for(asyncio.to_thread(get_steam_free_games), timeout=15)
        except asyncio.TimeoutError:
            await interaction.followup.send("⏱️ Timed out fetching Steam data. Please try again shortly.", ephemeral=True)
            return
        await _send_embed_list(interaction, games, 'Steam')
    except Exception as e:
        print(f"[/steamgames error] {e}")
        traceback.print_exception(type(e), e, e.__traceback__)
        if interaction.response.is_done():
            await interaction.followup.send("⚠️ Error fetching Steam games.", ephemeral=True)
        else:
            await interaction.response.send_message("⚠️ Error fetching Steam games.", ephemeral=True)

# Run the bot
if __name__ == "__main__":
    # Start web server to keep Replit alive
    keep_alive()
    
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env file!")
        exit(1)
    
    bot.run(TOKEN)
