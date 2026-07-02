package com.gaokao.ai.common;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import lombok.Data;

import java.io.Serializable;

/**
 * 分页请求基类
 *
 * @author gaokao-ai
 * @since 1.0.0
 */
@Data
@Schema(description = "分页请求参数")
public class PageRequest implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * 当前页码（从1开始）
     */
    @Schema(description = "当前页码", example = "1", minimum = "1")
    @Min(value = 1, message = "页码不能小于1")
    private int pageNum = 1;

    /**
     * 每页大小
     */
    @Schema(description = "每页大小", example = "10", minimum = "1", maximum = "100")
    @Min(value = 1, message = "每页大小不能小于1")
    @Max(value = 100, message = "每页大小不能大于100")
    private int pageSize = 10;

    /**
     * 排序字段
     */
    @Schema(description = "排序字段")
    private String orderBy;

    /**
     * 是否升序
     */
    @Schema(description = "是否升序", example = "false")
    private boolean ascending = false;

    /**
     * 获取偏移量
     */
    public int getOffset() {
        return (pageNum - 1) * pageSize;
    }
}
