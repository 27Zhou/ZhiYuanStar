package com.gaokao.ai.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.gaokao.ai.common.PageResult;
import com.gaokao.ai.entity.AdmissionScore;
import com.gaokao.ai.entity.Major;
import com.gaokao.ai.entity.School;
import com.gaokao.ai.mapper.AdmissionScoreMapper;
import com.gaokao.ai.mapper.MajorMapper;
import com.gaokao.ai.mapper.SchoolMapper;
import com.gaokao.ai.service.SchoolService;
import com.gaokao.ai.vo.SchoolDetailVO;
import com.gaokao.ai.vo.SchoolVO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.util.*;
import java.util.stream.Collectors;

/**
 * 学校服务实现
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class SchoolServiceImpl implements SchoolService {

    private final SchoolMapper schoolMapper;
    private final AdmissionScoreMapper admissionScoreMapper;
    private final MajorMapper majorMapper;

    // 类型映射
    private static final Map<Integer, String> TYPE_MAP = Map.ofEntries(
            Map.entry(1, "综合"), Map.entry(2, "理工"), Map.entry(3, "师范"),
            Map.entry(4, "医药"), Map.entry(5, "财经"), Map.entry(6, "政法"),
            Map.entry(7, "农林"), Map.entry(8, "艺术"), Map.entry(9, "体育"),
            Map.entry(10, "民族"), Map.entry(11, "军事")
    );

    private static final Map<Integer, String> LEVEL_MAP = Map.of(
            1, "本科", 2, "专科"
    );

    private static final Map<Integer, String> NATURE_MAP = Map.of(
            1, "公办", 2, "民办", 3, "中外合作"
    );

    @Override
    public PageResult<SchoolVO> searchSchools(
            String keyword, Integer provinceId, Integer type,
            Integer level, Integer nature, Integer is985,
            Integer is211, Integer isDouble,
            int pageNum, int pageSize,
            String sortField, String sortOrder) {

        // 构建查询条件
        LambdaQueryWrapper<School> wrapper = new LambdaQueryWrapper<>();

        // 关键词模糊查询
        if (StringUtils.hasText(keyword)) {
            wrapper.and(w -> w
                    .like(School::getName, keyword)
                    .or()
                    .like(School::getCode, keyword)
            );
        }

        // 精确筛选条件
        if (provinceId != null) {
            wrapper.eq(School::getProvinceId, provinceId);
        }
        if (type != null) {
            wrapper.eq(School::getType, type);
        }
        if (level != null) {
            wrapper.eq(School::getLevel, level);
        }
        if (nature != null) {
            wrapper.eq(School::getNature, nature);
        }
        if (is985 != null && is985 == 1) {
            wrapper.eq(School::getIs985, 1);
        }
        if (is211 != null && is211 == 1) {
            wrapper.eq(School::getIs211, 1);
        }
        if (isDouble != null && isDouble == 1) {
            wrapper.eq(School::getIsDoubleFirstClass, 1);
        }

        // 排序
        if ("ranking".equals(sortField)) {
            if ("asc".equals(sortOrder)) {
                wrapper.orderByAsc(School::getRanking);
            } else {
                wrapper.orderByDesc(School::getRanking);
            }
        } else {
            wrapper.orderByAsc(School::getId);
        }

        // 分页查询
        Page<School> page = new Page<>(pageNum, pageSize);
        Page<School> result = schoolMapper.selectPage(page, wrapper);

        // 转换为VO
        List<SchoolVO> voList = result.getRecords().stream()
                .map(this::toSchoolVO)
                .collect(Collectors.toList());

        return PageResult.of(voList, result.getTotal(), pageNum, pageSize);
    }

    @Override
    public SchoolDetailVO getSchoolDetail(Long schoolId) {
        // 查询学校基本信息
        School school = schoolMapper.selectById(schoolId);
        if (school == null) {
            return null;
        }

        // 查询录取分数线
        LambdaQueryWrapper<AdmissionScore> scoreWrapper = new LambdaQueryWrapper<>();
        scoreWrapper.eq(AdmissionScore::getSchoolId, schoolId)
                .orderByDesc(AdmissionScore::getYear);
        List<AdmissionScore> scores = admissionScoreMapper.selectList(scoreWrapper);

        // 按年份分组
        Map<String, List<Map<String, Object>>> scoreMap = scores.stream()
                .collect(Collectors.groupingBy(
                        s -> String.valueOf(s.getYear()),
                        Collectors.mapping(this::scoreToMap, Collectors.toList())
                ));

        // 查询开设专业
        LambdaQueryWrapper<Major> majorWrapper = new LambdaQueryWrapper<>();
        majorWrapper.eq(Major::getStatus, 1).orderByAsc(Major::getCode);
        List<Major> majors = majorMapper.selectList(majorWrapper);
        List<Map<String, Object>> majorList = majors.stream()
                .map(this::majorToMap)
                .collect(Collectors.toList());

        // 构建详情VO
        return SchoolDetailVO.builder()
                .id(school.getId())
                .name(school.getName())
                .code(school.getCode())
                .provinceId(school.getProvinceId())
                .provinceName(null) // 需要关联查询
                .cityName(null)
                .address(school.getAddress())
                .type(school.getType())
                .typeName(TYPE_MAP.getOrDefault(school.getType(), "未知"))
                .level(school.getLevel())
                .levelName(LEVEL_MAP.getOrDefault(school.getLevel(), "未知"))
                .nature(school.getNature())
                .natureName(NATURE_MAP.getOrDefault(school.getNature(), "未知"))
                .is985(school.getIs985())
                .is211(school.getIs211())
                .isDoubleFirstClass(school.getIsDoubleFirstClass())
                .website(school.getWebsite())
                .logo(school.getLogo())
                .description(school.getDescription())
                .ranking(school.getRanking())
                .studentCount(school.getStudentCount())
                .facultyCount(school.getFacultyCount())
                .admissionScores(scoreMap)
                .majors(majorList)
                .build();
    }

    @Override
    public Map<String, Object> getStatistics() {
        Map<String, Object> stats = new HashMap<>();
        stats.put("totalSchools", schoolMapper.selectCount(null));
        stats.put("byProvince", schoolMapper.countByProvince());
        stats.put("byType", schoolMapper.countByType());
        return stats;
    }

    /**
     * School -> SchoolVO
     */
    private SchoolVO toSchoolVO(School school) {
        return SchoolVO.builder()
                .id(school.getId())
                .name(school.getName())
                .code(school.getCode())
                .provinceName(null)
                .cityName(null)
                .type(school.getType())
                .typeName(TYPE_MAP.getOrDefault(school.getType(), "未知"))
                .level(school.getLevel())
                .levelName(LEVEL_MAP.getOrDefault(school.getLevel(), "未知"))
                .nature(school.getNature())
                .natureName(NATURE_MAP.getOrDefault(school.getNature(), "未知"))
                .is985(school.getIs985())
                .is211(school.getIs211())
                .isDoubleFirstClass(school.getIsDoubleFirstClass())
                .logo(school.getLogo())
                .ranking(school.getRanking())
                .website(school.getWebsite())
                .build();
    }

    /**
     * AdmissionScore -> Map
     */
    private Map<String, Object> scoreToMap(AdmissionScore score) {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("id", score.getId());
        map.put("year", score.getYear());
        map.put("provinceId", score.getProvinceId());
        map.put("subjectType", score.getSubjectType());
        map.put("batch", score.getBatch());
        map.put("minScore", score.getMinScore());
        map.put("maxScore", score.getMaxScore());
        map.put("avgScore", score.getAvgScore());
        map.put("minRanking", score.getMinRanking());
        map.put("planCount", score.getPlanCount());
        map.put("enrollCount", score.getEnrollCount());
        return map;
    }

    /**
     * Major -> Map
     */
    private Map<String, Object> majorToMap(Major major) {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("id", major.getId());
        map.put("name", major.getName());
        map.put("code", major.getCode());
        map.put("category", major.getCategory());
        map.put("duration", major.getDuration());
        map.put("degree", major.getDegree());
        return map;
    }
}
