package com.gaokao.ai.common;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.List;

/**
 * 分页结果封装
 *
 * @param <T> 数据类型
 * @author gaokao-ai
 * @since 1.0.0
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "分页结果")
public class PageResult<T> implements Serializable {

    private static final long serialVersionUID = 1L;

    /**
     * 总记录数
     */
    @Schema(description = "总记录数", example = "100")
    private long total;

    /**
     * 当前页码
     */
    @Schema(description = "当前页码", example = "1")
    private int pageNum;

    /**
     * 每页大小
     */
    @Schema(description = "每页大小", example = "10")
    private int pageSize;

    /**
     * 总页数
     */
    @Schema(description = "总页数", example = "10")
    private int totalPages;

    /**
     * 数据列表
     */
    @Schema(description = "数据列表")
    private List<T> records;

    /**
     * 是否有上一页
     */
    @Schema(description = "是否有上一页", example = "false")
    private boolean hasPrevious;

    /**
     * 是否有下一页
     */
    @Schema(description = "是否有下一页", example = "true")
    private boolean hasNext;

    /**
     * 创建分页结果
     */
    public static <T> PageResult<T> of(List<T> records, long total, int pageNum, int pageSize) {
        int totalPages = (int) Math.ceil((double) total / pageSize);
        return PageResult.<T>builder()
                .records(records)
                .total(total)
                .pageNum(pageNum)
                .pageSize(pageSize)
                .totalPages(totalPages)
                .hasPrevious(pageNum > 1)
                .hasNext(pageNum < totalPages)
                .build();
    }
}
