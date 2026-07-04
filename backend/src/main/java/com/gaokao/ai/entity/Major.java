package com.gaokao.ai.entity;

import com.baomidou.mybatisplus.annotation.*;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * 专业实体
 */
@Data
@TableName("major")
@Schema(description = "专业信息")
public class Major implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    @Schema(description = "专业ID")
    private Long id;

    @Schema(description = "专业名称")
    private String name;

    @Schema(description = "专业代码")
    private String code;

    @Schema(description = "专业大类")
    private String category;

    @Schema(description = "专业小类")
    private String subCategory;

    @Schema(description = "选科要求(新高考)")
    private String subjectRequirements;

    @Schema(description = "学制")
    private Integer duration;

    @Schema(description = "授予学位")
    private String degree;

    @Schema(description = "专业介绍")
    private String description;

    @Schema(description = "就业方向")
    private String employmentDirection;

    @Schema(description = "薪资范围")
    private String salaryRange;

    @Schema(description = "是否特色专业: 0-否, 1-是")
    private Integer isSpecial;

    @Schema(description = "状态: 0-禁用, 1-正常")
    private Integer status;

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
