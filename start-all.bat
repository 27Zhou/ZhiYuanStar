@echo off
setlocal enabledelayedexpansion

set JAVA_HOME=D:\jdk\jdk-24.0.2
set PATH=%JAVA_HOME%\bin;%PATH%
set MAVEN=D:\Code\apache-maven-3.9.9\bin\mvn
set PROJECT=D:\Code\ZhiYuan-Star

:MENU
cls
echo.
echo ====================================================
echo   ZhiYuan-Star - AI College Application System
echo ====================================================
echo.
echo   [1] One-Click Start
echo   [2] Start Backend Only
echo   [3] Start Docker Only
echo   [4] Import Data Only
echo   [5] Exit
echo.
set /p choice=Select:

if "%choice%"=="1" goto ONECLICK
if "%choice%"=="2" goto BACKEND
if "%choice%"=="3" goto DOCKER
if "%choice%"=="4" goto IMPORT
if "%choice%"=="5" goto EXIT
goto MENU

:ONECLICK
echo.
echo Starting Docker...
cd /d %PROJECT%\deploy\docker
docker-compose up -d
timeout /t 10 /nobreak >nul

echo Importing data...
cd /d %PROJECT%\spider
call venv\Scripts\activate.bat
python main.py school >nul 2>&1
python main.py major >nul 2>&1

echo Compiling...
taskkill /F /IM java.exe >nul 2>&1
timeout /t 3 /nobreak >nul
cd /d %PROJECT%\backend
call %MAVEN% clean compile -q

echo.
echo Starting backend...
echo API: http://localhost:8080/api
echo Swagger: http://localhost:8080/api/swagger-ui.html
echo.
call %MAVEN% spring-boot:run
goto END

:BACKEND
taskkill /F /IM java.exe >nul 2>&1
timeout /t 3 /nobreak >nul
cd /d %PROJECT%\backend
call %MAVEN% clean compile -q
call %MAVEN% spring-boot:run
goto END

:DOCKER
cd /d %PROJECT%\deploy\docker
docker-compose up -d
timeout /t 10 /nobreak >nul
docker-compose ps
pause
goto MENU

:IMPORT
cd /d %PROJECT%\spider
call venv\Scripts\activate.bat
python main.py school
python main.py major
pause
goto MENU

:EXIT
exit /b 0

:END
pause
