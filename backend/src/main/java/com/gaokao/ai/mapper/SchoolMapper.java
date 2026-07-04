package com.gaokao.ai.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.gaokao.ai.entity.School;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;

import java.util.List;
import java.util.Map;

/**
 * 高校Mapper
 */
@Mapper
public interface SchoolMapper extends BaseMapper<School> {

    /**
     * 统计各省份高校数量
     */
    @Select("SELECT p.name as provinceName, COUNT(*) as count " +
            "FROM school s JOIN province p ON s.province_id = p.id " +
            "WHERE s.deleted = 0 GROUP BY p.id, p.name ORDER BY count DESC")
    List<Map<String, Object>> countByProvince();

    /**
     * 统计各类型高校数量
     */
    @Select("SELECT type, COUNT(*) as count FROM school WHERE deleted = 0 GROUP BY type")
    List<Map<String, Object>> countByType();
}
