package com.gaokao.ai.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.gaokao.ai.entity.Favorite;
import org.apache.ibatis.annotations.Mapper;

/**
 * 收藏Mapper
 */
@Mapper
public interface FavoriteMapper extends BaseMapper<Favorite> {
}
