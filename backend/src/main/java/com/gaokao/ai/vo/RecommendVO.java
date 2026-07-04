package com.gaokao.ai.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.List;

/**
 * 推荐结果VO
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "推荐结果")
public class RecommendVO implements Serializable {

    private static final long serialVersionUID = 1L;

    @Schema(description = "用户分数")
    private Integer score;

    @Schema(description = "用户位次")
    private Integer ranking;

    @Schema(description = "推荐算法：ranking=位次法，score_diff=线差法")
    private String algorithm;

    @Schema(description = "冲刺院校")
    private List<RecommendSchool> rush;

    @Schema(description = "稳妥院校")
    private List<RecommendSchool> stable;

    @Schema(description = "保底院校")
    private List<RecommendSchool> safe;

    /**
     * 推荐院校详情
     */
    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    @Schema(description = "推荐院校")
    public static class RecommendSchool implements Serializable {

        private static final long serialVersionUID = 1L;

        @Schema(description = "学校ID")
        private Long id;

        @Schema(description = "学校名称")
        private String name;

        @Schema(description = "学校代码")
        private String code;

        @Schema(description = "省份")
        private String provinceName;

        @Schema(description = "类型")
        private String typeName;

        @Schema(description = "是否985")
        private Boolean is985;

        @Schema(description = "是否211")
        private Boolean is211;

        @Schema(description = "是否双一流")
        private Boolean isDoubleFirstClass;

        @Schema(description = "历年最低分")
        private Integer minScore;

        @Schema(description = "历年最低位次")
        private Integer minRanking;

        @Schema(description = "分数差（用户分-最低分）")
        private Integer scoreDiff;

        @Schema(description = "位次差（用户位次-最低位次）")
        private Integer rankingDiff;

        @Schema(description = "录取概率（百分比）")
        private Integer probability;

        @Schema(description = "推荐理由")
        private String reason;
    }
}
