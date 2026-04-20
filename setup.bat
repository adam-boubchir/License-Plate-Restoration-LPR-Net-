@echo off
echo ==============================
echo   CHECK PYTHON
echo ==============================

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python n'est pas installe ou pas dans le PATH.
    echo Installe Python depuis https://www.python.org/
    pause
    exit /b
)

echo Python OK :
python --version

echo ==============================
echo   CHECK PIP
echo ==============================

pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] pip n'est pas installe.
    pause
    exit /b
)

echo pip OK

echo ==============================
echo   INSTALL DEPENDENCIES
echo ==============================

pip install -r requirements.txt

IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Probleme lors de l'installation
    pause
    exit /b
)

echo ==============================
echo   DONE - ALL DEPENDENCIES INSTALLED
echo ==============================

pause