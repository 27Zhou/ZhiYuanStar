package com.gaokao.ai.service;

import com.gaokao.ai.entity.AssessmentQuestion;
import com.gaokao.ai.entity.AssessmentResult;

import java.util.List;
import java.util.Map;

/**
 * 心理测评服务接口
 */
public interface AssessmentService {

    /**
     * 获取测评题目
     */
    List<AssessmentQuestion> getQuestions();

    /**
     * 提交测评答案并生成结果
     *
     * @param answers 答案Map：key=题目ID, value=选项(A/B/C/D)
     * @return 测评结果
     */
    AssessmentResult submitAnswers(Map<Integer, String> answers);

    /**
     * 获取测评结果
     */
    AssessmentResult getResult(Long resultId);

    /**
     * 获取推荐专业
     */
    List<Map<String, Object>> getRecommendedMajors(Long resultId);
}
