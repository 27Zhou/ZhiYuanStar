package com.gaokao.ai.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.gaokao.ai.entity.SchoolMajor;
import org.apache.ibatis.annotations.Mapper;

/**
 * 高校专业关联Mapper
 */
@Mapper
public interface SchoolMajorMapper extends BaseMapper<SchoolMajor> {
}
