package com.gaokao.ai.entity;

import com.baomidou.mybatisplus.annotation.*;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * 志愿方案实体
 */
@Data
@TableName("volunteer_plan")
@Schema(description = "志愿方案")
public class VolunteerPlan implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    @Schema(description = "方案ID")
    private Long id;

    @Schema(description = "用户ID")
    private Long userId;

    @Schema(description = "方案名称")
    private String name;

    @Schema(description = "年份")
    private Integer year;

    @Schema(description = "省份")
    private String province;

    @Schema(description = "分数")
    private Integer score;

    @Schema(description = "排名")
    private Integer ranking;

    @Schema(description = "科类")
    private Integer subjectType;

    @Schema(description = "状态：0-草稿，1-已保存，2-已提交")
    private Integer status;

    @Schema(description = "备注")
    private String remark;

    @TableLogic
    @Schema(description = "逻辑删除")
    private Integer deleted;

    @TableField(fill = FieldFill.INSERT)
    @Schema(description = "创建时间")
    private LocalDateTime createTime;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    @Schema(description = "更新时间")
    private LocalDateTime updateTime;
}
