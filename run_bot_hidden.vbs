Set objShell = CreateObject("WScript.Shell")
command = "powershell.exe -NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File ""D:\Projects\Game bot\discord-free-games-bot\start_bot.ps1"""
objShell.Run command, 0, False
Set objShell = Nothing