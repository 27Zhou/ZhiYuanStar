package com.gaokao.ai.entity;

import com.baomidou.mybatisplus.annotation.*;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/**
 * 志愿明细实体
 */
@Data
@TableName("volunteer_detail")
@Schema(description = "志愿明细")
public class VolunteerDetail implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    @Schema(description = "ID")
    private Long id;

    @Schema(description = "方案ID")
    private Long planId;

    @Schema(description = "学校ID")
    private Long schoolId;

    @Schema(description = "专业ID")
    private Long majorId;

    @Schema(description = "优先级（排序）")
    private Integer priority;

    @Schema(description = "是否接受调剂：0-否，1-是")
    private Integer acceptAdjust;

    @Schema(description = "录取概率")
    private BigDecimal probability;

    @Schema(description = "备注")
    private String remark;

    @TableField(fill = FieldFill.INSERT)
    @Schema(description = "创建时间")
    private LocalDateTime createTime;
}
