@echo off
cd /d "%~dp0"
:loop
echo Starting InLeader bot...
python bot.py
echo.
echo [WARNING] Bot stopped or crashed! Restarting in 5 seconds...
timeout /t 5 /nobreak >nul
goto loop
