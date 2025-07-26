# Enable Windows Long Path Support
# Run this script as Administrator

Write-Host "Enabling Windows Long Path Support..." -ForegroundColor Green

# Enable long paths in registry
try {
    reg add "HKLM\SYSTEM\CurrentControlSet\Control\FileSystem" /v "LongPathsEnabled" /t REG_DWORD /d 1 /f
    Write-Host "✓ Long path support enabled in registry" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to enable long path support. Make sure you're running as Administrator." -ForegroundColor Red
    exit 1
}

# Also enable for current user
try {
    reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v "LongPathsEnabled" /t REG_DWORD /d 1 /f
    Write-Host "✓ Long path support enabled for current user" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to enable long path support for current user." -ForegroundColor Red
}

Write-Host "`nLong path support has been enabled!" -ForegroundColor Green
Write-Host "You may need to restart your computer for changes to take effect." -ForegroundColor Yellow
Write-Host "After restart, try installing the packages again." -ForegroundColor Yellow

pause 