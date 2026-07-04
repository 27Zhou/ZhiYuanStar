package com.gaokao.ai.controller;

import com.gaokao.ai.common.Result;
import com.gaokao.ai.entity.History;
import com.gaokao.ai.service.HistoryService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 浏览记录控制器
 */
@Slf4j
@RestController
@RequestMapping("/history")
@RequiredArgsConstructor
@Tag(name = "浏览记录", description = "浏览历史接口")
public class HistoryController {

    private final HistoryService historyService;

    // 临时默认用户ID（未登录状态）
    private static final Long DEFAULT_USER_ID = 1L;

    @PostMapping("/add")
    @Operation(summary = "添加浏览记录")
    public Result<History> addHistory(
            @Parameter(description = "浏览类型：1-高校，2-专业，3-招生计划，4-AI对话") @RequestParam Integer targetType,
            @Parameter(description = "目标ID") @RequestParam(required = false) Long targetId,
            @Parameter(description = "内容摘要") @RequestParam(required = false) String content
    ) {
        History history = historyService.addHistory(DEFAULT_USER_ID, targetType, targetId, content);
        return Result.success(history);
    }

    @GetMapping("/list")
    @Operation(summary = "获取浏览记录")
    public Result<List<Map<String, Object>>> getHistory(
            @Parameter(description = "浏览类型") @RequestParam(required = false) Integer targetType,
            @Parameter(description = "数量限制") @RequestParam(defaultValue = "20") int limit
    ) {
        List<Map<String, Object>> history = historyService.getHistory(DEFAULT_USER_ID, targetType, limit);
        return Result.success(history);
    }

    @DeleteMapping("/clear")
    @Operation(summary = "清空浏览记录")
    public Result<String> clearHistory() {
        historyService.clearHistory(DEFAULT_USER_ID);
        return Result.success("浏览记录已清空");
    }
}
