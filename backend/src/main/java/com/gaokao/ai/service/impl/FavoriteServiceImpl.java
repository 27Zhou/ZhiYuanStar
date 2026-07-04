package com.gaokao.ai.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.gaokao.ai.entity.Favorite;
import com.gaokao.ai.entity.School;
import com.gaokao.ai.entity.Major;
import com.gaokao.ai.mapper.FavoriteMapper;
import com.gaokao.ai.mapper.SchoolMapper;
import com.gaokao.ai.mapper.MajorMapper;
import com.gaokao.ai.service.FavoriteService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.*;

/**
 * 收藏服务实现
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class FavoriteServiceImpl implements FavoriteService {

    private final FavoriteMapper favoriteMapper;
    private final SchoolMapper schoolMapper;
    private final MajorMapper majorMapper;

    @Override
    public Favorite addFavorite(Long userId, Integer targetType, Long targetId, String remark) {
        // 检查是否已收藏
        if (isFavorite(userId, targetType, targetId)) {
            log.info("已收藏，跳过: userId={}, targetType={}, targetId={}", userId, targetType, targetId);
            return null;
        }

        Favorite favorite = new Favorite();
        favorite.setUserId(userId);
        favorite.setTargetType(targetType);
        favorite.setTargetId(targetId);
        favorite.setRemark(remark);
        favoriteMapper.insert(favorite);

        log.info("添加收藏: userId={}, targetType={}, targetId={}", userId, targetType, targetId);
        return favorite;
    }

    @Override
    public boolean removeFavorite(Long userId, Integer targetType, Long targetId) {
        LambdaQueryWrapper<Favorite> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Favorite::getUserId, userId)
               .eq(Favorite::getTargetType, targetType)
               .eq(Favorite::getTargetId, targetId);
        int deleted = favoriteMapper.delete(wrapper);
        log.info("取消收藏: userId={}, targetType={}, targetId={}, result={}", userId, targetType, targetId, deleted > 0);
        return deleted > 0;
    }

    @Override
    public boolean isFavorite(Long userId, Integer targetType, Long targetId) {
        LambdaQueryWrapper<Favorite> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Favorite::getUserId, userId)
               .eq(Favorite::getTargetType, targetType)
               .eq(Favorite::getTargetId, targetId);
        return favoriteMapper.selectCount(wrapper) > 0;
    }

    @Override
    public List<Map<String, Object>> getFavorites(Long userId, Integer targetType) {
        LambdaQueryWrapper<Favorite> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Favorite::getUserId, userId);
        if (targetType != null) {
            wrapper.eq(Favorite::getTargetType, targetType);
        }
        wrapper.orderByDesc(Favorite::getCreateTime);
        List<Favorite> favorites = favoriteMapper.selectList(wrapper);

        List<Map<String, Object>> result = new ArrayList<>();
        for (Favorite fav : favorites) {
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("id", fav.getId());
            item.put("targetType", fav.getTargetType());
            item.put("targetId", fav.getTargetId());
            item.put("remark", fav.getRemark());
            item.put("createTime", fav.getCreateTime());

            // 获取目标名称
            if (fav.getTargetType() == 1) {
                School school = schoolMapper.selectById(fav.getTargetId());
                if (school != null) {
                    item.put("name", school.getName());
                    item.put("code", school.getCode());
                }
            } else if (fav.getTargetType() == 2) {
                Major major = majorMapper.selectById(fav.getTargetId());
                if (major != null) {
                    item.put("name", major.getName());
                    item.put("code", major.getCode());
                }
            }

            result.add(item);
        }
        return result;
    }

    @Override
    public int getFavoriteCount(Long userId) {
        LambdaQueryWrapper<Favorite> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Favorite::getUserId, userId);
        return Math.toIntExact(favoriteMapper.selectCount(wrapper));
    }
}
