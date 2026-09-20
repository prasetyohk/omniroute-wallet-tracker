Set WshShell = CreateObject("WScript.Shell")
strCurrentDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Run pythonw launch_omniroute.py silently with zero console window
WshShell.CurrentDirectory = strCurrentDir
WshShell.Run "python.exe """ & strCurrentDir & "\launch_omniroute.py""", 0, False
