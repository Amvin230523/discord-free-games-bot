import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from epic_games import get_epic_free_games
from steam_games import get_steam_free_games
from keep_alive import keep_alive

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
        timestamp=datetime.utcnow()
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
    if not check_free_games.is_running():
        check_free_games.start()
        print(f'Started checking for free games every {CHECK_INTERVAL} hour(s)')

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
            "`!help_freegames` - Show this help message"
        ),
        inline=False
    )
    
    embed.add_field(
        name="⚙️ How it works",
        value=f"I check for new free games every {CHECK_INTERVAL} hour(s) and announce them automatically!",
        inline=False
    )
    
    await ctx.send(embed=embed)

# Run the bot
if __name__ == "__main__":
    # Start web server to keep Replit alive
    keep_alive()
    
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("Error: DISCORD_TOKEN not found in .env file!")
        exit(1)
    
    bot.run(TOKEN)
