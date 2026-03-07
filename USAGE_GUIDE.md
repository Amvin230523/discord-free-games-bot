# Bot Usage Guide (Local)

## Duplicate Prevention

### Scheduled checker

- The scheduled task prevents duplicate announcements.
- Announced game IDs are stored in `announced_games.json`.

### Manual commands

- Manual commands show current games and may repeat entries already announced before.
- This behavior is expected and useful for on-demand checks.

## Command Overview

- `!epicgames`: show current Epic deals
- `!steamgames`: show current Steam deals
- `!allgames`: show both stores
- `!checkgames` (admin): run scheduled check now
- `!cleardb` (admin): clear duplicate-tracking DB
- `!help_freegames`: help summary

Slash equivalents:

- `/commands`
- `/epicgames`
- `/steamgames`
- `/allgames`

## Local Runtime Options

### Foreground run

Use this for development:

```bash
python bot.py
```

### Auto-start on Windows

Use Task Scheduler to start the bot at login or boot.

Recommended action:

- Program: `python`
- Arguments: `bot.py`
- Start in: your repository folder

### Service-style run (optional)

Use a service wrapper such as NSSM/WinSW for auto-restart behavior.

## Practical Limits

- Steam parsing may require updates when Steam changes page structure.
- Continuous operation requires your machine to stay on and connected.
- If the bot is offline, no scheduled checks run.

## Troubleshooting

- Commands not detected: confirm Message Content Intent is enabled in the Discord Developer Portal.
- No announcements: verify `channel_id`, permissions, and console logs.
- Import errors: activate `.venv` and run `pip install -r requirements.txt`.

## Data File

`announced_games.json` format:

```json
{
  "epic": ["id_1", "id_2"],
  "steam": ["steam_123", "steam_456"]
}
```

If needed, reset with `!cleardb`.
