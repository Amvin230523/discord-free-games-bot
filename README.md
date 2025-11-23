# 🎮 Discord Free Games Bot

A Discord bot that automatically checks and announces free games from **Epic Games Store** and **Steam**! Get notifications when games become temporarily free, including Epic's weekly free games and Steam's limited-time 100% off promotions.

## ✨ Features

- 🔄 **Automatic Checking**: Scans for free games at regular intervals (default: every hour)
- 🎯 **Epic Games**: Tracks Epic's weekly free games with official API
- 🎮 **Steam**: Detects temporarily free games and free weekends
- 🔔 **Smart Notifications**: Only announces new games (no duplicates)
- 🎨 **Rich Embeds**: Beautiful game announcements with images and details
- 📌 **Role Pings**: Optional role mentions for notifications
- 🛠️ **Admin Commands**: Manual checks and database management
- 💾 **Database**: Tracks announced games to prevent re-posting

## 📸 Preview

The bot sends rich embeds with:
- Game title and platform
- Description
- Original price
- Availability end date
- Direct link to claim
- Game artwork

## 🚀 Setup Guide

### Prerequisites

1. **Python 3.8 or higher** installed
2. **Discord Bot Token** (see below)
3. **Discord Channel ID** where announcements will be sent

### Step 1: Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** and give it a name
3. Go to **"Bot"** section on the left
4. Click **"Add Bot"**
5. Under **"Token"**, click **"Reset Token"** and copy it (you'll need this!)
6. Enable these **Privileged Gateway Intents**:
   - ✅ Server Members Intent
   - ✅ Message Content Intent
7. Go to **"OAuth2" > "URL Generator"**
8. Select scopes:
   - ✅ `bot`
   - ✅ `applications.commands`
9. Select bot permissions:
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Messages/View Channels
   - ✅ Mention Everyone (if you want role pings)
10. Copy the generated URL and open it in your browser to invite the bot to your server

### Step 2: Get Discord Channel ID

1. Enable Developer Mode in Discord:
   - Settings > Advanced > Developer Mode (ON)
2. Right-click on the channel where you want announcements
3. Click **"Copy Channel ID"**

### Step 3: Install the Bot

1. **Download/Clone this project** to your computer

2. **Open PowerShell** in the bot folder:
   - Right-click in the folder > "Open PowerShell here"

3. **Create a virtual environment** (optional but recommended):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

4. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

### Step 4: Configure the Bot

1. **Create a `.env` file** (copy from `.env.example`):
   ```powershell
   Copy-Item .env.example .env
   ```

2. **Edit `.env`** file and add your bot token:
   ```
   DISCORD_TOKEN=your_actual_bot_token_here
   ```

3. **Edit `config.json`** file:
   ```json
   {
     "channel_id": 1234567890123456789,
     "check_interval_hours": 1,
     "ping_role_id": null
   }
   ```
   
   - `channel_id`: Your Discord channel ID (from Step 2)
   - `check_interval_hours`: How often to check for new games (default: 1 hour)
   - `ping_role_id`: (Optional) Role ID to ping when new games are found
     - To get role ID: Right-click role > Copy Role ID
     - Set to `null` if you don't want pings

### Step 5: Run the Bot

```powershell
python bot.py
```

You should see:
```
<YourBotName> has connected to Discord!
Bot is in X server(s)
Started checking for free games every 1 hour(s)
```

🎉 **Your bot is now running!**

## 📋 Bot Commands

| Command | Description | Permission |
|---------|-------------|------------|
| `!epicgames` | Show current Epic free games | Everyone |
| `!steamgames` | Show current Steam free games | Everyone |
| `!checkgames` | Manually trigger a check now | Admin |
| `!cleardb` | Reset announcement history | Admin |
| `!help_freegames` | Show help information | Everyone |

## 🌐 Free Hosting Options

You can run this bot **24/7 for FREE** on these platforms:

### Option 1: Replit (Easiest)

1. Go to [Replit](https://replit.com/)
2. Create new Repl > Import from GitHub
3. Add your GitHub repo URL
4. Set environment variables in Secrets tab:
   - `DISCORD_TOKEN` = your token
5. Edit `config.json` with your channel ID
6. Click Run!

**Keep it alive 24/7:**
- Use [UptimeRobot](https://uptimerobot.com/) to ping your Repl every 5 minutes

### Option 2: Railway.app

1. Sign up at [Railway.app](https://railway.app/)
2. New Project > Deploy from GitHub
3. Add environment variable: `DISCORD_TOKEN`
4. Deploy!

### Option 3: Render.com

1. Sign up at [Render.com](https://render.com/)
2. New Web Service > Connect GitHub repo
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python bot.py`
5. Add environment variable: `DISCORD_TOKEN`

### Option 4: Your Computer (Windows)

**Run automatically on startup:**

1. Create a batch file `start_bot.bat`:
   ```batch
   @echo off
   cd "C:\Users\Arvin\Downloads\DC bot"
   call venv\Scripts\activate.bat
   python bot.py
   pause
   ```

2. Press `Win + R`, type `shell:startup`, press Enter
3. Create a shortcut to `start_bot.bat` in the Startup folder
4. Bot will auto-start when Windows boots!

## 🔧 Troubleshooting

### Bot doesn't connect
- ✅ Check your `DISCORD_TOKEN` in `.env`
- ✅ Make sure token is valid (not expired)
- ✅ Bot must be invited to your server

### No announcements
- ✅ Check `channel_id` in `config.json` is correct
- ✅ Bot must have permissions to send messages in that channel
- ✅ Use `!checkgames` to manually trigger a check
- ✅ Check console for error messages

### Missing images in embeds
- ✅ Bot needs "Embed Links" permission

### Role pings not working
- ✅ Bot needs "Mention Everyone" permission
- ✅ Check `ping_role_id` in `config.json`

### Module not found errors
- ✅ Run `pip install -r requirements.txt` again
- ✅ Make sure you're in the correct folder

## 📊 How It Works

### Epic Games
- Uses Epic's official API endpoint
- Fetches current promotional offers
- Filters for games with 100% discount
- Extracts title, description, images, end dates

### Steam
- Scrapes Steam's search page for 100% off games
- Detects temporarily free promotions
- Identifies free weekend games
- Parses game details from store listings

### Database
- Stores announced game IDs in `announced_games.json`
- Prevents duplicate announcements
- Can be cleared with `!cleardb` command

## 🎯 Customization

### Change check frequency
Edit `config.json`:
```json
"check_interval_hours": 2  // Check every 2 hours instead of 1
```

### Modify embed colors
Edit `bot.py`, function `create_embed()`:
```python
color = 0x0078F2  # Epic blue
color = 0x171A21  # Steam dark
```

### Add more platforms
Create a new module like `steam_games.py`:
```python
def get_your_platform_free_games():
    # Your implementation
    return games_list
```

Then import and use it in `bot.py`.

## 📝 Notes

- **Epic Games**: Very reliable, uses official API
- **Steam**: Uses web scraping, may need updates if Steam changes their site
- **Rate Limits**: Current check interval (1 hour) is safe for both platforms
- **Accuracy**: Steam detection may have false positives - always verify manually

## 🤝 Contributing

Feel free to improve the bot:
- Add more game platforms (GOG, Itch.io, etc.)
- Improve Steam detection accuracy
- Add more commands
- Enhance embed designs

## 📄 License

This project is free to use and modify. No warranty provided.

## ⚠️ Legal

- Web scraping is done on public pages only
- Epic API is unofficial but publicly accessible
- Use responsibly and respect rate limits
- This bot is for personal/community use

## 🆘 Support

If you need help:
1. Check this README carefully
2. Look at error messages in the console
3. Verify all configuration files
4. Make sure Python and dependencies are installed

---

**Made with ❤️ for free games lovers!**

Enjoy your free games! 🎮
