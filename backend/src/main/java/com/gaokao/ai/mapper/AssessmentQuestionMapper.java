package com.gaokao.ai.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.gaokao.ai.entity.AssessmentQuestion;
import org.apache.ibatis.annotations.Mapper;

/**
 * 测评题目Mapper
 */
@Mapper
public interface AssessmentQuestionMapper extends BaseMapper<AssessmentQuestion> {
}
