@echo off

cacls.exe "%SystemDrive%\System Volume Information" >nul 2>nul

if %errorlevel%==0 goto Admin

:Admin


cmd /c netsh interface set interface "��������" disable
cmd /c netsh interface set interface "��������" enabled
