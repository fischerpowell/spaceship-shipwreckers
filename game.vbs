Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c .\game\start.bat"
oShell.Run strArgs, 0, false