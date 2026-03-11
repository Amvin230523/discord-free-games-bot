$ErrorActionPreference = "Stop"
Set-Location "D:\Projects\Game bot\discord-free-games-bot"

# Log file path
$log = Join-Path (Get-Location) "bot.log"

# Write a startup timestamp
"$((Get-Date).ToString('u')) - Starting bot" | Out-File -FilePath $log -Encoding utf8 -Append

# Prefer pythonw.exe (no console). If not available, fall back to python.exe with redirection.
$pythonw = Join-Path (Get-Location) ".\.venv\Scripts\pythonw.exe"
$python = Join-Path (Get-Location) ".\.venv\Scripts\python.exe"
if (Test-Path $pythonw) {
	Start-Process -FilePath $pythonw -ArgumentList "bot.py" -WindowStyle Hidden
} else {
	Start-Process -FilePath $python -ArgumentList "bot.py" -RedirectStandardOutput $log -RedirectStandardError $log -WindowStyle Hidden
}