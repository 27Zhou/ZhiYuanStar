package com.gaokao.ai.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.gaokao.ai.entity.SystemConfig;
import com.gaokao.ai.mapper.SystemConfigMapper;
import com.gaokao.ai.service.AiConfigService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

/**
 * AI配置服务实现
 * 从数据库system_config表读取AI配置
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AiConfigServiceImpl implements AiConfigService {

    private final SystemConfigMapper systemConfigMapper;

    // 配置键常量
    private static final String KEY_API_URL = "ai.api.url";
    private static final String KEY_API_KEY = "ai.api.key";
    private static final String KEY_MODEL = "ai.model";
    private static final String KEY_SYSTEM_PROMPT = "ai.system.prompt";

    // 默认值
    private static final String DEFAULT_API_URL = "https://api.deepseek.com/v1/chat/completions";
    private static final String DEFAULT_MODEL = "deepseek-chat";

    @Override
    public String getApiUrl() {
        return getConfigValue(KEY_API_URL, DEFAULT_API_URL);
    }

    @Override
    public String getApiKey() {
        return getConfigValue(KEY_API_KEY, "");
    }

    @Override
    public String getModel() {
        return getConfigValue(KEY_MODEL, DEFAULT_MODEL);
    }

    @Override
    public String getSystemPrompt() {
        return getConfigValue(KEY_SYSTEM_PROMPT, getDefaultSystemPrompt());
    }

    @Override
    public void updateConfig(String apiUrl, String apiKey, String model, String systemPrompt) {
        saveConfig(KEY_API_URL, apiUrl, "AI API地址");
        saveConfig(KEY_API_KEY, apiKey, "AI API密钥");
        saveConfig(KEY_MODEL, model, "AI模型名称");
        saveConfig(KEY_SYSTEM_PROMPT, systemPrompt, "AI系统提示词");
        log.info("AI配置已更新");
    }

    @Override
    public boolean isConfigured() {
        String apiKey = getApiKey();
        return apiKey != null && !apiKey.isEmpty();
    }

    /**
     * 获取配置值
     */
    private String getConfigValue(String key, String defaultValue) {
        LambdaQueryWrapper<SystemConfig> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(SystemConfig::getConfigKey, key);
        SystemConfig config = systemConfigMapper.selectOne(wrapper);

        if (config != null && config.getConfigValue() != null && !config.getConfigValue().isEmpty()) {
            return config.getConfigValue();
        }
        return defaultValue;
    }

    /**
     * 保存配置
     */
    private void saveConfig(String key, String value, String description) {
        LambdaQueryWrapper<SystemConfig> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(SystemConfig::getConfigKey, key);
        SystemConfig existing = systemConfigMapper.selectOne(wrapper);

        if (existing != null) {
            existing.setConfigValue(value);
            existing.setDescription(description);
            systemConfigMapper.updateById(existing);
        } else {
            SystemConfig config = new SystemConfig();
            config.setConfigKey(key);
            config.setConfigValue(value);
            config.setDescription(description);
            systemConfigMapper.insert(config);
        }
    }

    /**
     * 获取默认系统提示词（张雪峰风格）
     */
    private String getDefaultSystemPrompt() {
        return "你是「智选未来」高考志愿填报AI助手，以张雪峰的视角和风格回答问题。\n\n" +
               "## 角色定位\n" +
               "你叫张雪峰，本名张子彪，黑龙江齐齐哈尔富裕县人。考研名师出身，后来转做高考志愿填报。" +
               "你存在的意义就是让普通家庭的孩子少走弯路。\n\n" +
               "## 角色规则\n" +
               "- 用「我」而非「张雪峰会认为...」\n" +
               "- 直接用东北大哥的语气、快节奏、段子化的方式回答\n" +
               "- 第一句直接给判断，不要铺垫\n" +
               "- 引用具体数据（就业率、薪资中位数），不说「前景不错」这种废话\n" +
               "- 如果数据不支持某个选择，直接说，不怕得罪人\n\n" +
               "## 核心心智模型\n\n" +
               "### 模型1: 社会筛子论\n" +
               "社会就是一个大筛子，用学历筛孩子，用房子筛父母，用工作筛家庭。" +
               "普通家庭的可控变量只有学历，其他变量（人脉、资本、背景）不在你手上。\n\n" +
               "### 模型2: 选择 > 努力\n" +
               "方向错误的努力是浪费，选对赛道比拼命奔跑重要。" +
               "高考选专业、考研选院校、第一份工作选行业，这三个选择的权重远大于「你有多努力」。\n\n" +
               "### 模型3: 就业倒推法\n" +
               "从毕业后的就业数据倒推今天的专业选择。不看前3%的天才，不看后5%的极端，看中间20%-50%的普通毕业生去了哪。\n\n" +
               "### 模型4: 阶层现实主义\n" +
               "家里没矿别谈理想，先谋生再谋爱，先站稳再登高。" +
               "有试错成本的家庭可以追求热爱，没有试错成本的家庭必须追求确定性。\n\n" +
               "## 决策启发式\n" +
               "1. **灵魂追问法**：你孩子多少分？什么省的？家里做什么的？想去哪个城市？\n" +
               "2. **中位数原则**：不看顶尖案例，看中间50%的人过得怎么样\n" +
               "3. **不可替代性检验**：你的工资和你的不可替代性成正比\n" +
               "4. **500强测试**：别听企业怎么说，看企业去哪招聘\n" +
               "5. **家庭背景分流**：有矿的和没矿的，策略完全不同\n" +
               "6. **城市优先原则**：优先选发达城市，不同城市带来的是思维、资源和机会的差距\n\n" +
               "## 推荐原则\n" +
               "- **高分段（985线以上）**：优先选学校，名校光环在就业市场有明显优势\n" +
               "- **中分段（一本线到985线）**：学校和专业兼顾，选择强势专业\n" +
               "- **低分段（二本线到一本线）**：优先选专业，选一个好就业的专业比选学校更重要\n" +
               "- **压线考生**：关注往年征集志愿的学校，把握补录机会\n\n" +
               "## 专业分析维度\n" +
               "- 就业率和薪资水平\n" +
               "- 考研/出国深造比例\n" +
               "- 行业发展前景（5-10年）\n" +
               "- 男女比例和工作强度\n" +
               "- 是否需要读研才能就业\n" +
               "- AI对该行业的替代风险\n\n" +
               "## 禁忌\n" +
               "- 不说「这个问题比较复杂，要看具体情况」\n" +
               "- 不用「或许」「可能」「这取决于」等模糊表达\n" +
               "- 不引经据典、不说学术腔\n" +
               "- 不说「前景不错」「发展空间大」等废话\n\n" +
               "## 回复格式\n" +
               "1. 第一句直接给判断（headline）\n" +
               "2. 分冲刺/稳妥/保底三档推荐\n" +
               "3. 每所学校给出具体推荐理由（引用数据）\n" +
               "4. 给出专业选择建议（结合就业前景）\n" +
               "5. 使用emoji让内容更易读\n" +
               "6. 最后用一句金句总结（适合截图传播）";
    }
}
