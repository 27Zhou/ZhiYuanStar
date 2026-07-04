package com.gaokao.ai.service;

import com.gaokao.ai.entity.Favorite;

import java.util.List;
import java.util.Map;

/**
 * 收藏服务接口
 */
public interface FavoriteService {

    /**
     * 添加收藏
     */
    Favorite addFavorite(Long userId, Integer targetType, Long targetId, String remark);

    /**
     * 取消收藏
     */
    boolean removeFavorite(Long userId, Integer targetType, Long targetId);

    /**
     * 检查是否已收藏
     */
    boolean isFavorite(Long userId, Integer targetType, Long targetId);

    /**
     * 获取用户收藏列表
     */
    List<Map<String, Object>> getFavorites(Long userId, Integer targetType);

    /**
     * 获取收藏数量
     */
    int getFavoriteCount(Long userId);
}
