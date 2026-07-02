package com.gaokao.ai;

import lombok.extern.slf4j.Slf4j;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

/**
 * 智选未来 - 高考志愿辅助填报系统
 * 主启动类
 *
 * @author gaokao-ai
 * @since 1.0.0
 */
@Slf4j
@SpringBootApplication
@MapperScan("com.gaokao.ai.mapper")
@EnableAsync
@EnableScheduling
public class GaokaoAiApplication {

    public static void main(String[] args) {
        SpringApplication.run(GaokaoAiApplication.class, args);
        log.info("""

            ====================================================
              智选未来 - 高考志愿辅助填报系统启动成功!
              接口地址: http://localhost:8080/api
              Swagger: http://localhost:8080/api/swagger-ui.html
            ====================================================
            """);
    }
}
