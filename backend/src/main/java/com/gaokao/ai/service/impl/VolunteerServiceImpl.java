package com.gaokao.ai.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.gaokao.ai.entity.School;
import com.gaokao.ai.entity.VolunteerDetail;
import com.gaokao.ai.entity.VolunteerPlan;
import com.gaokao.ai.mapper.SchoolMapper;
import com.gaokao.ai.mapper.VolunteerDetailMapper;
import com.gaokao.ai.mapper.VolunteerPlanMapper;
import com.gaokao.ai.service.VolunteerService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.*;

/**
 * 志愿方案服务实现
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class VolunteerServiceImpl implements VolunteerService {

    private final VolunteerPlanMapper planMapper;
    private final VolunteerDetailMapper detailMapper;
    private final SchoolMapper schoolMapper;

    @Override
    public VolunteerPlan createPlan(VolunteerPlan plan) {
        planMapper.insert(plan);
        log.info("创建志愿方案: id={}, name={}", plan.getId(), plan.getName());
        return plan;
    }

    @Override
    public List<VolunteerPlan> getPlans(Long userId) {
        LambdaQueryWrapper<VolunteerPlan> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(VolunteerPlan::getUserId, userId)
               .eq(VolunteerPlan::getDeleted, 0)
               .orderByDesc(VolunteerPlan::getUpdateTime);
        return planMapper.selectList(wrapper);
    }

    @Override
    public Map<String, Object> getPlanDetail(Long planId) {
        VolunteerPlan plan = planMapper.selectById(planId);
        if (plan == null) {
            return null;
        }

        // 查询志愿明细
        LambdaQueryWrapper<VolunteerDetail> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(VolunteerDetail::getPlanId, planId)
               .orderByAsc(VolunteerDetail::getPriority);
        List<VolunteerDetail> details = detailMapper.selectList(wrapper);

        // 填充学校名称
        List<Map<String, Object>> detailList = new ArrayList<>();
        for (VolunteerDetail d : details) {
            Map<String, Object> item = new LinkedHashMap<>();
            item.put("id", d.getId());
            item.put("planId", d.getPlanId());
            item.put("schoolId", d.getSchoolId());
            item.put("majorId", d.getMajorId());
            item.put("priority", d.getPriority());
            item.put("acceptAdjust", d.getAcceptAdjust());
            item.put("probability", d.getProbability());
            item.put("remark", d.getRemark());

            School school = schoolMapper.selectById(d.getSchoolId());
            if (school != null) {
                item.put("schoolName", school.getName());
                item.put("schoolCode", school.getCode());
            }

            detailList.add(item);
        }

        Map<String, Object> result = new LinkedHashMap<>();
        result.put("plan", plan);
        result.put("details", detailList);
        return result;
    }

    @Override
    public VolunteerPlan updatePlan(VolunteerPlan plan) {
        planMapper.updateById(plan);
        log.info("更新志愿方案: id={}", plan.getId());
        return plan;
    }

    @Override
    public boolean deletePlan(Long planId, Long userId) {
        LambdaQueryWrapper<VolunteerPlan> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(VolunteerPlan::getId, planId)
               .eq(VolunteerPlan::getUserId, userId);
        int deleted = planMapper.delete(wrapper);
        log.info("删除志愿方案: planId={}, result={}", planId, deleted > 0);
        return deleted > 0;
    }

    @Override
    public VolunteerDetail addDetail(VolunteerDetail detail) {
        detailMapper.insert(detail);
        log.info("添加志愿明细: planId={}, schoolId={}", detail.getPlanId(), detail.getSchoolId());
        return detail;
    }

    @Override
    public boolean removeDetail(Long detailId) {
        int deleted = detailMapper.deleteById(detailId);
        log.info("删除志愿明细: detailId={}, result={}", detailId, deleted > 0);
        return deleted > 0;
    }

    @Override
    public boolean updateDetailPriority(Long detailId, Integer priority) {
        VolunteerDetail detail = detailMapper.selectById(detailId);
        if (detail == null) {
            return false;
        }
        detail.setPriority(priority);
        detailMapper.updateById(detail);
        log.info("更新志愿明细排序: detailId={}, priority={}", detailId, priority);
        return true;
    }
}
