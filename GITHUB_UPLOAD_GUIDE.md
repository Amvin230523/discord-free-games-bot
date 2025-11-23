# 📤 How to Upload Files to GitHub (Easy Method)

## Step 1: Create GitHub Repository (2 minutes)

1. **Go to GitHub**: https://github.com/new

2. **Fill in the form:**
   - Repository name: `discord-free-games-bot`
   - Description: `Discord bot that announces free games from Epic Games and Steam`
   - Select: **Public** ✅
   - DON'T check "Add a README file"
   - Click **"Create repository"**

3. **You'll see a page with instructions** - ignore those for now!

---

## Step 2: Prepare Files for Upload (1 minute)

### ✅ Files TO Upload:
Open File Explorer and go to: `C:\Users\Arvin\Downloads\DC bot`

Select these files (Ctrl+Click to select multiple):
- ✅ `bot.py`
- ✅ `epic_games.py`
- ✅ `steam_games.py`
- ✅ `keep_alive.py`
- ✅ `requirements.txt`
- ✅ `config.json`
- ✅ `.env.example`
- ✅ `.gitignore`
- ✅ `.replit`
- ✅ `README.md`
- ✅ `REPLIT_SETUP_GUIDE.md`
- ✅ `REPLIT_CHECKLIST.md`
- ✅ `USAGE_GUIDE.md`

### ❌ Files NOT to Upload:
- ❌ `.env` (contains your real token!)
- ❌ `.venv` folder (Python packages)
- ❌ `__pycache__` folder
- ❌ `announced_games.json` (not needed)

---

## Step 3: Upload to GitHub (3 minutes)

1. **On your GitHub repository page**, click **"uploading an existing file"**
   - It's a blue link in the middle of the page

2. **Drag and drop** all the ✅ files from Step 2
   - Or click "choose your files" and select them

3. **Wait for upload** (should be quick, they're small files)

4. **Add commit message** (or use the default)
   - Default: "Add files via upload"

5. **Click green "Commit changes" button**

6. ✅ **Done!** Your files are now on GitHub!

---

## Step 4: Verify Upload (1 minute)

Check your GitHub repository page - you should see all these files:
- bot.py
- epic_games.py
- steam_games.py
- keep_alive.py
- requirements.txt
- config.json
- .env.example
- .gitignore
- README.md
- And other guide files

**Important:** Make sure `.env` is NOT there! That would expose your token.

---

## Step 5: Get Your Repository URL

Copy your repository URL - it looks like:
```
https://github.com/YOUR_USERNAME/discord-free-games-bot
```

You'll need this for Replit!

---

## ⚠️ Security Check Before Uploading

**Did you:**
- [ ] Reset your Discord token? (if you haven't, do it now!)
- [ ] Verify `.env` is NOT in the files you're uploading?
- [ ] Check that `.env.example` has a fake token (not your real one)?

**If yes to all three ✅ - proceed with upload!**

---

## 🎯 After Upload - Go to Replit

Once files are uploaded:

1. Go to https://replit.com/
2. Sign up/Login
3. Click "Create Repl"
4. Select "Import from GitHub"
5. Paste your repository URL
6. Click "Import"
7. Add your token to Secrets (NOT to any file!)

---

## 🆘 Troubleshooting

**Q: I accidentally uploaded .env with my token!**
A: 
1. Delete the repository immediately
2. Reset your Discord token NOW
3. Start over with the new token

**Q: GitHub says "secret detected"**
A:
1. Cancel the upload
2. Make sure you're NOT uploading `.env`
3. Check `.env.example` has a fake token
4. Try again

**Q: Some files won't upload**
A:
- Make sure they're not too large
- Skip `.venv` and `__pycache__` folders
- You only need the Python files and configs

---

## ✅ Quick Checklist

- [ ] Created GitHub repository
- [ ] Selected only the safe files (no .env!)
- [ ] Uploaded files to GitHub
- [ ] Verified .env is NOT in the repository
- [ ] Copied repository URL
- [ ] Ready for Replit!

**Total time: ~5-10 minutes**

Next: Continue with Replit setup! 🚀
