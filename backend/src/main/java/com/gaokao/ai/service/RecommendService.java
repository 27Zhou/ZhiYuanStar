package com.gaokao.ai.service;

import com.gaokao.ai.vo.RecommendVO;

/**
 * AI推荐服务接口
 */
public interface RecommendService {

    /**
     * 智能推荐院校
     *
     * @param score     用户分数
     * @param ranking   用户位次（可选）
     * @param provinceId 省份ID
     * @param subjectType 科类：1-文科，2-理科，3-综合改革
     * @return 推荐结果（冲刺/稳妥/保底三档）
     */
    RecommendVO recommend(int score, Integer ranking, Integer provinceId, Integer subjectType);
}
