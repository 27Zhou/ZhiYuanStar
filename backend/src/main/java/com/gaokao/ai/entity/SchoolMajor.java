package com.gaokao.ai.entity;

import com.baomidou.mybatisplus.annotation.*;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 高校专业关联实体
 */
@Data
@TableName("school_major")
@Schema(description = "高校专业关联")
public class SchoolMajor implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    @Schema(description = "ID")
    private Long id;

    @Schema(description = "高校ID")
    private Long schoolId;

    @Schema(description = "专业ID")
    private Long majorId;

    @Schema(description = "专业排名")
    private Integer ranking;

    @Schema(description = "是否重点学科: 0-否, 1-是")
    private Integer isKey;

    @Schema(description = "是否国家重点学科: 0-否, 1-是")
    private Integer isNationalKey;

    @Schema(description = "学费(元/年)")
    private BigDecimal tuition;

    @Schema(description = "备注")
    private String remark;

    @TableField(fill = FieldFill.INSERT)
    @Schema(description = "创建时间")
    private LocalDateTime createTime;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    @Schema(description = "更新时间")
    private LocalDateTime updateTime;
}
