# Update Instructions (Local Project)

This project is configured for local use.

## Recommended Update Flow

1. Open a terminal in the repository folder.
2. Pull the latest code:

```bash
git pull origin main
```

3. Activate your virtual environment.
4. Reinstall dependencies (safe even if unchanged):

```bash
pip install -r requirements.txt
```

5. Restart the bot process:

```bash
python bot.py
```

## After Updating

- Confirm the bot logs in successfully.
- Confirm slash command sync appears in logs.
- Test `/commands`, `/epicgames`, and `/steamgames`.

## If Something Breaks

- Check terminal output for stack traces.
- Verify `.env` contains a valid `DISCORD_TOKEN`.
- Verify `config.json` still points to the correct channel.
- Recreate the environment if needed:

```bash
python -m venv .venv
# activate .venv
pip install -r requirements.txt
```
