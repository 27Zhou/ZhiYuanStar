@echo off
chcp 65001 >nul
echo ==================================
echo   智选未来 - 启动数据库服务
echo ==================================

:: 检查Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未安装Docker
    echo 请先安装Docker Desktop: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

:: 进入Docker目录
cd /d %~dp0

:: 启动MySQL和Redis
echo 正在启动 MySQL 和 Redis...
docker-compose up -d

:: 等待服务就绪
echo 等待服务就绪...
timeout /t 10 /nobreak >nul

:: 检查服务状态
echo.
echo 服务状态:
docker-compose ps

echo.
echo ==================================
echo   数据库服务已启动!
echo   MySQL: localhost:3306
echo   Redis: localhost:6379
echo ==================================
echo.
echo 下一步: 启动后端
echo   cd D:\Code\ZhiYuan-Star\backend
echo   set JAVA_HOME=D:\jdk\jdk-24.0.2
echo   D:\Code\apache-maven-3.9.9\bin\mvn spring-boot:run
echo.
echo 常用命令:
echo   查看日志: docker-compose logs -f
echo   停止服务: docker-compose down
echo   重启服务: docker-compose restart
echo.
pause
