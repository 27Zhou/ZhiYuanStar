# ZhiYuanStar - 智选未来

> 基于人工智能的高考志愿辅助填报系统 - 本科毕业设计项目

## 项目简介

本系统是一个基于人工智能的高考志愿辅助填报系统，旨在为高考考生提供科学、智能的志愿填报建议。系统整合了历年录取数据、院校信息、专业信息等多维度数据，通过AI算法为考生提供个性化的志愿推荐方案。

## 技术架构

### 后端技术栈
- **框架**: Spring Boot 3.4.1
- **JDK**: Java 24
- **ORM**: MyBatis-Plus 3.5.7
- **数据库**: MySQL 8.0
- **缓存**: Redis 7
- **权限认证**: Sa-Token 1.39.0
- **工具库**: Hutool 5.8.32

### 前端技术栈
- **框架**: HarmonyOS NEXT
- **语言**: ArkTS
- **UI组件**: HarmonyOS UI组件库

### 爬虫技术栈
- **框架**: Scrapy 2.11
- **数据处理**: Pandas 2.1
- **数据库驱动**: PyMySQL 1.1

### 部署技术栈
- **容器化**: Docker
- **反向代理**: Nginx
- **编排**: Docker Compose

## 项目结构

```
ZhiYuanStar/
├── backend/                    # SpringBoot后端
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/gaokao/ai/
│   │   │   │   ├── common/        # 公共模块
│   │   │   │   ├── config/        # 配置类
│   │   │   │   ├── controller/    # 控制器层
│   │   │   │   ├── entity/        # 实体类
│   │   │   │   ├── exception/     # 异常处理
│   │   │   │   └── utils/         # 工具类
│   │   │   └── resources/
│   │   │       ├── application.yml
│   │   │       ├── application-dev.yml
│   │   │       ├── application-prod.yml
│   │   │       └── logback-spring.xml
│   │   └── test/                  # 单元测试
│   └── pom.xml
│
├── frontend/                   # HarmonyOS NEXT前端
│   ├── entry/
│   │   └── src/main/ets/
│   │       ├── pages/          # 页面
│   │       ├── components/     # 组件
│   │       ├── services/       # 服务
│   │       ├── models/         # 数据模型
│   │       └── utils/          # 工具类
│   ├── build-profile.json5
│   └── oh-package.json5
│
├── spider/                     # Python爬虫
│   ├── src/
│   │   ├── spiders/           # 爬虫实现
│   │   ├── pipelines/         # 数据管道
│   │   ├── items/             # 数据项
│   │   ├── middlewares/       # 中间件
│   │   └── utils/             # 工具类
│   ├── config/
│   │   └── settings.py        # Scrapy配置
│   ├── data/                  # 数据存储
│   └── requirements.txt
│
├── sql/                       # 数据库脚本
│   ├── init/                  # 初始化脚本
│   ├── migration/             # 迁移脚本
│   └── seed/                  # 种子数据
│
├── deploy/                    # 部署配置
│   ├── docker/
│   │   ├── Dockerfile-backend
│   │   └── docker-compose.yml
│   ├── nginx/
│   │   └── nginx.conf
│   └── scripts/
│       └── deploy.sh
│
└── docs/                      # 项目文档
    ├── api/                   # API文档
    ├── design/                # 设计文档
    ├── requirements/          # 需求文档
    └── meeting-notes/         # 会议记录
```

## 快速开始

### 环境要求

- JDK 24+
- Maven 3.9+
- Node.js 18+
- Docker & Docker Compose
- MySQL 8.0
- Redis 7

### 后端启动

```bash
# 1. 进入后端目录
cd backend

# 2. 修改数据库配置
# 编辑 src/main/resources/application-dev.yml

# 3. 构建项目
mvn clean package -DskipTests

# 4. 运行项目
java -jar target/gaokao-ai-backend-1.0.0.jar
```

### 前端开发

```bash
# 1. 进入前端目录
cd frontend

# 2. 使用DevEco Studio打开项目
# 3. 运行模拟器或真机调试
```

### 爬虫运行

```bash
# 1. 进入爬虫目录
cd spider

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行爬虫
scrapy crawl university
```

### Docker部署

```bash
# 1. 进入部署目录
cd deploy/scripts

# 2. 构建并启动服务
./deploy.sh build
./deploy.sh start

# 3. 查看日志
./deploy.sh logs
```

## 开发规范

### 代码规范

- 遵循阿里巴巴Java开发手册
- 使用Lombok简化代码
- 统一异常处理
- 统一返回格式

### Git规范

- 分支命名: `feature/xxx`, `bugfix/xxx`, `hotfix/xxx`
- 提交信息: `feat: xxx`, `fix: xxx`, `docs: xxx`

### 数据库规范

- 表名使用小写字母+下划线
- 字段名使用小写字母+下划线
- 必须包含主键、创建时间、更新时间
- 使用逻辑删除

## 功能模块

### 1. 用户模块
- 用户注册/登录
- 个人信息管理
- 成绩信息管理

### 2. 院校模块
- 院校信息查询
- 院校对比
- 院校收藏

### 3. 专业模块
- 专业信息查询
- 专业对比
- 专业收藏

### 4. 志愿模块
- 智能推荐
- 志愿方案管理
- 录取概率预测

### 5. AI助手
- 智能问答
- 个性化建议
- 政策解读

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件
