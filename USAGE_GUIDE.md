# 🎮 Bot Usage Guide

## ✅ How Duplicate Prevention Works

### Automatic Checking (Every Hour)
- ✅ **PREVENTS DUPLICATES** - Only announces games that haven't been announced before
- Stores game IDs in `announced_games.json`
- This is the main feature that runs automatically

### Manual Commands
- ❌ **DOES NOT CHECK DUPLICATES** - Shows all current free games
- These commands are for users to manually check what's free RIGHT NOW
- They don't post announcements, just show current games

**Commands:**
- `!epicgames` - Shows all current Epic free games (no duplicate check)
- `!steamgames` - Shows all current Steam free games (no duplicate check)
- `!checkgames` - Triggers automatic check (DOES prevent duplicates)

## 🔄 How to Keep Bot Running 24/7

### Option 1: Keep Running on Your PC
**Pros:** Free, full control
**Cons:** Need to keep PC on, need to restart manually

**Steps:**
1. Keep the terminal window open
2. Don't close the terminal or stop the script
3. Bot stops when PC shuts down

### Option 2: Auto-Start on Windows Boot
**Pros:** Starts automatically when PC turns on
**Cons:** Still requires PC to be on

**I can help you set this up!** Just ask.

### Option 3: Free Cloud Hosting (RECOMMENDED)
**Pros:** True 24/7, no PC needed, runs even when you're offline
**Cons:** Slight learning curve

#### Replit (Easiest)
1. Sign up at https://replit.com/
2. Create new Repl → Import from GitHub
3. Upload your files or paste the code
4. Add Secret: `DISCORD_TOKEN` = your token
5. Edit `config.json` with your channel ID
6. Click Run!
7. Use UptimeRobot to keep it alive 24/7

#### Railway.app
1. Sign up at https://railway.app/
2. New Project → Deploy from GitHub
3. Add environment variable: `DISCORD_TOKEN`
4. Upload files
5. Auto-deploys and runs 24/7

#### Render.com
1. Sign up at https://render.com/
2. New Web Service
3. Upload files
4. Build: `pip install -r requirements.txt`
5. Start: `python bot.py`
6. Add env variable: `DISCORD_TOKEN`

## ⚙️ Bot Limitations

### Rate Limits
- **Epic Games:** Safe to check every hour (no official limit)
- **Steam:** Safe to check every hour (scraping limit)
- **Discord:** 50 messages/second (way more than needed)

### Technical Limits
- Must run continuously to work
- Steam scraping may break if site changes
- Internet connection required
- Steam detection may include free-to-play games

### Hosting Limits
| Platform | Free Tier Limit |
|----------|----------------|
| Replit | May sleep (use pinger) |
| Railway | 500 hours/month |
| Render | Cold starts possible |
| Your PC | 24/7 if PC is on |

## 🐛 Troubleshooting

### Bot shows duplicate games in manual commands
✅ **This is normal!** Manual commands (`!epicgames`, `!steamgames`) show all current games.
The automatic checker prevents duplicate announcements.

### Bot stopped working
- Check if script is still running
- Check internet connection
- Check Discord token is valid
- Restart the bot

### Bot can't see commands
- Enable Message Content Intent in Discord Developer Portal
- Give bot "Read Messages" permission in channel
- Restart the bot

### No games being announced
- Wait for new games (bot checks every hour)
- Use `!checkgames` to manually trigger
- Check console for errors

## 📊 Database Info

**File:** `announced_games.json`
**Purpose:** Tracks which games have been announced
**Format:**
```json
{
  "epic": ["game_id_1", "game_id_2"],
  "steam": ["steam_123", "steam_456"]
}
```

**Clear database:** Use `!cleardb` command (Admin only)
**Effect:** Bot will re-announce all current free games

## 🎯 Best Practices

1. **Let automatic checking work** - It prevents duplicates
2. **Use manual commands sparingly** - They're for quick checks
3. **Host on cloud** - For true 24/7 operation
4. **Check console logs** - See what bot is doing
5. **Don't clear database** - Unless you want to re-announce games

## 💡 Command Summary

| Command | Who Can Use | Duplicate Check | Purpose |
|---------|-------------|-----------------|---------|
| `!help_freegames` | Everyone | N/A | Show help |
| `!epicgames` | Everyone | ❌ No | Show current Epic games |
| `!steamgames` | Everyone | ❌ No | Show current Steam games |
| `!checkgames` | Admin | ✅ Yes | Trigger auto-check now |
| `!cleardb` | Admin | N/A | Reset database |

## 🚀 Next Steps

**Want to:**
- Set up auto-start on Windows? → Ask me!
- Host on Replit/Railway? → Ask me!
- Add more platforms? → Ask me!
- Customize the bot? → Ask me!
