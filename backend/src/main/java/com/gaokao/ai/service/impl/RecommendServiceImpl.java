package com.gaokao.ai.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.gaokao.ai.entity.AdmissionScore;
import com.gaokao.ai.entity.School;
import com.gaokao.ai.mapper.AdmissionScoreMapper;
import com.gaokao.ai.mapper.SchoolMapper;
import com.gaokao.ai.service.RecommendService;
import com.gaokao.ai.vo.RecommendVO;
import com.gaokao.ai.vo.RecommendVO.RecommendSchool;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

/**
 * 推荐服务实现
 *
 * 算法说明：
 * - 高分段（排名前30%）：使用位次法，根据位次对比历年录取位次
 * - 低分段（排名后70%）：使用线差法，根据分数与分数线的差值
 *
 * 三档推荐：
 * - 冲刺：录取概率 20-40%
 * - 稳妥：录取概率 50-80%
 * - 保底：录取概率 80-99%
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class RecommendServiceImpl implements RecommendService {

    private final SchoolMapper schoolMapper;
    private final AdmissionScoreMapper admissionScoreMapper;

    // 位次法阈值（前30%使用位次法）
    private static final double RANKING_THRESHOLD = 0.3;

    @Override
    public RecommendVO recommend(int score, Integer ranking, Integer provinceId, Integer subjectType) {
        log.info("推荐请求: score={}, ranking={}, provinceId={}, subjectType={}", score, ranking, provinceId, subjectType);

        // 获取该省份该科类的所有录取数据
        LambdaQueryWrapper<AdmissionScore> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(AdmissionScore::getProvinceId, provinceId)
               .eq(AdmissionScore::getSubjectType, subjectType)
               .eq(AdmissionScore::getYear, 2024)  // 只用最新年份数据
               .isNotNull(AdmissionScore::getMinScore);
        List<AdmissionScore> scores = admissionScoreMapper.selectList(wrapper);

        if (scores.isEmpty()) {
            // 如果2024年没有数据，尝试2023年
            wrapper = new LambdaQueryWrapper<>();
            wrapper.eq(AdmissionScore::getProvinceId, provinceId)
                   .eq(AdmissionScore::getSubjectType, subjectType)
                   .eq(AdmissionScore::getYear, 2023)
                   .isNotNull(AdmissionScore::getMinScore);
            scores = admissionScoreMapper.selectList(wrapper);
        }

        if (scores.isEmpty()) {
            log.warn("无录取数据可参考");
            return RecommendVO.builder()
                    .score(score)
                    .ranking(ranking)
                    .rush(Collections.emptyList())
                    .stable(Collections.emptyList())
                    .safe(Collections.emptyList())
                    .build();
        }

        // 按学校分组，取每个学校的最低分和最低位次
        Map<Long, AdmissionScore> schoolScoreMap = new HashMap<>();
        for (AdmissionScore s : scores) {
            schoolScoreMap.merge(s.getSchoolId(), s, (a, b) -> {
                if (a.getMinScore() != null && b.getMinScore() != null) {
                    return a.getMinScore() <= b.getMinScore() ? a : b;
                }
                return a;
            });
        }

        // 获取学校信息
        Set<Long> schoolIds = schoolScoreMap.keySet();
        LambdaQueryWrapper<School> schoolWrapper = new LambdaQueryWrapper<>();
        schoolWrapper.in(School::getId, schoolIds);
        Map<Long, School> schoolMap = schoolMapper.selectList(schoolWrapper)
                .stream()
                .collect(Collectors.toMap(School::getId, s -> s));

        // 判断使用哪种算法
        boolean useRanking = false;
        if (ranking != null && ranking > 0) {
            // 如果有位次信息，判断是否属于高分段
            int totalStudents = 500000; // 假设全省50万考生
            useRanking = (double) ranking / totalStudents <= RANKING_THRESHOLD;
        }

        String algorithm = useRanking ? "ranking" : "score_diff";
        log.info("使用算法: {}", algorithm);

        // 计算推荐结果
        List<RecommendSchool> rushList = new ArrayList<>();
        List<RecommendSchool> stableList = new ArrayList<>();
        List<RecommendSchool> safeList = new ArrayList<>();

        for (Map.Entry<Long, AdmissionScore> entry : schoolScoreMap.entrySet()) {
            Long schoolId = entry.getKey();
            AdmissionScore admissionScore = entry.getValue();
            School school = schoolMap.get(schoolId);

            if (school == null || admissionScore.getMinScore() == null) {
                continue;
            }

            Integer minScore = admissionScore.getMinScore();
            Integer minRanking = admissionScore.getMinRanking();

            // 计算分数差和位次差
            int scoreDiff = score - minScore;
            Integer rankingDiff = null;
            if (ranking != null && minRanking != null) {
                rankingDiff = minRanking - ranking; // 正数表示用户排名更靠前
            }

            // 计算录取概率和推荐档位
            int probability;
            String tier;

            if (useRanking && rankingDiff != null) {
                // 位次法
                probability = calculateProbabilityByRanking(rankingDiff, minRanking);
            } else {
                // 线差法
                probability = calculateProbabilityByScoreDiff(scoreDiff);
            }

            // 分档
            if (probability >= 20 && probability < 50) {
                tier = "rush"; // 冲刺
            } else if (probability >= 50 && probability < 80) {
                tier = "stable"; // 稳妥
            } else if (probability >= 80) {
                tier = "safe"; // 保底
            } else {
                continue; // 概率太低或太高，不推荐
            }

            // 构建推荐学校
            RecommendSchool recommendSchool = RecommendSchool.builder()
                    .id(school.getId())
                    .name(school.getName())
                    .code(school.getCode())
                    .typeName(getTypeName(school.getType()))
                    .is985(school.getIs985())
                    .is211(school.getIs211())
                    .isDoubleFirstClass(school.getIsDoubleFirstClass())
                    .minScore(minScore)
                    .minRanking(minRanking)
                    .scoreDiff(scoreDiff)
                    .rankingDiff(rankingDiff)
                    .probability(probability)
                    .reason(generateReason(school, scoreDiff, rankingDiff, probability, useRanking))
                    .build();

            // 分档
            switch (tier) {
                case "rush":
                    rushList.add(recommendSchool);
                    break;
                case "stable":
                    stableList.add(recommendSchool);
                    break;
                case "safe":
                    safeList.add(recommendSchool);
                    break;
            }
        }

        // 排序：冲刺按概率降序，稳妥按概率升序，保底按概率降序
        rushList.sort((a, b) -> b.getProbability().compareTo(a.getProbability()));
        stableList.sort((a, b) -> a.getProbability().compareTo(b.getProbability()));
        safeList.sort((a, b) -> b.getProbability().compareTo(a.getProbability()));

        // 限制每档数量
        rushList = rushList.stream().limit(10).collect(Collectors.toList());
        stableList = stableList.stream().limit(10).collect(Collectors.toList());
        safeList = safeList.stream().limit(10).collect(Collectors.toList());

        log.info("推荐完成: 冲刺={}, 稳妥={}, 保底={}", rushList.size(), stableList.size(), safeList.size());

        return RecommendVO.builder()
                .score(score)
                .ranking(ranking)
                .algorithm(algorithm)
                .rush(rushList)
                .stable(stableList)
                .safe(safeList)
                .build();
    }

    /**
     * 位次法计算录取概率
     */
    private int calculateProbabilityByRanking(int rankingDiff, int minRanking) {
        // rankingDiff = minRanking - userRanking
        // 正数表示用户排名更靠前（更有优势）
        if (minRanking <= 0) return 50;

        double ratio = (double) rankingDiff / minRanking;

        if (ratio > 0.5) return 95;       // 远超
        if (ratio > 0.3) return 85;       // 大幅领先
        if (ratio > 0.1) return 70;       // 略有优势
        if (ratio > -0.1) return 50;      // 接近
        if (ratio > -0.3) return 35;      // 略有差距
        if (ratio > -0.5) return 25;      // 差距较大
        return 15;                         // 差距很大
    }

    /**
     * 线差法计算录取概率
     */
    private int calculateProbabilityByScoreDiff(int scoreDiff) {
        // scoreDiff = userScore - minScore
        // 正数表示用户分数高于录取线
        if (scoreDiff > 50) return 95;
        if (scoreDiff > 30) return 85;
        if (scoreDiff > 15) return 70;
        if (scoreDiff > 5) return 55;
        if (scoreDiff > -5) return 45;
        if (scoreDiff > -15) return 35;
        if (scoreDiff > -30) return 25;
        return 15;
    }

    /**
     * 生成推荐理由
     */
    private String generateReason(School school, int scoreDiff, Integer rankingDiff, int probability, boolean useRanking) {
        StringBuilder sb = new StringBuilder();

        if (school.getIs985() != null && school.getIs985()) {
            sb.append("985高校，");
        } else if (school.getIs211() != null && school.getIs211()) {
            sb.append("211高校，");
        } else if (school.getIsDoubleFirstClass() != null && school.getIsDoubleFirstClass()) {
            sb.append("双一流高校，");
        }

        if (useRanking && rankingDiff != null) {
            if (rankingDiff > 0) {
                sb.append("您的位次高于历年录取位次").append(Math.abs(rankingDiff)).append("位，");
            } else {
                sb.append("您的位次低于历年录取位次").append(Math.abs(rankingDiff)).append("位，");
            }
        } else {
            if (scoreDiff > 0) {
                sb.append("您的分数高于历年最低分").append(scoreDiff).append("分，");
            } else {
                sb.append("您的分数低于历年最低分").append(Math.abs(scoreDiff)).append("分，");
            }
        }

        if (probability >= 80) {
            sb.append("录取概率较大，建议作为保底志愿");
        } else if (probability >= 50) {
            sb.append("录取概率适中，建议作为稳妥志愿");
        } else {
            sb.append("有一定风险，建议作为冲刺志愿");
        }

        return sb.toString();
    }

    /**
     * 获取学校类型名称
     */
    private String getTypeName(Integer type) {
        if (type == null) return "未知";
        Map<Integer, String> typeMap = Map.ofEntries(
                Map.entry(1, "综合"), Map.entry(2, "理工"), Map.entry(3, "师范"),
                Map.entry(4, "医药"), Map.entry(5, "财经"), Map.entry(6, "政法"),
                Map.entry(7, "农林"), Map.entry(8, "艺术"), Map.entry(9, "体育"),
                Map.entry(10, "民族"), Map.entry(11, "军事")
        );
        return typeMap.getOrDefault(type, "未知");
    }
}
