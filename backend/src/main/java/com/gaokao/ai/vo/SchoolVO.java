package com.gaokao.ai.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * 学校列表VO（精简字段，用于列表展示）
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "学校列表信息")
public class SchoolVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @Schema(description = "高校ID")
    private Long id;

    @Schema(description = "高校名称")
    private String name;

    @Schema(description = "高校代码")
    private String code;

    @Schema(description = "所在省份")
    private String provinceName;

    @Schema(description = "所在城市")
    private String cityName;

    @Schema(description = "类型: 1-综合, 2-理工, 3-师范...")
    private Integer type;

    @Schema(description = "类型名称")
    private String typeName;

    @Schema(description = "层次: 1-本科, 2-专科")
    private Integer level;

    @Schema(description = "层次名称")
    private String levelName;

    @Schema(description = "性质: 1-公办, 2-民办, 3-中外合作")
    private Integer nature;

    @Schema(description = "性质名称")
    private String natureName;

    @Schema(description = "是否985")
    private Boolean is985;

    @Schema(description = "是否211")
    private Boolean is211;

    @Schema(description = "是否双一流")
    private Boolean isDoubleFirstClass;

    @Schema(description = "校徽URL")
    private String logo;

    @Schema(description = "综合排名")
    private Integer ranking;

    @Schema(description = "官网地址")
    private String website;
}
