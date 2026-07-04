package com.gaokao.ai.controller;

import com.gaokao.ai.common.PageResult;
import com.gaokao.ai.common.Result;
import com.gaokao.ai.service.SchoolService;
import com.gaokao.ai.vo.SchoolDetailVO;
import com.gaokao.ai.vo.SchoolVO;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 学校控制器
 * 提供院校查询、详情、统计等接口
 */
@Slf4j
@RestController
@RequestMapping("/school")
@RequiredArgsConstructor
@Tag(name = "院校查询", description = "院校搜索、详情、统计接口")
public class SchoolController {

    private final SchoolService schoolService;

    /**
     * 多条件模糊分页查询学校
     */
    @GetMapping("/search")
    @Operation(summary = "搜索学校", description = "根据关键词、省份、类型等条件分页查询学校")
    public Result<PageResult<SchoolVO>> searchSchools(
            @Parameter(description = "关键词（学校名称/代码）") @RequestParam(required = false) String keyword,
            @Parameter(description = "省份ID") @RequestParam(required = false) Integer province,
            @Parameter(description = "学校类型: 1-综合, 2-理工, 3-师范...") @RequestParam(required = false) Integer type,
            @Parameter(description = "办学层次: 1-本科, 2-专科") @RequestParam(required = false) Integer level,
            @Parameter(description = "办学性质: 1-公办, 2-民办, 3-中外合作") @RequestParam(required = false) Integer nature,
            @Parameter(description = "是否985") @RequestParam(required = false) Integer is985,
            @Parameter(description = "是否211") @RequestParam(required = false) Integer is211,
            @Parameter(description = "是否双一流") @RequestParam(required = false) Integer isDouble,
            @Parameter(description = "页码") @RequestParam(defaultValue = "1") int pageNum,
            @Parameter(description = "每页大小") @RequestParam(defaultValue = "10") int pageSize,
            @Parameter(description = "排序字段") @RequestParam(defaultValue = "ranking") String sortField,
            @Parameter(description = "排序方向") @RequestParam(defaultValue = "asc") String sortOrder
    ) {
        log.info("搜索学校: keyword={}, province={}, type={}, level={}, pageNum={}",
                keyword, province, type, level, pageNum);

        PageResult<SchoolVO> result = schoolService.searchSchools(
                keyword, province, type, level, nature,
                is985, is211, isDouble,
                pageNum, pageSize, sortField, sortOrder
        );

        return Result.success(result);
    }

    /**
     * 根据ID查询学校详情
     */
    @GetMapping("/detail/{schoolId}")
    @Operation(summary = "学校详情", description = "根据学校ID查询详细信息，包括简介、录取分数线、专业列表")
    public Result<SchoolDetailVO> getSchoolDetail(
            @Parameter(description = "学校ID") @PathVariable Long schoolId
    ) {
        log.info("查询学校详情: schoolId={}", schoolId);

        SchoolDetailVO detail = schoolService.getSchoolDetail(schoolId);
        if (detail == null) {
            return Result.error(404, "学校不存在");
        }

        return Result.success(detail);
    }

    /**
     * 获取学校统计信息
     */
    @GetMapping("/statistics")
    @Operation(summary = "学校统计", description = "获取学校数量统计（按省份、类型分布）")
    public Result<Map<String, Object>> getStatistics() {
        log.info("查询学校统计信息");

        Map<String, Object> stats = schoolService.getStatistics();
        return Result.success(stats);
    }
}
