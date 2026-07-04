# =====================================================
# Spring Boot 后端 Dockerfile
# =====================================================

# 构建阶段
FROM eclipse-temurin:24-jdk-alpine AS builder

WORKDIR /app

# 复制整个项目
COPY backend/ .

# 编译打包
RUN chmod +x mvnw && ./mvnw clean package -DskipTests -B -q

# =====================================================
# 运行阶段
# =====================================================
FROM eclipse-temurin:24-jre-alpine

WORKDIR /app

# 复制打包好的jar
COPY --from=builder /app/target/*.jar app.jar

# 暴露端口
EXPOSE 8080

# 启动命令
ENTRYPOINT ["java", "-jar", "app.jar"]
