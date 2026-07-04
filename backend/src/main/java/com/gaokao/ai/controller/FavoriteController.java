package com.gaokao.ai.controller;

import com.gaokao.ai.common.Result;
import com.gaokao.ai.entity.Favorite;
import com.gaokao.ai.service.FavoriteService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

/**
 * 收藏控制器
 */
@Slf4j
@RestController
@RequestMapping("/favorite")
@RequiredArgsConstructor
@Tag(name = "收藏管理", description = "学校/专业收藏接口")
public class FavoriteController {

    private final FavoriteService favoriteService;

    // 临时默认用户ID（未登录状态）
    private static final Long DEFAULT_USER_ID = 1L;

    @PostMapping("/add")
    @Operation(summary = "添加收藏", description = "收藏学校或专业")
    public Result<Favorite> addFavorite(
            @Parameter(description = "收藏类型：1-高校，2-专业") @RequestParam Integer targetType,
            @Parameter(description = "目标ID") @RequestParam Long targetId,
            @Parameter(description = "备注") @RequestParam(required = false) String remark
    ) {
        Favorite favorite = favoriteService.addFavorite(DEFAULT_USER_ID, targetType, targetId, remark);
        if (favorite == null) {
            return Result.error(400, "已收藏");
        }
        return Result.success(favorite);
    }

    @DeleteMapping("/remove")
    @Operation(summary = "取消收藏")
    public Result<String> removeFavorite(
            @Parameter(description = "收藏类型：1-高校，2-专业") @RequestParam Integer targetType,
            @Parameter(description = "目标ID") @RequestParam Long targetId
    ) {
        boolean removed = favoriteService.removeFavorite(DEFAULT_USER_ID, targetType, targetId);
        if (removed) {
            return Result.success("取消收藏成功");
        }
        return Result.error(400, "未收藏");
    }

    @GetMapping("/check")
    @Operation(summary = "检查是否已收藏")
    public Result<Boolean> checkFavorite(
            @Parameter(description = "收藏类型：1-高校，2-专业") @RequestParam Integer targetType,
            @Parameter(description = "目标ID") @RequestParam Long targetId
    ) {
        boolean isFavorite = favoriteService.isFavorite(DEFAULT_USER_ID, targetType, targetId);
        return Result.success(isFavorite);
    }

    @GetMapping("/list")
    @Operation(summary = "获取收藏列表")
    public Result<List<Map<String, Object>>> getFavorites(
            @Parameter(description = "收藏类型：1-高校，2-专业，不传返回全部") @RequestParam(required = false) Integer targetType
    ) {
        List<Map<String, Object>> favorites = favoriteService.getFavorites(DEFAULT_USER_ID, targetType);
        return Result.success(favorites);
    }

    @GetMapping("/count")
    @Operation(summary = "获取收藏数量")
    public Result<Integer> getFavoriteCount() {
        int count = favoriteService.getFavoriteCount(DEFAULT_USER_ID);
        return Result.success(count);
    }
}
