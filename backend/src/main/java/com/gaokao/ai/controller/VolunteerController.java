package com.gaokao.ai.controller;

import com.gaokao.ai.common.Result;
import com.gaokao.ai.entity.VolunteerDetail;
import com.gaokao.ai.entity.VolunteerPlan;
import com.gaokao.ai.service.VolunteerService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 志愿方案控制器
 */
@Slf4j
@RestController
@RequestMapping("/volunteer")
@RequiredArgsConstructor
@Tag(name = "志愿方案", description = "志愿填报方案管理")
public class VolunteerController {

    private final VolunteerService volunteerService;

    // 临时默认用户ID（未登录状态）
    private static final Long DEFAULT_USER_ID = 1L;

    @PostMapping("/plan")
    @Operation(summary = "创建志愿方案")
    public Result<VolunteerPlan> createPlan(@RequestBody VolunteerPlan plan) {
        plan.setUserId(DEFAULT_USER_ID);
        plan.setStatus(1);
        VolunteerPlan created = volunteerService.createPlan(plan);
        return Result.success(created);
    }

    @GetMapping("/plans")
    @Operation(summary = "获取志愿方案列表")
    public Result<List<VolunteerPlan>> getPlans() {
        List<VolunteerPlan> plans = volunteerService.getPlans(DEFAULT_USER_ID);
        return Result.success(plans);
    }

    @GetMapping("/plan/{planId}")
    @Operation(summary = "获取志愿方案详情")
    public Result<Map<String, Object>> getPlanDetail(
            @Parameter(description = "方案ID") @PathVariable Long planId
    ) {
        Map<String, Object> detail = volunteerService.getPlanDetail(planId);
        if (detail == null) {
            return Result.error(404, "方案不存在");
        }
        return Result.success(detail);
    }

    @PutMapping("/plan/{planId}")
    @Operation(summary = "更新志愿方案")
    public Result<VolunteerPlan> updatePlan(
            @Parameter(description = "方案ID") @PathVariable Long planId,
            @RequestBody VolunteerPlan plan
    ) {
        plan.setId(planId);
        plan.setUserId(DEFAULT_USER_ID);
        VolunteerPlan updated = volunteerService.updatePlan(plan);
        return Result.success(updated);
    }

    @DeleteMapping("/plan/{planId}")
    @Operation(summary = "删除志愿方案")
    public Result<String> deletePlan(
            @Parameter(description = "方案ID") @PathVariable Long planId
    ) {
        boolean deleted = volunteerService.deletePlan(planId, DEFAULT_USER_ID);
        if (deleted) {
            return Result.success("删除成功");
        }
        return Result.error(400, "删除失败");
    }

    @PostMapping("/detail")
    @Operation(summary = "添加志愿明细（添加学校到方案）")
    public Result<VolunteerDetail> addDetail(@RequestBody VolunteerDetail detail) {
        VolunteerDetail added = volunteerService.addDetail(detail);
        return Result.success(added);
    }

    @DeleteMapping("/detail/{detailId}")
    @Operation(summary = "删除志愿明细")
    public Result<String> removeDetail(
            @Parameter(description = "明细ID") @PathVariable Long detailId
    ) {
        boolean removed = volunteerService.removeDetail(detailId);
        if (removed) {
            return Result.success("删除成功");
        }
        return Result.error(400, "删除失败");
    }

    @PutMapping("/detail/{detailId}/priority")
    @Operation(summary = "更新志愿排序")
    public Result<String> updateDetailPriority(
            @Parameter(description = "明细ID") @PathVariable Long detailId,
            @Parameter(description = "优先级") @RequestParam Integer priority
    ) {
        boolean updated = volunteerService.updateDetailPriority(detailId, priority);
        if (updated) {
            return Result.success("更新成功");
        }
        return Result.error(400, "更新失败");
    }
}
