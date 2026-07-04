package com.gaokao.ai.service;

import java.util.Map;

/**
 * AI推荐服务接口
 * 调用大模型API进行智能推荐
 */
public interface AiRecommendService {

    /**
     * AI智能推荐
     *
     * @param score       分数
     * @param ranking     位次
     * @param provinceId  省份ID
     * @param subjectType 科类
     * @param interests   兴趣/偏好（可选）
     * @return AI推荐结果
     */
    Map<String, Object> aiRecommend(int score, Integer ranking, Integer provinceId, Integer subjectType, String interests);

    /**
     * AI聊天
     *
     * @param message 用户消息
     * @return AI回复
     */
    String chat(String message);
}
