# How to Upload This Project to GitHub

Use this guide to safely back up/share the local project code.

## 1. Create a Repository

1. Go to `https://github.com/new`.
2. Repository name: `discord-free-games-bot`.
3. Visibility: Public or Private.
4. Create the repository.

## 2. Verify Sensitive Files Are Ignored

Do not commit secrets:

- `.env`
- `.env.local`
- `announced_games.json`
- `.venv/`

`\.gitignore` already excludes these.

## 3. Push from Local Machine

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/discord-free-games-bot.git
git push -u origin main
```

If the repo already exists locally, skip `git init` and just commit/push.

## 4. Security Checklist

- Confirm `.env` is not tracked.
- Confirm no real token appears in any tracked file.
- If a token was leaked, reset it immediately in Discord Developer Portal.

## 5. Keep It Updated

```bash
git add .
git commit -m "Describe your change"
git push
```

This repository is local-first. GitHub is used as source control and backup.
