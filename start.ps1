# =====================================================
# 智选未来 - 一键启动脚本
# 用法: 右键 -> 使用 PowerShell 运行
# =====================================================

$ErrorActionPreference = "Stop"
$JAVA_HOME = "D:\jdk\jdk-24.0.2"
$MAVEN_HOME = "D:\Code\apache-maven-3.9.9"
$PROJECT_ROOT = "D:\Code\ZhiYuan-Star"

# 设置环境变量
$env:JAVA_HOME = $JAVA_HOME
$env:Path = "$JAVA_HOME\bin;$env:Path"

function Write-Header {
    Write-Host ""
    Write-Host "====================================================" -ForegroundColor Cyan
    Write-Host "  智选未来 - 高考志愿辅助填报系统" -ForegroundColor Green
    Write-Host "====================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step($step, $msg) {
    Write-Host "[$step] $msg" -ForegroundColor Yellow
}

function Write-OK($msg) {
    Write-Host "  [√] $msg" -ForegroundColor Green
}

function Write-Err($msg) {
    Write-Host "  [×] $msg" -ForegroundColor Red
}

function Test-Java {
    try {
        $ver = & java -version 2>&1 | Select-Object -First 1
        Write-OK "Java: $ver"
        return $true
    } catch {
        Write-Err "Java未找到"
        return $false
    }
}

function Test-MySQL {
    $listening = netstat -ano | Select-String ":3306.*LISTENING"
    if ($listening) {
        Write-OK "MySQL服务运行中"
        return $true
    } else {
        Write-Err "MySQL未运行 (端口3306)"
        return $false
    }
}

function Stop-OldProcess {
    Write-Step "1/3" "清理旧进程..."
    Get-Process java -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Write-OK "旧进程已清理"
}

function Start-Backend {
    Write-Step "2/3" "编译后端..."
    Set-Location "$PROJECT_ROOT\backend"

    $compileResult = & "$MAVEN_HOME\bin\mvn" clean compile -q 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Err "编译失败"
        Write-Host $compileResult -ForegroundColor Red
        return $false
    }
    Write-OK "编译成功"

    Write-Step "3/3" "启动后端服务..."
    Write-Host ""
    Write-Host "====================================================" -ForegroundColor Cyan
    Write-Host "  接口地址: http://localhost:8080/api" -ForegroundColor Green
    Write-Host "  Swagger:  http://localhost:8080/api/swagger-ui.html" -ForegroundColor Green
    Write-Host "  按 Ctrl+C 停止服务" -ForegroundColor Yellow
    Write-Host "====================================================" -ForegroundColor Cyan
    Write-Host ""

    & "$MAVEN_HOME\bin\mvn" spring-boot:run
}

function Import-Data {
    Write-Step "1/1" "导入数据..."
    Set-Location "$PROJECT_ROOT\spider"

    $activateScript = ".\venv\Scripts\Activate.ps1"
    if (Test-Path $activateScript) {
        & $activateScript
    }

    python main.py school
    Write-Host ""
    python main.py major
    Write-Host ""
    Write-OK "数据导入完成"
}

# 主程序
Write-Header

# 检查环境
Write-Host "环境检查:" -ForegroundColor White
$javaOK = Test-Java
$mysqlOK = Test-MySQL

if (-not $javaOK) {
    Write-Host "`n请安装Java 24或检查JAVA_HOME配置" -ForegroundColor Red
    Read-Host "按回车退出"
    exit 1
}

if (-not $mysqlOK) {
    Write-Host "`n请先启动MySQL服务" -ForegroundColor Red
    Read-Host "按回车退出"
    exit 1
}

# 功能菜单
Write-Host ""
Write-Host "请选择操作:" -ForegroundColor White
Write-Host "  [1] 一键启动后端 (默认)" -ForegroundColor Green
Write-Host "  [2] 导入数据到数据库" -ForegroundColor Green
Write-Host "  [3] 导入数据 + 启动后端" -ForegroundColor Green
Write-Host "  [4] 退出" -ForegroundColor Gray
Write-Host ""

$choice = Read-Host "请输入选项 (1-4)"
if ([string]::IsNullOrEmpty($choice)) { $choice = "1" }

switch ($choice) {
    "1" {
        Stop-OldProcess
        Start-Backend
    }
    "2" {
        Import-Data
    }
    "3" {
        Import-Data
        Write-Host ""
        Stop-OldProcess
        Start-Backend
    }
    "4" {
        exit 0
    }
    default {
        Write-Err "无效选项"
        exit 1
    }
}

Read-Host "按回车退出"
