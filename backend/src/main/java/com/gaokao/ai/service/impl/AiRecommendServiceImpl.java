package com.gaokao.ai.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.gaokao.ai.entity.AdmissionScore;
import com.gaokao.ai.entity.School;
import com.gaokao.ai.mapper.AdmissionScoreMapper;
import com.gaokao.ai.mapper.SchoolMapper;
import com.gaokao.ai.service.AiConfigService;
import com.gaokao.ai.service.AiRecommendService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.*;

/**
 * AI推荐服务实现
 * 调用可配置的大模型API（DeepSeek/ChatGPT/其他）
 * 采用张雪峰风格的提示词
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AiRecommendServiceImpl implements AiRecommendService {

    private final AiConfigService aiConfigService;
    private final SchoolMapper schoolMapper;
    private final AdmissionScoreMapper admissionScoreMapper;
    private final RestTemplate restTemplate;

    @Override
    public Map<String, Object> aiRecommend(int score, Integer ranking, Integer provinceId, Integer subjectType, String interests) {
        log.info("AI推荐请求: score={}, ranking={}, provinceId={}, subjectType={}, interests={}",
                score, ranking, provinceId, subjectType, interests);

        // 1. 从数据库检索匹配的学校数据
        String schoolData = retrieveSchoolData(score, provinceId, subjectType);

        // 2. 构建用户提示词
        String userPrompt = buildUserPrompt(score, ranking, provinceId, subjectType, interests, schoolData);

        // 3. 调用AI API
        String aiResponse = callAiApi(userPrompt);

        // 4. 返回结果
        Map<String, Object> result = new HashMap<>();
        result.put("score", score);
        result.put("ranking", ranking);
        result.put("aiResponse", aiResponse);
        result.put("dataUsed", schoolData);

        return result;
    }

    @Override
    public String chat(String message) {
        return callAiApi(message);
    }

    /**
     * 从数据库检索匹配的学校数据
     */
    private String retrieveSchoolData(int score, Integer provinceId, Integer subjectType) {
        // 查询该省份该科类的录取数据（分数在用户分数±50分范围内）
        LambdaQueryWrapper<AdmissionScore> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(AdmissionScore::getProvinceId, provinceId)
               .eq(AdmissionScore::getSubjectType, subjectType)
               .eq(AdmissionScore::getYear, 2024)
               .between(AdmissionScore::getMinScore, score - 80, score + 30)
               .isNotNull(AdmissionScore::getMinScore)
               .orderByAsc(AdmissionScore::getMinScore);
        List<AdmissionScore> scores = admissionScoreMapper.selectList(wrapper);

        if (scores.isEmpty()) {
            // 尝试2023年
            wrapper = new LambdaQueryWrapper<>();
            wrapper.eq(AdmissionScore::getProvinceId, provinceId)
                   .eq(AdmissionScore::getSubjectType, subjectType)
                   .eq(AdmissionScore::getYear, 2023)
                   .between(AdmissionScore::getMinScore, score - 80, score + 30)
                   .isNotNull(AdmissionScore::getMinScore)
                   .orderByAsc(AdmissionScore::getMinScore);
            scores = admissionScoreMapper.selectList(wrapper);
        }

        if (scores.isEmpty()) {
            return "暂无该省份的录取数据";
        }

        // 获取学校信息
        Set<Long> schoolIds = new HashSet<>();
        for (AdmissionScore s : scores) {
            schoolIds.add(s.getSchoolId());
        }

        LambdaQueryWrapper<School> schoolWrapper = new LambdaQueryWrapper<>();
        schoolWrapper.in(School::getId, schoolIds);
        List<School> schools = schoolMapper.selectList(schoolWrapper);
        Map<Long, School> schoolMap = new HashMap<>();
        for (School s : schools) {
            schoolMap.put(s.getId(), s);
        }

        // 构建数据摘要
        StringBuilder sb = new StringBuilder();
        sb.append("【").append(score).append("分可报考的学校数据】\n");

        for (AdmissionScore s : scores) {
            School school = schoolMap.get(s.getSchoolId());
            if (school == null) continue;

            sb.append("- ").append(school.getName());
            if (school.getIs985() != null && school.getIs985()) sb.append(" [985]");
            if (school.getIs211() != null && school.getIs211()) sb.append(" [211]");
            if (school.getIsDoubleFirstClass() != null && school.getIsDoubleFirstClass()) sb.append(" [双一流]");
            sb.append(" | 最低分:").append(s.getMinScore());
            if (s.getMinRanking() != null) sb.append(" | 最低位次:").append(s.getMinRanking());
            sb.append(" | 分差:").append(score - s.getMinScore()).append("分");
            sb.append("\n");
        }

        return sb.toString();
    }

    /**
     * 构建用户提示词
     */
    private String buildUserPrompt(int score, Integer ranking, Integer provinceId, Integer subjectType,
                                    String interests, String schoolData) {
        StringBuilder sb = new StringBuilder();

        sb.append("请根据以下信息，为我推荐高考志愿填报方案：\n\n");

        sb.append("## 我的基本信息\n");
        sb.append("- 分数：").append(score).append("分\n");
        if (ranking != null) {
            sb.append("- 位次：第").append(ranking).append("名\n");
        }
        sb.append("- 省份ID：").append(provinceId).append("\n");
        sb.append("- 科类：").append(subjectType == 1 ? "文科" : subjectType == 2 ? "理科" : "综合改革").append("\n");

        if (interests != null && !interests.isEmpty()) {
            sb.append("- 兴趣/偏好：").append(interests).append("\n");
        }

        sb.append("\n## 参考数据\n");
        sb.append(schoolData);

        sb.append("\n## 请按以下格式回复\n");
        sb.append("1. 🎯 总体建议（2-3句话概括）\n");
        sb.append("2. 🚀 冲刺院校（3-5所，附推荐理由）\n");
        sb.append("3. ✅ 稳妥院校（3-5所，附推荐理由）\n");
        sb.append("4. 🛡️ 保底院校（3-5所，附推荐理由）\n");
        sb.append("5. 💡 专业选择建议（结合就业前景）\n");
        sb.append("6. ⚠️ 填报注意事项\n");

        return sb.toString();
    }

    /**
     * 调用AI API
     */
    private String callAiApi(String userPrompt) {
        String apiUrl = aiConfigService.getApiUrl();
        String apiKey = aiConfigService.getApiKey();
        String model = aiConfigService.getModel();
        String systemPrompt = aiConfigService.getSystemPrompt();

        // 检查配置
        if (apiKey == null || apiKey.isEmpty()) {
            log.warn("AI API Key未配置");
            return "⚠️ AI服务未配置，请在系统设置中配置AI API Key。\n\n" +
                   "配置路径：系统设置 → AI配置 → 填写API地址和密钥";
        }

        try {
            // 构建请求体
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("model", model);
            requestBody.put("temperature", 0.7);
            requestBody.put("max_tokens", 2000);

            // 构建消息列表
            List<Map<String, String>> messages = new ArrayList<>();

            // 系统提示词
            Map<String, String> systemMessage = new HashMap<>();
            systemMessage.put("role", "system");
            systemMessage.put("content", systemPrompt);
            messages.add(systemMessage);

            // 用户消息
            Map<String, String> userMessage = new HashMap<>();
            userMessage.put("role", "user");
            userMessage.put("content", userPrompt);
            messages.add(userMessage);

            requestBody.put("messages", messages);

            // 设置请求头
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.setBearerAuth(apiKey);

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

            // 发送请求
            log.info("调用AI API: {}", apiUrl);
            ResponseEntity<Map> response = restTemplate.exchange(apiUrl, HttpMethod.POST, entity, Map.class);

            if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
                Map<String, Object> body = response.getBody();
                List<Map<String, Object>> choices = (List<Map<String, Object>>) body.get("choices");
                if (choices != null && !choices.isEmpty()) {
                    Map<String, Object> message = (Map<String, Object>) choices.get(0).get("message");
                    if (message != null) {
                        String content = (String) message.get("content");
                        log.info("AI响应成功，长度: {}", content.length());
                        return content;
                    }
                }
            }

            log.error("AI响应格式异常: {}", response.getBody());
            return "⚠️ AI响应格式异常，请检查API配置";

        } catch (Exception e) {
            log.error("调用AI API失败: {}", e.getMessage());
            return "⚠️ AI服务调用失败：" + e.getMessage() + "\n\n请检查API地址和密钥是否正确。";
        }
    }
}
