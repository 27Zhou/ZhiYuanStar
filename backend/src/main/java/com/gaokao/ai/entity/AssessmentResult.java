package com.gaokao.ai.entity;

import com.baomidou.mybatisplus.annotation.*;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * 测评结果实体
 */
@Data
@TableName("assessment_result")
@Schema(description = "测评结果")
public class AssessmentResult implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    @Schema(description = "结果ID")
    private Long id;

    @Schema(description = "用户ID（可选，未登录时为空）")
    private Long userId;

    @Schema(description = "会话ID（用于未登录用户）")
    private String sessionId;

    @Schema(description = "逻辑思维得分")
    private Integer logicScore;

    @Schema(description = "创造能力得分")
    private Integer creativityScore;

    @Schema(description = "沟通能力得分")
    private Integer communicationScore;

    @Schema(description = "领导能力得分")
    private Integer leadershipScore;

    @Schema(description = "动手能力得分")
    private Integer handsOnScore;

    @Schema(description = "社交能力得分")
    private Integer socialScore;

    @Schema(description = "艺术感知得分")
    private Integer artisticScore;

    @Schema(description = "实践能力得分")
    private Integer practicalScore;

    @Schema(description = "共情能力得分")
    private Integer empathyScore;

    @Schema(description = "创新能力得分")
    private Integer innovationScore;

    @Schema(description = "分析能力得分")
    private Integer analysisScore;

    @Schema(description = "执行能力得分")
    private Integer executionScore;

    @Schema(description = "推荐专业方向（JSON数组）")
    private String recommendedMajors;

    @Schema(description = "性格类型描述")
    private String personalityType;

    @Schema(description = "详细分析报告")
    private String report;

    @TableField(fill = FieldFill.INSERT)
    @Schema(description = "创建时间")
    private LocalDateTime createTime;
}
