$desktopPath = [System.Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktopPath "OmniRoute App.lnk"

$workspaceDir = "d:\VIBECODES\RELAY LOOKUP"
$vbsPath = Join-Path $workspaceDir "OmniRoute_App.vbs"
$iconPath = Join-Path $workspaceDir "assets\app_icon.ico"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = "wscript.exe"
$Shortcut.Arguments = "`"$vbsPath`""
$Shortcut.WorkingDirectory = $workspaceDir
if (Test-Path $iconPath) {
    $Shortcut.IconLocation = "$iconPath,0"
}
$Shortcut.Description = "OmniRoute - Universal Cross-Chain Wallet Intelligence"
$Shortcut.Save()

Write-Host "[OK] Desktop shortcut created successfully at: $shortcutPath" -ForegroundColor Green
