$ErrorActionPreference = "Stop"
Set-Location "D:\Projects\Game bot\discord-free-games-bot"

# Using Start-Process with -WindowStyle Hidden ensures Python stays silent
Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "bot.py" -WindowStyle Hidden