package com.gaokao.ai.controller;

import com.gaokao.ai.common.Result;
import com.gaokao.ai.service.AiConfigService;
import com.gaokao.ai.service.AiRecommendService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

/**
 * AI控制器
 * 提供AI推荐和聊天接口
 */
@Slf4j
@RestController
@RequestMapping("/ai")
@RequiredArgsConstructor
@Tag(name = "AI智能推荐", description = "AI大模型推荐和聊天接口")
public class AiController {

    private final AiRecommendService aiRecommendService;
    private final AiConfigService aiConfigService;

    /**
     * AI智能推荐院校
     */
    @GetMapping("/recommend")
    @Operation(summary = "AI智能推荐", description = "调用大模型进行个性化院校推荐（张雪峰风格）")
    public Result<Map<String, Object>> aiRecommend(
            @Parameter(description = "高考分数", required = true)
            @RequestParam int score,

            @Parameter(description = "省排名/位次")
            @RequestParam(required = false) Integer ranking,

            @Parameter(description = "省份ID", required = true)
            @RequestParam int provinceId,

            @Parameter(description = "科类：1-文科，2-理科，3-综合改革", required = true)
            @RequestParam int subjectType,

            @Parameter(description = "兴趣/偏好（如：想学计算机、想留在北京）")
            @RequestParam(required = false) String interests
    ) {
        log.info("AI推荐请求: score={}, ranking={}, provinceId={}, subjectType={}", score, ranking, provinceId, subjectType);

        if (!aiConfigService.isConfigured()) {
            return Result.error(400, "AI服务未配置，请先在系统设置中配置AI API Key");
        }

        Map<String, Object> result = aiRecommendService.aiRecommend(score, ranking, provinceId, subjectType, interests);
        return Result.success(result);
    }

    /**
     * AI聊天
     */
    @PostMapping("/chat")
    @Operation(summary = "AI聊天", description = "与AI助手对话")
    public Result<Map<String, String>> chat(@RequestBody Map<String, String> request) {
        String message = request.get("message");
        if (message == null || message.isEmpty()) {
            return Result.error(400, "消息不能为空");
        }

        log.info("AI聊天请求: {}", message);

        if (!aiConfigService.isConfigured()) {
            return Result.error(400, "AI服务未配置，请先在系统设置中配置AI API Key");
        }

        String reply = aiRecommendService.chat(message);

        Map<String, String> result = new HashMap<>();
        result.put("message", reply);
        return Result.success(result);
    }

    /**
     * 获取AI配置
     */
    @GetMapping("/config")
    @Operation(summary = "获取AI配置", description = "获取当前AI配置（隐藏API Key）")
    public Result<Map<String, Object>> getConfig() {
        Map<String, Object> config = new HashMap<>();
        config.put("apiUrl", aiConfigService.getApiUrl());
        config.put("model", aiConfigService.getModel());
        config.put("configured", aiConfigService.isConfigured());

        // 隐藏API Key，只显示前8位和后4位
        String apiKey = aiConfigService.getApiKey();
        if (apiKey != null && apiKey.length() > 12) {
            config.put("apiKeyPreview", apiKey.substring(0, 8) + "****" + apiKey.substring(apiKey.length() - 4));
        } else {
            config.put("apiKeyPreview", "未配置");
        }

        return Result.success(config);
    }

    /**
     * 更新AI配置
     */
    @PostMapping("/config")
    @Operation(summary = "更新AI配置", description = "设置AI API地址、Key、模型等")
    public Result<String> updateConfig(@RequestBody Map<String, String> request) {
        String apiUrl = request.get("apiUrl");
        String apiKey = request.get("apiKey");
        String model = request.get("model");
        String systemPrompt = request.get("systemPrompt");

        if (apiUrl == null || apiUrl.isEmpty()) {
            return Result.error(400, "API地址不能为空");
        }
        if (apiKey == null || apiKey.isEmpty()) {
            return Result.error(400, "API Key不能为空");
        }

        aiConfigService.updateConfig(apiUrl, apiKey, model, systemPrompt);
        return Result.success("AI配置更新成功");
    }
}
