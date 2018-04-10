@echo off

cacls.exe "%SystemDrive%\System Volume Information" >nul 2>nul

if %errorlevel%==0 goto Admin

:Admin


cmd /c netsh interface set interface "本地连接" disable
cmd /c netsh interface set interface "本地连接" enabled
