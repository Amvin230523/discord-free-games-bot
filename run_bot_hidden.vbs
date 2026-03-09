Set WshShell = CreateObject("WScript.Shell")
' Use Chr(34) to represent double quotes cleanly
WshShell.Run "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File " & Chr(34) & "D:\Projects\Game bot\discord-free-games-bot\start_bot.ps1" & Chr(34), 0, False