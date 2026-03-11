@echo off
echo Starting InLeader API on port 9000...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :9000') do taskkill /f /pid %%a >nul 2>&1
uvicorn api:app --host 127.0.0.1 --port 9000 --reload
pause
