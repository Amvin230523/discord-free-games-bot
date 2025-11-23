# 🚀 How to Host Your Discord Bot on Replit (FREE 24/7)

## 📋 What You'll Need
1. GitHub account (free)
2. Replit account (free)
3. UptimeRobot account (free - to keep bot alive)

---

## Step 1: Create GitHub Repository

### Option A: Using GitHub Desktop (Easiest)
1. Download GitHub Desktop: https://desktop.github.com/
2. Install and sign in with your GitHub account
3. Click **"Add"** → **"Add Existing Repository"**
4. Browse to: `C:\Users\Arvin\Downloads\DC bot`
5. Click **"Create Repository"**
6. Name it: `discord-free-games-bot`
7. Make it **Public**
8. Click **"Publish Repository"**

### Option B: Using Git Command Line
```powershell
cd "C:\Users\Arvin\Downloads\DC bot"
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/discord-free-games-bot.git
git push -u origin main
```

### Option C: Manual Upload (If you don't want Git)
1. Go to https://github.com/new
2. Create new repository: `discord-free-games-bot`
3. Make it **Public**
4. Click **"uploading an existing file"**
5. Drag and drop all files from `C:\Users\Arvin\Downloads\DC bot`
6. Commit

---

## Step 2: Set Up Replit

### 1. Create Replit Account
- Go to https://replit.com/
- Sign up (use GitHub for easy login)
- Free account is enough!

### 2. Import Your Project
1. Click **"+ Create Repl"** button
2. Select **"Import from GitHub"**
3. Paste your GitHub repo URL: `https://github.com/YOUR_USERNAME/discord-free-games-bot`
4. Click **"Import from GitHub"**
5. Wait for it to load

### 3. Configure Secrets (Environment Variables)
1. On the left sidebar, click **🔒 "Secrets"** (or Tools → Secrets)
2. Add a new secret:
   - **Key:** `DISCORD_TOKEN`
   - **Value:** `[YOUR_NEW_DISCORD_TOKEN_HERE]` (Get this from Discord Developer Portal after resetting your token)
3. Click **"Add Secret"**

### 4. Edit config.json
1. Open `config.json` in Replit
2. Make sure it has your correct channel ID:
```json
{
  "channel_id": YOUR_CHANNEL_ID_HERE,
  "check_interval_hours": 1,
  "ping_role_id": YOUR_ROLE_ID_HERE
}
```

### 5. Create .replit Configuration File
Click **"+ New file"** and create `.replit`:
```toml
run = "python bot.py"
language = "python3"

[nix]
channel = "stable-23_11"

[deployment]
run = ["sh", "-c", "python bot.py"]
```

### 6. Run the Bot
1. Click the big green **"Run"** button at the top
2. Wait for packages to install
3. You should see: `Game Catcher#0114 has connected to Discord!`
4. ✅ Bot is now running!

---

## Step 3: Keep It Alive 24/7 (Important!)

Replit free tier stops bots after inactivity. We'll use UptimeRobot to ping it every 5 minutes.

### Create a Web Server (So Replit Can Be Pinged)

Create a new file `keep_alive.py`:

```python
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
```

### Update bot.py to Use Keep Alive

Add this at the very top of `bot.py` (after the imports):
```python
from keep_alive import keep_alive
```

Add this right before `if __name__ == "__main__":` at the bottom:
```python
# Start web server to keep Replit alive
keep_alive()
```

### Update requirements.txt

Add Flask to `requirements.txt`:
```
discord.py>=2.3.0
requests>=2.31.0
beautifulsoup4>=4.12.0
python-dotenv>=1.0.0
flask>=3.0.0
```

### Click Run Again
- The bot should start a web server on port 8080
- Copy the Replit URL (looks like: `https://discord-free-games-bot.yourname.repl.co`)

---

## Step 4: Set Up UptimeRobot (Keep Bot Alive 24/7)

### 1. Create UptimeRobot Account
- Go to https://uptimerobot.com/
- Sign up for FREE account
- Verify your email

### 2. Create Monitor
1. Click **"+ Add New Monitor"**
2. Fill in:
   - **Monitor Type:** HTTP(s)
   - **Friendly Name:** Discord Free Games Bot
   - **URL:** `https://discord-free-games-bot.yourname.repl.co` (your Replit URL)
   - **Monitoring Interval:** 5 minutes
3. Click **"Create Monitor"**

### 3. Done!
✅ UptimeRobot will ping your Replit every 5 minutes
✅ This keeps the bot alive 24/7 for FREE!

---

## 🎉 Your Bot is Now Running 24/7!

### Verify It's Working:
1. Check Discord - bot should be online
2. Check Replit console - should show no errors
3. Check UptimeRobot - monitor should be "Up"

### Managing Your Bot:

**View Logs:**
- Check Replit console for real-time logs

**Restart Bot:**
- Click "Stop" then "Run" in Replit

**Update Code:**
- Edit files in Replit directly, or
- Push to GitHub and Replit will auto-update

**Stop Bot:**
- Click "Stop" in Replit
- Delete UptimeRobot monitor

---

## 🐛 Troubleshooting

### Bot keeps going offline
- Make sure UptimeRobot monitor is active
- Check Replit isn't showing errors
- Verify your keep_alive.py is working

### "Module not found" errors
- Click "Packages" in Replit
- Search and install missing packages
- Or update requirements.txt and run again

### Bot can't connect to Discord
- Check your DISCORD_TOKEN in Secrets
- Make sure it's the correct token
- Token might have expired - regenerate in Discord Developer Portal

### Replit is slow
- Free tier has limited resources
- Bot should still work fine
- Consider upgrading if needed (but not necessary)

---

## 💰 Cost Breakdown

| Service | Cost | What It Does |
|---------|------|--------------|
| Replit | **FREE** | Hosts the bot |
| UptimeRobot | **FREE** | Keeps bot alive |
| GitHub | **FREE** | Stores your code |
| **TOTAL** | **$0.00/month** | ✅ Completely FREE! |

---

## 📊 Comparison: PC vs Replit

| Feature | Your PC | Replit |
|---------|---------|--------|
| Cost | FREE | FREE |
| 24/7 | ❌ Only when PC on | ✅ Always on |
| Internet | Need stable connection | ✅ Reliable |
| Setup | Easy | Medium |
| Maintenance | Manual restarts | Auto-restarts |
| Power usage | Uses electricity | None |

---

## 🔄 Alternative: Railway.app (If Replit Doesn't Work)

### Quick Setup:
1. Go to https://railway.app/
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select your `discord-free-games-bot` repo
5. Add environment variable: `DISCORD_TOKEN` = your token
6. Click Deploy
7. ✅ Done! No pinger needed!

**Railway Advantages:**
- No need for UptimeRobot pinger
- Better performance
- True 24/7 uptime
- 500 hours/month free (plenty for one bot)

---

## ✅ Next Steps After Hosting

1. **Test the bot** - Send `!help_freegames` in Discord
2. **Wait for games** - Bot checks every hour automatically
3. **Monitor logs** - Check Replit console occasionally
4. **Share with friends** - Invite them to your Discord server!

## 🎮 Enjoy Your Free Game Notifications!

Your bot is now:
- ✅ Running 24/7 in the cloud
- ✅ Checking Epic Games every hour
- ✅ Checking Steam every hour
- ✅ Announcing new free games automatically
- ✅ Completely FREE!

Need help? Just ask! 🚀
