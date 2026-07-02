#!/bin/bash

# 智选未来 - 高考志愿辅助填报系统部署脚本

set -e

echo "========================================="
echo "  智选未来 - 高考志愿辅助填报系统部署"
echo "========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Docker是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}错误: 未安装Docker${NC}"
        exit 1
    fi
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}错误: 未安装Docker Compose${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker环境检查通过${NC}"
}

# 构建后端
build_backend() {
    echo -e "${YELLOW}正在构建后端...${NC}"
    cd ../backend
    mvn clean package -DskipTests
    cd ../deploy/docker
    echo -e "${GREEN}✓ 后端构建完成${NC}"
}

# 启动服务
start_services() {
    echo -e "${YELLOW}正在启动服务...${NC}"
    cd ../deploy/docker
    docker compose up -d
    echo -e "${GREEN}✓ 服务启动成功${NC}"
}

# 停止服务
stop_services() {
    echo -e "${YELLOW}正在停止服务...${NC}"
    cd ../deploy/docker
    docker compose down
    echo -e "${GREEN}✓ 服务已停止${NC}"
}

# 查看日志
view_logs() {
    cd ../deploy/docker
    docker compose logs -f
}

# 主菜单
main() {
    check_docker

    case "$1" in
        "build")
            build_backend
            ;;
        "start")
            start_services
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            stop_services
            start_services
            ;;
        "logs")
            view_logs
            ;;
        *)
            echo "使用方法: ./deploy.sh [命令]"
            echo ""
            echo "可用命令:"
            echo "  build   - 构建后端镜像"
            echo "  start   - 启动所有服务"
            echo "  stop    - 停止所有服务"
            echo "  restart - 重启所有服务"
            echo "  logs    - 查看服务日志"
            ;;
    esac
}

main "$@"
