package com.gaokao.ai.service;

import com.gaokao.ai.entity.History;

import java.util.List;
import java.util.Map;

/**
 * 浏览记录服务接口
 */
public interface HistoryService {

    /**
     * 添加浏览记录
     */
    History addHistory(Long userId, Integer targetType, Long targetId, String content);

    /**
     * 获取浏览记录
     */
    List<Map<String, Object>> getHistory(Long userId, Integer targetType, int limit);

    /**
     * 清空浏览记录
     */
    void clearHistory(Long userId);
}
