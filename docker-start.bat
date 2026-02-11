@echo off
REM 🐳 Address Validation Service - Docker Quick Start

echo.
echo ========================================
echo  🚀 Address Validation Service
echo  🐳 Docker Quick Start
echo ========================================
echo.

REM Check if Docker is running
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running! Please start Docker Desktop first.
    pause
    exit /b 1
)

echo ✅ Docker is running!
echo.

:menu
echo Choose option:
echo 1) Start Service (Development)
echo 2) Start Service (Background)
echo 3) Stop Service
echo 4) View Logs
echo 5) Test API
echo 6) Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto dev
if "%choice%"=="2" goto prod
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto logs
if "%choice%"=="5" goto test
if "%choice%"=="6" goto exit
echo ❌ Invalid choice! Please try again.
goto menu

:dev
echo.
echo 🔧 Starting service (development mode)...
docker compose up --build
goto menu

:prod
echo.
echo 🚀 Starting service (background)...
docker compose up --build -d
echo ✅ Service started!
echo.
echo 🌍 API: http://localhost:8000
echo 📚 Docs: http://localhost:8000/docs
echo ❤️  Health: http://localhost:8000/health
goto menu

:stop
echo.
echo 🛑 Stopping service...
docker compose down
echo ✅ Service stopped!
goto menu

:logs
echo.
echo 📋 Showing logs...
echo 🔄 Press Ctrl+C to exit
echo.
docker compose logs -f
goto menu

:test
echo.
echo 🧪 Testing API...
echo.
echo Health Check:
curl -s http://localhost:8000/health | head -c 200
echo.
echo.
echo Validation Test:
curl -X POST http://localhost:8000/validate ^
  -H "Content-Type: application/json" ^
  -d "{\"cnpj\": \"00924432000199\", \"cep\": \"13288390\"}" ^
  2>nul | head -c 300
echo.
echo.
pause
goto menu

:exit
echo.
echo 👋 Goodbye!
echo.
pause