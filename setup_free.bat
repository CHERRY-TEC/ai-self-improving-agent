@echo off
echo ============================================================
echo         AI SELF-IMPROVING AGENT - FREE SETUP
echo ============================================================
echo.
echo This script will set up Ollama (FREE) for you.
echo Ollama runs AI models locally on your computer.
echo.

REM Check if Ollama is installed
where ollama >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [!] Ollama is not installed.
    echo.
    echo Please install Ollama from: https://ollama.com/download
    echo.
    echo After installation, run this script again.
    echo.
    pause
    exit /b 1
)

echo [OK] Ollama is installed!
echo.

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [!] Ollama is not running.
    echo Starting Ollama...
    start /b ollama serve
    timeout /t 5 /nobreak >nul
)

echo [OK] Ollama is running!
echo.

REM Check if codellama model is available
echo Checking for codellama model...
ollama list | findstr "codellama" >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [!] codellama model not found.
    echo Downloading codellama (this may take a few minutes)...
    ollama pull codellama
)

echo.
echo ============================================================
echo         SETUP COMPLETE!
echo ============================================================
echo.
echo You can now run the agent with:
echo.
echo     python main.py --iterations 5
echo.
echo The agent will use Ollama (FREE) to improve its own code!
echo.
pause
