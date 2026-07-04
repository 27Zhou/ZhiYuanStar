package com.gaokao.ai.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.gaokao.ai.entity.AssessmentQuestion;
import com.gaokao.ai.entity.AssessmentResult;
import com.gaokao.ai.entity.Major;
import com.gaokao.ai.mapper.AssessmentQuestionMapper;
import com.gaokao.ai.mapper.AssessmentResultMapper;
import com.gaokao.ai.mapper.MajorMapper;
import com.gaokao.ai.service.AssessmentService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.*;

/**
 * 心理测评服务实现
 * 12项能力维度测评 + 专业推荐
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AssessmentServiceImpl implements AssessmentService {

    private final AssessmentQuestionMapper questionMapper;
    private final AssessmentResultMapper resultMapper;
    private final MajorMapper majorMapper;

    // 12个能力维度
    private static final String[] DIMENSIONS = {
        "logic", "creativity", "communication", "leadership",
        "hands_on", "social", "artistic", "practical",
        "empathy", "innovation", "analysis", "execution"
    };

    // 选项得分映射
    private static final Map<String, int[]> OPTION_SCORES = Map.of(
        "A", new int[]{4, 3, 2, 1},
        "B", new int[]{3, 4, 1, 2},
        "C", new int[]{2, 1, 4, 3},
        "D", new int[]{1, 2, 3, 4}
    );

    // 能力维度到专业大类的映射
    private static final Map<String, List<String>> DIMENSION_MAJOR_MAP = Map.ofEntries(
        Map.entry("logic", List.of("工学", "理学")),
        Map.entry("creativity", List.of("艺术学", "文学")),
        Map.entry("communication", List.of("文学", "法学", "教育学")),
        Map.entry("leadership", List.of("管理学", "经济学")),
        Map.entry("hands_on", List.of("工学", "农学")),
        Map.entry("social", List.of("法学", "教育学", "管理学")),
        Map.entry("artistic", List.of("艺术学")),
        Map.entry("practical", List.of("工学", "管理学")),
        Map.entry("empathy", List.of("教育学", "医学")),
        Map.entry("innovation", List.of("工学", "理学")),
        Map.entry("analysis", List.of("理学", "经济学")),
        Map.entry("execution", List.of("管理学", "工学"))
    );

    @Override
    public List<AssessmentQuestion> getQuestions() {
        LambdaQueryWrapper<AssessmentQuestion> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(AssessmentQuestion::getStatus, 1)
               .orderByAsc(AssessmentQuestion::getSortOrder);
        return questionMapper.selectList(wrapper);
    }

    @Override
    public AssessmentResult submitAnswers(Map<Integer, String> answers) {
        log.info("收到测评答案，共 {} 题", answers.size());

        // 获取题目信息
        List<AssessmentQuestion> questions = getQuestions();
        Map<Integer, AssessmentQuestion> questionMap = new HashMap<>();
        for (AssessmentQuestion q : questions) {
            questionMap.put(q.getId(), q);
        }

        // 计算各维度得分
        Map<String, int[]> dimensionScores = new HashMap<>();
        for (String dim : DIMENSIONS) {
            dimensionScores.put(dim, new int[]{0, 0}); // [总分, 题数]
        }

        for (Map.Entry<Integer, String> entry : answers.entrySet()) {
            Integer questionId = entry.getKey();
            String answer = entry.getValue().toUpperCase();

            AssessmentQuestion question = questionMap.get(questionId);
            if (question == null || question.getDimension() == null) {
                continue;
            }

            String dimension = question.getDimension();
            int[] scores = dimensionScores.get(dimension);
            if (scores == null) {
                continue;
            }

            // 计算该题得分
            int[] optionScore = OPTION_SCORES.get(answer);
            if (optionScore != null) {
                // 取四个选项的平均分作为该维度的贡献
                int avgScore = (optionScore[0] + optionScore[1] + optionScore[2] + optionScore[3]) / 4;
                scores[0] += avgScore;
                scores[1] += 1;
            }
        }

        // 计算各维度最终得分（百分制）
        AssessmentResult result = new AssessmentResult();
        result.setLogicScore(calculateFinalScore(dimensionScores.get("logic")));
        result.setCreativityScore(calculateFinalScore(dimensionScores.get("creativity")));
        result.setCommunicationScore(calculateFinalScore(dimensionScores.get("communication")));
        result.setLeadershipScore(calculateFinalScore(dimensionScores.get("leadership")));
        result.setHandsOnScore(calculateFinalScore(dimensionScores.get("hands_on")));
        result.setSocialScore(calculateFinalScore(dimensionScores.get("social")));
        result.setArtisticScore(calculateFinalScore(dimensionScores.get("artistic")));
        result.setPracticalScore(calculateFinalScore(dimensionScores.get("practical")));
        result.setEmpathyScore(calculateFinalScore(dimensionScores.get("empathy")));
        result.setInnovationScore(calculateFinalScore(dimensionScores.get("innovation")));
        result.setAnalysisScore(calculateFinalScore(dimensionScores.get("analysis")));
        result.setExecutionScore(calculateFinalScore(dimensionScores.get("execution")));

        // 生成性格类型
        result.setPersonalityType(generatePersonalityType(result));

        // 生成推荐专业
        result.setRecommendedMajors(generateRecommendedMajors(result));

        // 生成详细报告
        result.setReport(generateReport(result));

        // 保存结果
        resultMapper.insert(result);
        log.info("测评结果已保存，ID: {}", result.getId());

        return result;
    }

    @Override
    public AssessmentResult getResult(Long resultId) {
        return resultMapper.selectById(resultId);
    }

    @Override
    public List<Map<String, Object>> getRecommendedMajors(Long resultId) {
        AssessmentResult result = resultMapper.selectById(resultId);
        if (result == null || result.getRecommendedMajors() == null) {
            return Collections.emptyList();
        }

        // 解析推荐的专业大类
        String[] categories = result.getRecommendedMajors().split(",");
        List<Map<String, Object>> majors = new ArrayList<>();

        for (String category : categories) {
            LambdaQueryWrapper<Major> wrapper = new LambdaQueryWrapper<>();
            wrapper.eq(Major::getCategory, category.trim())
                   .eq(Major::getStatus, 1)
                   .orderByAsc(Major::getCode);
            List<Major> majorList = majorMapper.selectList(wrapper);

            for (Major m : majorList) {
                Map<String, Object> map = new HashMap<>();
                map.put("id", m.getId());
                map.put("name", m.getName());
                map.put("code", m.getCode());
                map.put("category", m.getCategory());
                map.put("duration", m.getDuration());
                map.put("degree", m.getDegree());
                majors.add(map);
            }
        }

        return majors;
    }

    /**
     * 计算最终得分（百分制）
     */
    private int calculateFinalScore(int[] scores) {
        if (scores[1] == 0) return 50;
        int avg = scores[0] / scores[1];
        return Math.min(100, Math.max(0, avg * 25));
    }

    /**
     * 生成性格类型描述
     */
    private String generatePersonalityType(AssessmentResult result) {
        // 找出得分最高的3个维度
        Map<String, Integer> scores = new LinkedHashMap<>();
        scores.put("逻辑思维", result.getLogicScore());
        scores.put("创造能力", result.getCreativityScore());
        scores.put("沟通能力", result.getCommunicationScore());
        scores.put("领导能力", result.getLeadershipScore());
        scores.put("动手能力", result.getHandsOnScore());
        scores.put("社交能力", result.getSocialScore());
        scores.put("艺术感知", result.getArtisticScore());
        scores.put("实践能力", result.getPracticalScore());
        scores.put("共情能力", result.getEmpathyScore());
        scores.put("创新能力", result.getInnovationScore());
        scores.put("分析能力", result.getAnalysisScore());
        scores.put("执行能力", result.getExecutionScore());

        // 排序
        List<Map.Entry<String, Integer>> sorted = new ArrayList<>(scores.entrySet());
        sorted.sort((a, b) -> b.getValue().compareTo(a.getValue()));

        StringBuilder type = new StringBuilder();
        type.append("你的核心能力是");
        type.append(sorted.get(0).getKey());
        type.append("、");
        type.append(sorted.get(1).getKey());
        type.append("和");
        type.append(sorted.get(2).getKey());
        type.append("。");

        // 根据能力组合给出性格描述
        String top1 = sorted.get(0).getKey();
        String top2 = sorted.get(1).getKey();

        if ("逻辑思维".equals(top1) && "分析能力".equals(top2)) {
            type.append("你是一个理性分析型人才，善于用数据和逻辑解决问题。");
        } else if ("创造能力".equals(top1) && "艺术感知".equals(top2)) {
            type.append("你是一个创意艺术型人才，有很强的审美和创新能力。");
        } else if ("沟通能力".equals(top1) && "社交能力".equals(top2)) {
            type.append("你是一个社交沟通型人才，善于与人打交道。");
        } else if ("领导能力".equals(top1) && "执行能力".equals(top2)) {
            type.append("你是一个领导管理型人才，有很强的组织和执行力。");
        } else if ("动手能力".equals(top1) && "实践能力".equals(top2)) {
            type.append("你是一个动手实践型人才，适合做技术类工作。");
        } else if ("共情能力".equals(top1) && "沟通能力".equals(top2)) {
            type.append("你是一个关怀服务型人才，适合做教育、医疗类工作。");
        } else if ("创新能力".equals(top1) && "逻辑思维".equals(top2)) {
            type.append("你是一个创新研究型人才，适合做科研、开发类工作。");
        } else {
            type.append("你是一个多面手型人才，能力均衡发展。");
        }

        return type.toString();
    }

    /**
     * 生成推荐专业大类
     */
    private String generateRecommendedMajors(AssessmentResult result) {
        // 找出得分最高的3个维度
        Map<String, Integer> dimScores = new LinkedHashMap<>();
        dimScores.put("logic", result.getLogicScore());
        dimScores.put("creativity", result.getCreativityScore());
        dimScores.put("communication", result.getCommunicationScore());
        dimScores.put("leadership", result.getLeadershipScore());
        dimScores.put("hands_on", result.getHandsOnScore());
        dimScores.put("social", result.getSocialScore());
        dimScores.put("artistic", result.getArtisticScore());
        dimScores.put("practical", result.getPracticalScore());
        dimScores.put("empathy", result.getEmpathyScore());
        dimScores.put("innovation", result.getInnovationScore());
        dimScores.put("analysis", result.getAnalysisScore());
        dimScores.put("execution", result.getExecutionScore());

        // 排序
        List<Map.Entry<String, Integer>> sorted = new ArrayList<>(dimScores.entrySet());
        sorted.sort((a, b) -> b.getValue().compareTo(a.getValue()));

        // 取前3个维度对应的专业大类
        Set<String> categories = new LinkedHashSet<>();
        for (int i = 0; i < 3 && i < sorted.size(); i++) {
            String dim = sorted.get(i).getKey();
            List<String> cats = DIMENSION_MAJOR_MAP.get(dim);
            if (cats != null) {
                categories.addAll(cats);
            }
        }

        return String.join(",", categories);
    }

    /**
     * 生成详细报告
     */
    private String generateReport(AssessmentResult result) {
        StringBuilder report = new StringBuilder();

        report.append("# 🧠 你的个人发展能力图谱\n\n");

        report.append("## 核心能力\n");
        report.append("| 能力维度 | 得分 | 等级 |\n");
        report.append("|---------|------|------|\n");

        appendScoreRow(report, "逻辑思维", result.getLogicScore());
        appendScoreRow(report, "创造能力", result.getCreativityScore());
        appendScoreRow(report, "沟通能力", result.getCommunicationScore());
        appendScoreRow(report, "领导能力", result.getLeadershipScore());
        appendScoreRow(report, "动手能力", result.getHandsOnScore());
        appendScoreRow(report, "社交能力", result.getSocialScore());
        appendScoreRow(report, "艺术感知", result.getArtisticScore());
        appendScoreRow(report, "实践能力", result.getPracticalScore());
        appendScoreRow(report, "共情能力", result.getEmpathyScore());
        appendScoreRow(report, "创新能力", result.getInnovationScore());
        appendScoreRow(report, "分析能力", result.getAnalysisScore());
        appendScoreRow(report, "执行能力", result.getExecutionScore());

        report.append("\n## 性格分析\n");
        report.append(result.getPersonalityType()).append("\n");

        report.append("\n## 推荐专业方向\n");
        String[] categories = result.getRecommendedMajors().split(",");
        for (String cat : categories) {
            report.append("- ").append(cat).append("\n");
        }

        report.append("\n## 建议\n");
        report.append("根据你的能力图谱，建议在选择专业时优先考虑以上方向。");
        report.append("同时也要结合自己的兴趣、分数和就业前景综合考虑。");

        return report.toString();
    }

    /**
     * 追加得分行
     */
    private void appendScoreRow(StringBuilder report, String name, int score) {
        String level;
        if (score >= 80) level = "⭐⭐⭐⭐⭐ 优秀";
        else if (score >= 60) level = "⭐⭐⭐⭐ 良好";
        else if (score >= 40) level = "⭐⭐⭐ 中等";
        else if (score >= 20) level = "⭐⭐ 较弱";
        else level = "⭐ 待提升";

        report.append("| ").append(name).append(" | ").append(score).append(" | ").append(level).append(" |\n");
    }
}
