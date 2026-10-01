@echo off
title TesteoLab - NAUTA
color 0A

rem %~dp0 = la carpeta donde vive este .bat.
rem Asi sigue funcionando aunque muevas el proyecto.
cd /d "%~dp0"

echo.
echo   TesteoLab / NAUTA
echo   -----------------------------------
echo   Dashboard : http://localhost:5000
echo   Apagar    : Ctrl+C o cerrar esta ventana
echo.

rem Abre el navegador 3 segundos despues, cuando Flask ya levanto.
start "" /B powershell -NoProfile -Command "Start-Sleep 3; Start-Process 'http://localhost:5000'"

python notion_api.py

echo.
echo   El servidor se detuvo.
pause
