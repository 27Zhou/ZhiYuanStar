package com.gaokao.ai.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.List;
import java.util.Map;

/**
 * 学校详情VO（完整字段）
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "学校详情信息")
public class SchoolDetailVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @Schema(description = "高校ID")
    private Long id;

    @Schema(description = "高校名称")
    private String name;

    @Schema(description = "高校代码")
    private String code;

    @Schema(description = "所在省份ID")
    private Integer provinceId;

    @Schema(description = "所在省份")
    private String provinceName;

    @Schema(description = "所在城市")
    private String cityName;

    @Schema(description = "详细地址")
    private String address;

    @Schema(description = "类型")
    private Integer type;

    @Schema(description = "类型名称")
    private String typeName;

    @Schema(description = "层次")
    private Integer level;

    @Schema(description = "层次名称")
    private String levelName;

    @Schema(description = "性质")
    private Integer nature;

    @Schema(description = "性质名称")
    private String natureName;

    @Schema(description = "是否985")
    private Integer is985;

    @Schema(description = "是否211")
    private Integer is211;

    @Schema(description = "是否双一流")
    private Integer isDoubleFirstClass;

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

    @Schema(description = "历年录取分数线（按年份分组）")
    private Map<String, List<Map<String, Object>>> admissionScores;

    @Schema(description = "开设专业列表")
    private List<Map<String, Object>> majors;
}
