package com.gaokao.ai.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.gaokao.ai.common.PageResult;
import com.gaokao.ai.entity.*;
import com.gaokao.ai.mapper.*;
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
    private final SchoolMajorMapper schoolMajorMapper;
    private final ProvinceMapper provinceMapper;

    // Fix: 问题3 - 省份名称缓存Map，启动时加载
    private Map<Integer, String> provinceNameMap;

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

    /**
     * Fix: 问题3 - 获取省份名称映射（懒加载）
     */
    private Map<Integer, String> getProvinceNameMap() {
        if (provinceNameMap == null) {
            List<Province> provinces = provinceMapper.selectList(null);
            provinceNameMap = new HashMap<>();
            for (Province p : provinces) {
                provinceNameMap.put(p.getId(), p.getName());
            }
        }
        return provinceNameMap;
    }

    /**
     * Fix: 问题3 - 根据省份ID获取省份名称
     */
    private String resolveProvinceName(Integer provinceId) {
        if (provinceId == null) return null;
        return getProvinceNameMap().getOrDefault(provinceId, "未知");
    }

    @Override
    public PageResult<SchoolVO> searchSchools(
            String keyword, Integer provinceId, Integer type,
            Integer level, Integer nature, Integer is985,
            Integer is211, Integer isDouble,
            int pageNum, int pageSize,
            String sortField, String sortOrder) {

        LambdaQueryWrapper<School> wrapper = new LambdaQueryWrapper<>();

        if (StringUtils.hasText(keyword)) {
            wrapper.and(w -> w
                    .like(School::getName, keyword)
                    .or()
                    .like(School::getCode, keyword)
            );
        }

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
        // Fix: 问题4 - Boolean类型判断改为 true/false
        if (is985 != null && is985 == 1) {
            wrapper.eq(School::getIs985, true);
        }
        if (is211 != null && is211 == 1) {
            wrapper.eq(School::getIs211, true);
        }
        if (isDouble != null && isDouble == 1) {
            wrapper.eq(School::getIsDoubleFirstClass, true);
        }

        if ("ranking".equals(sortField)) {
            if ("asc".equals(sortOrder)) {
                wrapper.orderByAsc(School::getRanking);
            } else {
                wrapper.orderByDesc(School::getRanking);
            }
        } else {
            wrapper.orderByAsc(School::getId);
        }

        Page<School> page = new Page<>(pageNum, pageSize);
        Page<School> result = schoolMapper.selectPage(page, wrapper);

        List<SchoolVO> voList = result.getRecords().stream()
                .map(this::toSchoolVO)
                .collect(Collectors.toList());

        return PageResult.of(voList, result.getTotal(), pageNum, pageSize);
    }

    @Override
    public SchoolDetailVO getSchoolDetail(Long schoolId) {
        School school = schoolMapper.selectById(schoolId);
        if (school == null) {
            return null;
        }

        // 查询录取分数线
        LambdaQueryWrapper<AdmissionScore> scoreWrapper = new LambdaQueryWrapper<>();
        scoreWrapper.eq(AdmissionScore::getSchoolId, schoolId)
                .orderByDesc(AdmissionScore::getYear);
        List<AdmissionScore> scores = admissionScoreMapper.selectList(scoreWrapper);

        Map<String, List<Map<String, Object>>> scoreMap = scores.stream()
                .collect(Collectors.groupingBy(
                        s -> String.valueOf(s.getYear()),
                        Collectors.mapping(this::scoreToMap, Collectors.toList())
                ));

        // Fix: 问题1 - 通过school_major关联表查询该学校的专业
        List<Map<String, Object>> majorList = new ArrayList<>();
        try {
            LambdaQueryWrapper<SchoolMajor> smWrapper = new LambdaQueryWrapper<>();
            smWrapper.eq(SchoolMajor::getSchoolId, schoolId);
            List<SchoolMajor> schoolMajors = schoolMajorMapper.selectList(smWrapper);

            if (!schoolMajors.isEmpty()) {
                List<Long> majorIds = schoolMajors.stream()
                        .map(SchoolMajor::getMajorId)
                        .collect(Collectors.toList());

                LambdaQueryWrapper<Major> majorWrapper = new LambdaQueryWrapper<>();
                majorWrapper.in(Major::getId, majorIds)
                        .eq(Major::getStatus, 1)
                        .orderByAsc(Major::getCode);
                List<Major> majors = majorMapper.selectList(majorWrapper);

                majorList = majors.stream()
                        .map(this::majorToMap)
                        .collect(Collectors.toList());
            }
        } catch (Exception e) {
            log.warn("查询学校专业失败: schoolId={}", schoolId, e);
        }

        return SchoolDetailVO.builder()
                .id(school.getId())
                .name(school.getName())
                .code(school.getCode())
                .provinceId(school.getProvinceId())
                .provinceName(resolveProvinceName(school.getProvinceId()))
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

        // Fix: 问题2 - 使用QueryWrapper支持原生SQL分组统计
        // 按省份统计
        QueryWrapper<School> provinceWrapper = new QueryWrapper<>();
        provinceWrapper.select("province_id", "count(*) as count")
                .eq("deleted", 0)
                .groupBy("province_id");
        List<Map<String, Object>> byProvince = schoolMapper.selectMaps(provinceWrapper);

        // 补充省份名称
        Map<Integer, String> pMap = getProvinceNameMap();
        for (Map<String, Object> item : byProvince) {
            Object pidObj = item.get("province_id");
            if (pidObj != null) {
                Integer pid = Integer.parseInt(pidObj.toString());
                item.put("provinceName", pMap.getOrDefault(pid, "未知"));
            }
        }
        stats.put("byProvince", byProvince);

        // 按类型统计
        QueryWrapper<School> typeWrapper = new QueryWrapper<>();
        typeWrapper.select("type", "count(*) as count")
                .eq("deleted", 0)
                .groupBy("type");
        List<Map<String, Object>> byType = schoolMapper.selectMaps(typeWrapper);

        // 补充类型名称
        for (Map<String, Object> item : byType) {
            Object typeObj = item.get("type");
            if (typeObj != null) {
                Integer t = Integer.parseInt(typeObj.toString());
                item.put("typeName", TYPE_MAP.getOrDefault(t, "未知"));
            }
        }
        stats.put("byType", byType);

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
                .provinceName(resolveProvinceName(school.getProvinceId()))
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
