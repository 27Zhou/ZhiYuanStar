package com.gaokao.ai.entity;

import com.baomidou.mybatisplus.annotation.*;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * 高校实体
 */
@Data
@TableName("school")
@Schema(description = "高校信息")
public class School implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    @Schema(description = "高校ID")
    private Long id;

    @Schema(description = "高校名称")
    private String name;

    @Schema(description = "高校代码(教育部编码)")
    private String code;

    @Schema(description = "所在省份ID")
    private Integer provinceId;

    @Schema(description = "所在城市ID")
    private Integer cityId;

    @Schema(description = "详细地址")
    private String address;

    @Schema(description = "类型: 1-综合, 2-理工, 3-师范, 4-医药, 5-财经, 6-政法, 7-农林, 8-艺术, 9-体育, 10-民族, 11-军事")
    private Integer type;

    @Schema(description = "层次: 1-本科, 2-专科")
    private Integer level;

    @Schema(description = "性质: 1-公办, 2-民办, 3-中外合作")
    private Integer nature;

    @TableField("is_985")
    @Schema(description = "是否985")
    private Boolean is985;

    @TableField("is_211")
    @Schema(description = "是否211")
    private Boolean is211;

    @TableField("is_double_first_class")
    @Schema(description = "是否双一流")
    private Boolean isDoubleFirstClass;

    @Schema(description = "官网地址")
    private String website;

    @Schema(description = "校徽URL")
    private String logo;

    @Schema(description = "学校简介")
    private String description;

    @Schema(description = "综合排名")
    private Integer ranking;

    @Schema(description = "在校生人数")
    private Integer studentCount;

    @Schema(description = "教职工人数")
    private Integer facultyCount;

    @Schema(description = "状态: 0-禁用, 1-正常")
    private Integer status;

    @TableLogic
    @Schema(description = "逻辑删除: 0-未删除, 1-已删除")
    private Integer deleted;

    @TableField(fill = FieldFill.INSERT)
    @Schema(description = "创建时间")
    private LocalDateTime createTime;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    @Schema(description = "更新时间")
    private LocalDateTime updateTime;
}
