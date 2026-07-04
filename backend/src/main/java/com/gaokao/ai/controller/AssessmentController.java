package com.gaokao.ai.controller;

import com.gaokao.ai.common.Result;
import com.gaokao.ai.entity.AssessmentQuestion;
import com.gaokao.ai.entity.AssessmentResult;
import com.gaokao.ai.service.AssessmentService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 心理测评控制器
 * 12项能力图谱测评
 */
@Slf4j
@RestController
@RequestMapping("/assessment")
@RequiredArgsConstructor
@Tag(name = "心理测评", description = "12项能力图谱测评")
public class AssessmentController {

    private final AssessmentService assessmentService;

    /**
     * 获取测评题目
     */
    @GetMapping("/questions")
    @Operation(summary = "获取测评题目", description = "获取所有测评题目（共36题，每维度3题）")
    public Result<List<AssessmentQuestion>> getQuestions() {
        List<AssessmentQuestion> questions = assessmentService.getQuestions();
        return Result.success(questions);
    }

    /**
     * 提交测评答案
     */
    @PostMapping("/submit")
    @Operation(summary = "提交测评答案", description = "提交答案并生成能力图谱")
    public Result<AssessmentResult> submitAnswers(@RequestBody Map<Integer, String> answers) {
        if (answers == null || answers.isEmpty()) {
            return Result.error(400, "答案不能为空");
        }
        log.info("收到测评提交，共 {} 题", answers.size());
        AssessmentResult result = assessmentService.submitAnswers(answers);
        return Result.success(result);
    }

    /**
     * 获取测评结果
     */
    @GetMapping("/result/{resultId}")
    @Operation(summary = "获取测评结果", description = "根据ID获取测评结果详情")
    public Result<AssessmentResult> getResult(
            @Parameter(description = "结果ID") @PathVariable Long resultId
    ) {
        AssessmentResult result = assessmentService.getResult(resultId);
        if (result == null) {
            return Result.error(404, "测评结果不存在");
        }
        return Result.success(result);
    }

    /**
     * 获取推荐专业
     */
    @GetMapping("/result/{resultId}/majors")
    @Operation(summary = "获取推荐专业", description = "根据测评结果获取推荐专业列表")
    public Result<List<Map<String, Object>>> getRecommendedMajors(
            @Parameter(description = "结果ID") @PathVariable Long resultId
    ) {
        List<Map<String, Object>> majors = assessmentService.getRecommendedMajors(resultId);
        return Result.success(majors);
    }
}
