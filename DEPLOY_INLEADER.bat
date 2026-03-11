@echo off
chcp 65001 >nul
:: Папка скрипта = Project\InLeader
cd /d "%~dp0"
:: Путь к исходникам (КУХНЯ)
set "SRC_PATH=%~dp0inleader-0f0db311"
:: Путь к сайту (ТАРЕЛКА)
set "DEST_PATH=%USERPROFILE%\in-leader-site"

echo [1/3] Переходим в папку проекта...
cd /d "%SRC_PATH%"
if errorlevel 1 (
    echo ОШИБКА: не найден путь %SRC_PATH%
    pause
    exit /b 1
)

echo [2/3] Собираем новый билд (npm run build)...
call npm run build
if errorlevel 1 (
    echo ОШИБКА БИЛДА! Остановка.
    pause
    exit /b 1
)

echo [3/3] Очищаем старый сайт и копируем новый...
:: Удаляем только содержимое папки сайта, чтобы Caddy не ругался
powershell -Command "if (Test-Path '%DEST_PATH%') { Remove-Item -Path '%DEST_PATH%\*' -Recurse -Force }"
if not exist "%DEST_PATH%" mkdir "%DEST_PATH%"
:: Копируем свежий дистрибутив
xcopy "dist\*" "%DEST_PATH%\" /E /I /H /Y

echo.
echo ✅ ГОТОВО! Проверь сайт в режиме Инкогнито (Ctrl+Shift+N).
pause
