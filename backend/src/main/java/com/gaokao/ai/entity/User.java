package com.gaokao.ai.entity;

import com.baomidou.mybatisplus.annotation.*;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * 用户实体
 */
@Data
@TableName("user")
@Schema(description = "用户")
public class User implements Serializable {

    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    @Schema(description = "用户ID")
    private Long id;

    @Schema(description = "用户名")
    private String username;

    @Schema(description = "密码(BCrypt加密)")
    private String password;

    @Schema(description = "真实姓名")
    private String realName;

    @Schema(description = "手机号")
    private String phone;

    @Schema(description = "邮箱")
    private String email;

    @Schema(description = "性别：0-未知，1-男，2-女")
    private Integer gender;

    @Schema(description = "头像URL")
    private String avatar;

    @Schema(description = "所在省份ID")
    private Integer provinceId;

    @Schema(description = "所在城市ID")
    private Integer cityId;

    @Schema(description = "高考分数")
    private Integer score;

    @Schema(description = "省排名/位次")
    private Integer ranking;

    @Schema(description = "科类：1-文科，2-理科，3-综合改革")
    private Integer subjectType;

    @Schema(description = "毕业年份")
    private Integer graduationYear;

    @Schema(description = "状态：0-禁用，1-正常")
    private Integer status;

    @Schema(description = "最后登录时间")
    private LocalDateTime lastLoginTime;

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
