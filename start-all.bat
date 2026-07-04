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
echo   [1] Start Backend Server
echo   [2] Import School Data
echo   [3] Import Major Data
echo   [4] Import All Data
echo   [5] Import Data + Start Backend
echo   [6] Exit
echo.
set /p choice=Select (1-6):

if "%choice%"=="1" goto START_BACKEND
if "%choice%"=="2" goto IMPORT_SCHOOL
if "%choice%"=="3" goto IMPORT_MAJOR
if "%choice%"=="4" goto IMPORT_ALL
if "%choice%"=="5" goto START_ALL
if "%choice%"=="6" goto EXIT
echo Invalid choice
timeout /t 2 /nobreak >nul
goto MENU

:KILL_JAVA
echo Killing old Java processes...
taskkill /F /IM java.exe >nul 2>&1
timeout /t 3 /nobreak >nul
:WAIT_PORT
netstat -ano | findstr ":8080.*LISTEN" >nul 2>&1
if %errorlevel%==0 (
    echo Waiting for port 8080...
    timeout /t 2 /nobreak >nul
    goto WAIT_PORT
)
echo Port 8080 is free.
goto :eof

:START_BACKEND
echo.
call :KILL_JAVA

echo.
echo Compiling project...
cd /d %PROJECT%\backend
call %MAVEN% clean compile -q
if %errorlevel% neq 0 (
    echo Compile failed!
    pause
    goto MENU
)
echo Compile success.

echo.
echo Starting backend...
echo.
echo ====================================================
echo   API:      http://localhost:8080/api
echo   Swagger:  http://localhost:8080/api/swagger-ui.html
echo   Press Ctrl+C to stop
echo ====================================================
echo.

call %MAVEN% spring-boot:run
goto END

:IMPORT_SCHOOL
echo.
echo Importing school data...
cd /d %PROJECT%\spider
call venv\Scripts\activate.bat
python main.py school
echo.
echo Done.
pause
goto MENU

:IMPORT_MAJOR
echo.
echo Importing major data...
cd /d %PROJECT%\spider
call venv\Scripts\activate.bat
python main.py major
echo.
echo Done.
pause
goto MENU

:IMPORT_ALL
echo.
echo Importing all data...
cd /d %PROJECT%\spider
call venv\Scripts\activate.bat
python main.py school
echo.
python main.py major
echo.
echo Done.
pause
goto MENU

:START_ALL
echo.
echo [Step 1/4] Import data...
cd /d %PROJECT%\spider
call venv\Scripts\activate.bat
python main.py school
python main.py major

echo.
call :KILL_JAVA

echo.
echo [Step 3/4] Compile project...
cd /d %PROJECT%\backend
call %MAVEN% clean compile -q
if %errorlevel% neq 0 (
    echo Compile failed!
    pause
    goto MENU
)
echo Compile success.

echo.
echo [Step 4/4] Starting backend...
echo.
echo ====================================================
echo   API:      http://localhost:8080/api
echo   Swagger:  http://localhost:8080/api/swagger-ui.html
echo   Press Ctrl+C to stop
echo ====================================================
echo.

call %MAVEN% spring-boot:run
goto END

:EXIT
exit /b 0

:END
pause
