package com.gaokao.ai.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.gaokao.ai.entity.AdmissionScore;
import org.apache.ibatis.annotations.Mapper;

/**
 * 录取分数线Mapper
 */
@Mapper
public interface AdmissionScoreMapper extends BaseMapper<AdmissionScore> {
}
