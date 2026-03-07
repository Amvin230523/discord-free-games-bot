# Discord Free Games Bot

A Discord bot that checks and announces free games from Epic Games Store and Steam.

## Features

- Automatic scheduled checks for new free games
- Epic Games support (official promotions endpoint)
- Steam support (100% discount and temporary free promotions)
- Duplicate prevention using `announced_games.json`
- DLC/Add-on indicator in embeds when detected
- Rich Discord embeds
- Text commands and slash commands

## Local Setup

### Requirements

- Python 3.8+
- A Discord bot token
- A Discord channel ID for announcements

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create `.env` from `.env.example`:

```powershell
Copy-Item .env.example .env
```

Set your token in `.env`:

```env
DISCORD_TOKEN=your_discord_bot_token_here
```

Important token rules:

- No quotes around the token
- No extra spaces before/after `=`
- Keep only one `DISCORD_TOKEN=` line in `.env`
- If leaked, reset it immediately in Discord Developer Portal

### 4. Configure Discord bot application

1. Open Discord Developer Portal: `https://discord.com/developers/applications`
2. Select your application, then open the `Bot` tab
3. If needed, click `Reset Token` and copy the new token into `.env`
4. In `Privileged Gateway Intents`, enable:
  - `Message Content Intent` (required for `!` text commands)
5. Open `OAuth2` -> `URL Generator`
6. Select scopes:
  - `bot`
  - `applications.commands`
7. Select bot permissions:
  - `View Channels`
  - `Send Messages`
  - `Embed Links`
  - `Read Message History`
  - `Use Slash Commands` (or `Use Application Commands`)
8. Copy the generated invite URL and invite the bot to your server

### 5. Get the announcement channel ID

1. In Discord, go to `User Settings` -> `Advanced` -> enable `Developer Mode`
2. Right-click your target channel and click `Copy Channel ID`

### 6. Configure `config.json`

```json
{
  "channel_id": 123456789012345678,
  "check_interval_hours": 1
}
```

- `channel_id`: target Discord channel
- `check_interval_hours`: polling interval

### 7. Run the bot

```bash
python bot.py
```

Expected startup output includes:

- Bot connected to Discord
- Slash commands synced
- Background check loop started

### 8. Verify in Discord

- Check the bot is online in your server member list
- Run `/commands`
- Run `!epicgames`
- Confirm the bot can post embeds in your configured channel

## Full Startup Setup (Windows)

Use this section to make the bot launch automatically when you log in to Windows.

### Option A: Startup Folder (recommended, no admin required)

1. Create a launcher script in `C:\bot_start\start_discord_free_games_bot.cmd`:

```bat
@echo off
cd /d "D:\Projects\Game bot\discord-free-games-bot"
"D:\Projects\Game bot\discord-free-games-bot\.venv\Scripts\python.exe" "D:\Projects\Game bot\discord-free-games-bot\bot.py"
```

2. Copy launcher into your user Startup folder:

```powershell
$startup = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Startup"
Copy-Item "C:\bot_start\start_discord_free_games_bot.cmd" (Join-Path $startup "start_discord_free_games_bot.cmd") -Force
```

3. Verify file exists in Startup folder:

```powershell
$startup = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Startup"
Test-Path (Join-Path $startup "start_discord_free_games_bot.cmd")
```

4. Reboot or sign out/sign in and confirm bot comes online automatically.

### Option B: Task Scheduler (more control)

Use this if you want Task Scheduler retries/history. Requires permissions that may be blocked by your Windows policy.

1. Open Task Scheduler -> `Create Task`.
2. `General` tab:
  - Name: `DiscordFreeGamesBot`
  - Select `Run only when user is logged on`
3. `Triggers` tab:
  - New trigger: `At log on`
4. `Actions` tab:
  - Program/script: `powershell.exe`
  - Add arguments:
    - `-NoProfile -ExecutionPolicy Bypass -File "D:\Projects\Game bot\discord-free-games-bot\start_bot.ps1"`
5. Save task.

Command-line equivalent:

```powershell
schtasks /Create /TN "DiscordFreeGamesBot" /TR "C:\bot_start\start_discord_free_games_bot.cmd" /SC ONLOGON /F
```

If command returns `Access is denied`, use Option A.

### Disable Startup

To disable auto-start, remove launcher from Startup folder:

```powershell
$startup = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\Startup"
Remove-Item (Join-Path $startup "start_discord_free_games_bot.cmd") -Force
```

Or disable/delete Task Scheduler task:

```powershell
schtasks /Delete /TN "DiscordFreeGamesBot" /F
```

## Commands

### Text commands

- `!epicgames`
- `!steamgames`
- `!allgames`
- `!dlconly`
- `!help_freegames`
- `!checkgames` (admin)
- `!cleardb` (admin)

### Slash commands

- `/commands`
- `/epicgames`
- `/steamgames`
- `/allgames`
- `/dlconly`

## Run Locally 24/7

For true local operation, keep the process running on your machine.

Options:

- Windows Startup folder or Task Scheduler: start at login.
- NSSM or WinSW: run as a Windows service.
- Linux systemd service: run/restart automatically.
- macOS LaunchAgent: launch at login/startup.

Current local setup in this repo:

- Startup launcher: `C:\bot_start\start_discord_free_games_bot.cmd`
- Copied to user Startup folder: `C:\Users\Arvin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\start_discord_free_games_bot.cmd`

## Troubleshooting

- Bot does not connect: verify `DISCORD_TOKEN` in `.env`.
- No announcements: verify `channel_id` and bot channel permissions.
- Missing embeds/images: ensure `Embed Links` permission is enabled.
- Module errors: reactivate your virtual env and reinstall requirements.

## Notes

- Epic data source is generally stable.
- Steam scraping can break if Steam HTML changes.
- Duplicate prevention only applies to scheduled announcements.

## License

Free to use and modify.
