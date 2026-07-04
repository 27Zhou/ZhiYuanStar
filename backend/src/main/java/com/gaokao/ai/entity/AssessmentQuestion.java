package com.gaokao.ai.entity;

import com.baomidou.mybatisplus.annotation.*;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * 测评题目实体
 */
@Data
@TableName("assessment_question")
@Schema(description = "测评题目")
public class AssessmentQuestion implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    @Schema(description = "题目ID")
    private Integer id;

    @Schema(description = "题目内容")
    private String content;

    @Schema(description = "选项A")
    private String optionA;

    @Schema(description = "选项B")
    private String optionB;

    @Schema(description = "选项C")
    private String optionC;

    @Schema(description = "选项D")
    private String optionD;

    @Schema(description = "能力维度：logic/logic/creativity/communication/leadership/hands_on/social/artistic/practical/empathy/innovation/analysis")
    private String dimension;

    @Schema(description = "题目排序")
    private Integer sortOrder;

    @Schema(description = "状态：0-禁用，1-正常")
    private Integer status;

    @TableField(fill = FieldFill.INSERT)
    @Schema(description = "创建时间")
    private LocalDateTime createTime;
}
