@echo off
echo ==============================
echo   RUN PROJECT
echo ==============================

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python n'est pas detecte.
    pause
    exit /b
)

echo Python OK

IF NOT EXIST main.py (
    echo [ERROR] main.py introuvable.
    pause
    exit /b
)

echo Lancement du projet...

python main.py

IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Probleme lors de l'execution
    pause
    exit /b
)

echo ==============================
echo   FIN EXECUTION
echo ==============================
pause