package com.gaokao.ai.controller;

import com.gaokao.ai.common.Result;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * 健康检查控制器
 *
 * @author gaokao-ai
 * @since 1.0.0
 */
@Slf4j
@RestController
@Tag(name = "健康检查", description = "系统健康检查接口")
public class HealthController {

    /**
     * 健康检查
     */
    @GetMapping("/health")
    @Operation(summary = "健康检查", description = "检查系统是否正常运行")
    public Result<Map<String, Object>> health() {
        log.info("健康检查请求");
        Map<String, Object> data = new HashMap<>();
        data.put("status", "UP");
        data.put("timestamp", LocalDateTime.now());
        data.put("service", "智选未来 - 高考志愿辅助填报系统");
        data.put("version", "1.0.0");
        return Result.success(data);
    }
}
