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
import re

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

# Currency conversion rates (USD base)
CURRENCY_RATES = {
    'USD': {'symbol': '$', 'rate': 1.0, 'name': 'US Dollar'},
    'EUR': {'symbol': '€', 'rate': 0.92, 'name': 'Euro'},
    'GBP': {'symbol': '£', 'rate': 0.79, 'name': 'British Pound'},
    'CAD': {'symbol': 'C$', 'rate': 1.36, 'name': 'Canadian Dollar'},
    'AUD': {'symbol': 'A$', 'rate': 1.53, 'name': 'Australian Dollar'},
    'JPY': {'symbol': '¥', 'rate': 149.50, 'name': 'Japanese Yen'},
    'INR': {'symbol': '₹', 'rate': 83.12, 'name': 'Indian Rupee'},
    'BRL': {'symbol': 'R$', 'rate': 4.97, 'name': 'Brazilian Real'},
    'MXN': {'symbol': 'MX$', 'rate': 17.08, 'name': 'Mexican Peso'},
    'PHP': {'symbol': '₱', 'rate': 55.50, 'name': 'Philippine Peso'},
}

# Map Discord locales to currencies
LOCALE_TO_CURRENCY = {
    'en-US': 'USD', 'en-GB': 'GBP', 'en-AU': 'AUD', 'en-CA': 'CAD',
    'es-ES': 'EUR', 'fr': 'EUR', 'de': 'EUR', 'it': 'EUR', 'nl': 'EUR',
    'pt-BR': 'BRL', 'ja': 'JPY', 'ko': 'USD', 'zh-CN': 'USD',
    'zh-TW': 'USD', 'ru': 'USD', 'pl': 'EUR', 'tr': 'USD',
    'hi': 'INR', 'th': 'USD', 'sv-SE': 'EUR', 'no': 'EUR',
    'da': 'EUR', 'fi': 'EUR', 'cs': 'EUR', 'ro': 'EUR',
    'es-MX': 'MXN', 'fil': 'PHP',
}

def convert_price(price_str, target_currency='USD'):
    """Convert price string to target currency"""
    if not price_str or price_str in ['Free', 'Paid Game', 'Full Game Access']:
        return price_str
    
    # Extract number from price string
    match = re.search(r'[\d.]+', price_str)
    if not match:
        return price_str
    
    try:
        usd_amount = float(match.group())
        currency_info = CURRENCY_RATES.get(target_currency, CURRENCY_RATES['USD'])
        converted = usd_amount * currency_info['rate']
        
        # Format based on currency
        if target_currency == 'JPY':
            return f"{currency_info['symbol']}{int(converted)}"
        else:
            return f"{currency_info['symbol']}{converted:.2f}"
    except:
        return price_str

def get_user_currency(interaction: discord.Interaction = None):
    """Detect user's currency from their Discord locale"""
    if interaction and hasattr(interaction, 'locale'):
        locale = str(interaction.locale)
        return LOCALE_TO_CURRENCY.get(locale, 'USD')
    return 'USD'

def create_embed(game, platform, currency='USD'):
    """Create a modern rich embed for game announcement"""
    # Modern color scheme
    color_map = {
        'Epic Games': 0x2E3440,  # Dark modern gray
        'Steam': 0x1B2838,       # Steam's dark blue-gray
    }
    color = color_map.get(platform, 0x2E3440)
    
    # Create embed with modern styling
    embed = discord.Embed(
        title="",  # Empty title for cleaner look
        description="",  # Will add content below
        color=color,
        timestamp=datetime.now()
    )
    
    # Add game title as author for modern look
    embed.set_author(
        name=f"🎮 {game['title']}",
        icon_url="https://cdn.discordapp.com/emojis/1234567890.png" if platform == 'Epic Games' else None
    )
    
    # Main description with platform badge
    platform_emoji = "🏪" if platform == "Epic Games" else "⚙️"
    status_badge = "```ansi\n\u001b[0;32m● FREE NOW\u001b[0m\n```"
    
    embed.description = f"{platform_emoji} **{platform}**\n{status_badge}"
    
    # Add description in a modern card style
    if game.get('description'):
        desc_text = game['description'][:180] + "..." if len(game['description']) > 180 else game['description']
        embed.add_field(
            name="📝 About",
            value=f">>> {desc_text}",
            inline=False
        )
    
    # Price and availability in a compact row
    info_row = []
    
    if game.get('original_price'):
        converted_price = convert_price(game['original_price'], currency)
        currency_name = CURRENCY_RATES.get(currency, {}).get('name', currency)
        info_row.append(f"💰 ~~{converted_price}~~ **FREE**")
    
    if game.get('end_date'):
        info_row.append(f"⏰ Until **{game['end_date']}**")
    
    if info_row:
        embed.add_field(
            name="💎 Deal Information",
            value="\n".join(info_row),
            inline=False
        )
    
    # Modern CTA button style
    embed.add_field(
        name="",
        value=f"### [🎁 Claim Now →]({game['url']})\n*Click above to get this game for free!*",
        inline=False
    )
    
    # Set thumbnail/image
    if game.get('image'):
        embed.set_image(url=game['image'])
    
    # Modern footer
    platform_icon = "🎮" if platform == "Epic Games" else "⚙️"
    embed.set_footer(
        text=f"{platform_icon} Free Games Notifier • Powered by {platform}",
        icon_url=None
    )
    
    return embed

def create_modern_help_embed(currency='USD'):
    """Create modern help embed"""
    embed = discord.Embed(
        title="",
        description="",
        color=0x5865F2,  # Discord blurple
        timestamp=datetime.now()
    )
    
    embed.set_author(
        name="🎮 Free Games Bot",
        icon_url=None
    )
    
    embed.description = """
    ```ansi
\u001b[0;36m● ACTIVE\u001b[0m Your automated free games notifier
    ```
    
    I automatically scan **Epic Games** and **Steam** for free games and notify you instantly!
    
    🌍 Prices shown in **{currency}** based on your location
    """.format(currency=CURRENCY_RATES.get(currency, {}).get('name', currency))
    
    # Commands section
    embed.add_field(
        name="⚡ Quick Commands",
        value=(
            "```\n"
            "/commands     • View all commands\n"
            "/epicgames    • Check Epic store\n"
            "/steamgames   • Check Steam store\n"
            "```"
        ),
        inline=False
    )
    
    # Text commands
    embed.add_field(
        name="💬 Text Commands",
        value=(
            "> `!epicgames` • `!steamgames`\n"
            "> `!checkgames` (Admin)\n"
            "> `!cleardb` (Admin)"
        ),
        inline=False
    )
    
    # Features
    embed.add_field(
        name="✨ Features",
        value=(
            "```yaml\n"
            "Scan Interval: Every 1 hour\n"
            "Platforms: Epic Games + Steam\n"
            "Smart Detection: No duplicates\n"
            "Auto Currency: Based on locale\n"
            "```"
        ),
        inline=False
    )
    
    embed.set_footer(
        text="🎮 Free Games Notifier • Always Free",
        icon_url=None
    )
    
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
        title="",
        description="",
        color=0x5865F2,
        timestamp=datetime.now()
    )
    
    welcome_embed.set_author(name="🎮 Welcome to Free Games Bot!")
    
    welcome_embed.description = """
    ```ansi
\u001b[0;32m✓ Successfully Added\u001b[0m
    ```
    
    Thanks for adding me! I'll automatically notify you when new free games drop on **Epic Games** and **Steam**.
    """
    
    welcome_embed.add_field(
        name="⚡ Quick Start",
        value=(
            "```yaml\n"
            f"Auto-Check: Every {CHECK_INTERVAL} hour(s)\n"
            "Platforms: Epic Games + Steam\n"
            "Commands: Use /commands\n"
            "```"
        ),
        inline=False
    )
    
    welcome_embed.add_field(
        name="🎯 What's Next?",
        value=(
            "> Use `/commands` to see all available commands\n"
            "> Use `/epicgames` or `/steamgames` anytime\n"
            "> I'll post in this channel when new games are free!"
        ),
        inline=False
    )
    
    welcome_embed.set_footer(text="🎮 Free Games Notifier • Let's find some free games!")
    
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
            header_embed = discord.Embed(
                description="```ansi\n\u001b[0;34m🏪 EPIC GAMES STORE\u001b[0m\n```",
                color=0x2E3440
            )
            await target_channel.send(embed=header_embed)
            
            for game in epic_games:
                embed = create_embed(game, 'Epic Games', 'USD')
                await target_channel.send(embed=embed)
                await asyncio.sleep(0.5)
            print(f"  ✓ Sent {len(epic_games)} Epic game(s)")
        
        # Steam Games
        steam_games = get_steam_free_games()
        if steam_games:
            header_embed = discord.Embed(
                description="```ansi\n\u001b[0;36m⚙️ STEAM STORE\u001b[0m\n```",
                color=0x1B2838
            )
            await target_channel.send(embed=header_embed)
            
            for game in steam_games:
                embed = create_embed(game, 'Steam', 'USD')
                await target_channel.send(embed=embed)
                await asyncio.sleep(0.5)
            print(f"  ✓ Sent {len(steam_games)} Steam game(s)")
        
        if not epic_games and not steam_games:
            no_games_embed = discord.Embed(
                description="```ansi\n\u001b[0;33m⏳ No free games right now\u001b[0m\n```\nBut I'll notify you the moment something drops!",
                color=0xFEE75C
            )
            await target_channel.send(embed=no_games_embed)
            
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
    embed = create_modern_help_embed('USD')
    await ctx.send(embed=embed)

# Slash Commands
##############################
# Helpers & Error Handling
##############################

async def _send_embed_list(interaction: discord.Interaction, games, platform: str):
    """Send a list of game embeds for a platform, chunking to avoid rate limits."""
    if not games:
        embed = discord.Embed(
            description=f"```ansi\n\u001b[0;33m⚠ No free games available\u001b[0m\n```\nNo free games currently on {platform}, but I'm checking every hour!",
            color=0xFEE75C
        )
        await interaction.followup.send(embed=embed)
        return
    
    # Detect user currency
    currency = get_user_currency(interaction)
    
    # Discord rate limiting: send sequentially
    for game in games:
        embed = create_embed(game, platform, currency)
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
    currency = get_user_currency(interaction)
    embed = create_modern_help_embed(currency)
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
