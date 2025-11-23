# 🔄 Update Instructions for Replit

## ✨ New Features Added:
- ✅ `/commands` - Slash command to see all commands
- ✅ `/epicgames` - Slash command for Epic games
- ✅ `/steamgames` - Slash command for Steam games
- ✅ Fixed datetime deprecation warning

---

## 📝 File Updated:
- **`bot.py`** - Main bot file

---

## 🔄 How to Update in Replit:

### Option 1: Pull from GitHub (Recommended)
1. Open your Repl in Replit
2. Click **"Shell"** tab (bottom of screen)
3. Run this command:
   ```bash
   git pull origin main
   ```
4. Stop the bot (if running)
5. Click **"Run"** to restart
6. You should see: `Synced 3 slash command(s)`

### Option 2: Manual Copy (If Git doesn't work)
1. Open `bot.py` in Replit
2. Delete ALL the content
3. Open `bot.py` on your PC: `C:\Users\Arvin\Downloads\DC bot\bot.py`
4. Copy everything (Ctrl+A, Ctrl+C)
5. Paste into Replit's `bot.py` (Ctrl+V)
6. Click **"Run"** to restart

---

## ✅ How to Test Slash Commands:

In your Discord server, type:
- `/commands` - Should show a nice embed with all commands
- `/epicgames` - Shows current Epic free games
- `/steamgames` - Shows current Steam free games

**Note:** Slash commands might take a few seconds to appear in Discord after the bot starts.

---

## 🎯 All Available Commands Now:

### Slash Commands (type `/` to see them):
- `/commands` - Show all commands
- `/epicgames` - Show Epic free games
- `/steamgames` - Show Steam free games

### Text Commands (type `!`):
- `!epicgames` - Show Epic free games
- `!steamgames` - Show Steam free games
- `!help_freegames` - Show help
- `!checkgames` - Manual check (Admin)
- `!cleardb` - Clear database (Admin)

---

## 🐛 Troubleshooting:

**Slash commands not showing?**
- Wait 1-2 minutes after bot starts
- Make sure bot has "applications.commands" permission
- Restart Discord client
- Check bot console shows: "Synced X slash command(s)"

**Bot won't start?**
- Check for syntax errors in bot.py
- Make sure you copied the entire file
- Check Replit console for errors

---

## ✨ What's New:

The bot now supports both:
- **Text commands** (`!epicgames`) - Traditional style
- **Slash commands** (`/epicgames`) - Modern Discord style

Users can use whichever they prefer! 🎮
