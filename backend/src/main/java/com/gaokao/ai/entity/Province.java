package com.gaokao.ai.entity;

import com.baomidou.mybatisplus.annotation.*;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * 省份实体
 */
@Data
@TableName("province")
@Schema(description = "省份信息")
public class Province implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    @Schema(description = "省份ID")
    private Integer id;

    @Schema(description = "省份名称")
    private String name;

    @Schema(description = "省份代码")
    private String code;

    @Schema(description = "所属区域")
    private String region;

    @Schema(description = "是否新高考省份: 0-否, 1-是")
    private Integer isNewGaokao;

    @TableField(fill = FieldFill.INSERT)
    @Schema(description = "创建时间")
    private LocalDateTime createTime;

    @TableField(fill = FieldFill.INSERT_UPDATE)
    @Schema(description = "更新时间")
    private LocalDateTime updateTime;
}
