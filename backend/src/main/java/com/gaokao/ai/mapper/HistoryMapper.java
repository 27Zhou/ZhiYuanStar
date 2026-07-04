package com.gaokao.ai.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.gaokao.ai.entity.History;
import org.apache.ibatis.annotations.Mapper;

/**
 * 浏览记录Mapper
 */
@Mapper
public interface HistoryMapper extends BaseMapper<History> {
}
