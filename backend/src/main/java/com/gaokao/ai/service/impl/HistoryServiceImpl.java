package com.gaokao.ai.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.gaokao.ai.entity.History;
import com.gaokao.ai.entity.School;
import com.gaokao.ai.mapper.HistoryMapper;
import com.gaokao.ai.mapper.SchoolMapper;
import com.gaokao.ai.service.HistoryService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.*;

/**
 * 浏览记录服务实现
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class HistoryServiceImpl implements HistoryService {

    private final HistoryMapper historyMapper;
    private final SchoolMapper schoolMapper;

    @Override
    public History addHistory(Long userId, Integer targetType, Long targetId, String content) {
        History history = new History();
        history.setUserId(userId);
        history.setTargetType(targetType);
        history.setTargetId(targetId);
        history.setContent(content);
        historyMapper.insert(history);
        log.info("添加浏览记录: userId={}, targetType={}, targetId={}", userId, targetType, targetId);
        return history;
    }

    @Override
    public List<Map<String, Object>> getHistory(Long userId, Integer targetType, int limit) {
        LambdaQueryWrapper<History> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(History::getUserId, userId);
        if (targetType != null) {
            wrapper.eq(History::getTargetType, targetType);
        }
        wrapper.orderByDesc(History::getCreateTime);
        if (limit > 0) {
            wrapper.last("LIMIT " + limit);
        }
        List<History> histories = historyMapper.selectList(wrapper);

        List<Map<String, Object>> result = new ArrayList<>();
        for (History h : histories) {
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("id", h.getId());
            item.put("targetType", h.getTargetType());
            item.put("targetId", h.getTargetId());
            item.put("content", h.getContent());
            item.put("createTime", h.getCreateTime());

            // 获取学校名称
            if (h.getTargetType() == 1 && h.getTargetId() != null) {
                School school = schoolMapper.selectById(h.getTargetId());
                if (school != null) {
                    item.put("name", school.getName());
                }
            }

            result.add(item);
        }
        return result;
    }

    @Override
    public void clearHistory(Long userId) {
        LambdaQueryWrapper<History> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(History::getUserId, userId);
        historyMapper.delete(wrapper);
        log.info("清空浏览记录: userId={}", userId);
    }
}
