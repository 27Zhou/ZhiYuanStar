package com.gaokao.ai.entity;

import com.baomidou.mybatisplus.annotation.*;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 历年录取分数线实体
 */
@Data
@TableName("admission_score")
@Schema(description = "历年录取分数线")
public class AdmissionScore implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    @Schema(description = "ID")
    private Long id;

    @Schema(description = "高校ID")
    private Long schoolId;

    @Schema(description = "专业ID")
    private Long majorId;

    @Schema(description = "年份")
    private Integer year;

    @Schema(description = "招生省份ID")
    private Integer provinceId;

    @Schema(description = "科类: 1-文科, 2-理科, 3-综合改革")
    private Integer subjectType;

    @Schema(description = "批次")
    private String batch;

    @Schema(description = "最低分")
    private Integer minScore;

    @Schema(description = "最高分")
    private Integer maxScore;

    @Schema(description = "平均分")
    private BigDecimal avgScore;

    @Schema(description = "最低位次")
    private Integer minRanking;

    @Schema(description = "计划招生数")
    private Integer planCount;

    @Schema(description = "实际录取数")
    private Integer enrollCount;

    @TableField(fill = FieldFill.INSERT)
    @Schema(description = "创建时间")
    private LocalDateTime createTime;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    @Schema(description = "更新时间")
    private LocalDateTime updateTime;
}
