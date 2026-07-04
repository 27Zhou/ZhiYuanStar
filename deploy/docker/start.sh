#!/bin/bash
# =====================================================
# 智选未来 - Docker 启动脚本
# =====================================================

echo "=================================="
echo "  智选未来 - Docker 启动"
echo "=================================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误: 未安装Docker"
    echo "请先安装Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# 检查Docker Compose是否可用
if ! command -v docker-compose &> /dev/null; then
    echo "错误: 未安装Docker Compose"
    exit 1
fi

# 进入Docker目录
cd "$(dirname "$0")"

# 启动服务
echo "正在启动服务..."
docker-compose up -d

# 等待服务就绪
echo "等待服务就绪..."
sleep 10

# 检查服务状态
echo ""
echo "服务状态:"
docker-compose ps

echo ""
echo "=================================="
echo "  启动完成!"
echo "  后端API: http://localhost:8080/api"
echo "  Swagger: http://localhost:8080/api/swagger-ui.html"
echo "=================================="
echo ""
echo "常用命令:"
echo "  查看日志: docker-compose logs -f backend"
echo "  停止服务: docker-compose down"
echo "  重启服务: docker-compose restart"
