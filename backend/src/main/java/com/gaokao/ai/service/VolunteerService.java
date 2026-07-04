package com.gaokao.ai.service;

import com.gaokao.ai.entity.VolunteerDetail;
import com.gaokao.ai.entity.VolunteerPlan;

import java.util.List;
import java.util.Map;

/**
 * 志愿方案服务接口
 */
public interface VolunteerService {

    /**
     * 创建志愿方案
     */
    VolunteerPlan createPlan(VolunteerPlan plan);

    /**
     * 获取用户的志愿方案列表
     */
    List<VolunteerPlan> getPlans(Long userId);

    /**
     * 获取志愿方案详情
     */
    Map<String, Object> getPlanDetail(Long planId);

    /**
     * 更新志愿方案
     */
    VolunteerPlan updatePlan(VolunteerPlan plan);

    /**
     * 删除志愿方案
     */
    boolean deletePlan(Long planId, Long userId);

    /**
     * 添加志愿明细
     */
    VolunteerDetail addDetail(VolunteerDetail detail);

    /**
     * 删除志愿明细
     */
    boolean removeDetail(Long detailId);

    /**
     * 更新志愿明细排序
     */
    boolean updateDetailPriority(Long detailId, Integer priority);
}
