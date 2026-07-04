@echo off
chcp 65001 >nul
title 智选未来 - 一键启动
echo.
echo ====================================================
echo   智选未来 - 高考志愿辅助填报系统
echo ====================================================
echo.

:: 设置Java环境
set JAVA_HOME=D:\jdk\jdk-24.0.2
set PATH=%JAVA_HOME%\bin;%PATH%

:: 检查Java
java -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Java，请检查JAVA_HOME配置
    pause
    exit /b 1
)
echo [√] Java环境正常

:: 检查MySQL
netstat -ano | findstr ":3306" >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] MySQL可能未启动，请确保MySQL服务已启动
) else (
    echo [√] MySQL服务正常
)

:: 杀掉旧的Java进程
echo.
echo [1/3] 清理旧进程...
taskkill /F /IM java.exe >nul 2>&1
timeout /t 2 /nobreak >nul
echo [√] 旧进程已清理

:: 编译项目
echo.
echo [2/3] 编译后端项目...
cd /d D:\Code\ZhiYuan-Star\backend
call D:\Code\apache-maven-3.9.9\bin\mvn clean compile -q
if %errorlevel% neq 0 (
    echo [错误] 编译失败，请检查代码
    pause
    exit /b 1
)
echo [√] 编译成功

:: 启动后端
echo.
echo [3/3] 启动后端服务...
echo.
echo ====================================================
echo   启动中，请等待...
echo   启动完成后访问:
echo   - 接口地址: http://localhost:8080/api
echo   - Swagger:  http://localhost:8080/api/swagger-ui.html
echo ====================================================
echo.

call D:\Code\apache-maven-3.9.9\bin\mvn spring-boot:run
