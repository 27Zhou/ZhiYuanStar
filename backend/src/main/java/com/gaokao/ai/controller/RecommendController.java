package com.gaokao.ai.controller;

import com.gaokao.ai.common.Result;
import com.gaokao.ai.service.RecommendService;
import com.gaokao.ai.vo.RecommendVO;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * 推荐控制器
 * 根据分数和位次智能推荐院校
 */
@Slf4j
@RestController
@RequestMapping("/recommend")
@RequiredArgsConstructor
@Tag(name = "智能推荐", description = "根据分数和位次推荐院校")
public class RecommendController {

    private final RecommendService recommendService;

    /**
     * 智能推荐院校
     *
     * 算法说明：
     * - 高分段（排名前30%）：使用位次法，根据位次对比历年录取位次
     * - 低分段（排名后70%）：使用线差法，根据分数与分数线的差值
     *
     * 返回三档推荐：
     * - 冲刺：录取概率 20-50%
     * - 稳妥：录取概率 50-80%
     * - 保底：录取概率 80%+
     */
    @GetMapping("/school")
    @Operation(summary = "智能推荐院校", description = "根据分数和位次推荐冲刺/稳妥/保底三档院校")
    public Result<RecommendVO> recommendSchools(
            @Parameter(description = "高考分数", required = true)
            @RequestParam int score,

            @Parameter(description = "省排名/位次（可选，有则使用位次法）")
            @RequestParam(required = false) Integer ranking,

            @Parameter(description = "省份ID", required = true)
            @RequestParam int provinceId,

            @Parameter(description = "科类：1-文科，2-理科，3-综合改革", required = true)
            @RequestParam int subjectType
    ) {
        log.info("推荐请求: score={}, ranking={}, provinceId={}, subjectType={}",
                score, ranking, provinceId, subjectType);

        // 参数校验
        if (score < 0 || score > 750) {
            return Result.error(400, "分数范围应在0-750之间");
        }
        if (provinceId < 1 || provinceId > 31) {
            return Result.error(400, "省份ID无效");
        }
        if (subjectType < 1 || subjectType > 3) {
            return Result.error(400, "科类无效：1-文科，2-理科，3-综合改革");
        }

        RecommendVO result = recommendService.recommend(score, ranking, provinceId, subjectType);
        return Result.success(result);
    }
}
