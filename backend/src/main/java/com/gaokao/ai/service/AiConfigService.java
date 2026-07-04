package com.gaokao.ai.service;

/**
 * AI配置服务接口
 * 管理AI API的配置（URL、Key、模型等）
 */
public interface AiConfigService {

    /**
     * 获取AI API地址
     */
    String getApiUrl();

    /**
     * 获取AI API Key
     */
    String getApiKey();

    /**
     * 获取AI模型名称
     */
    String getModel();

    /**
     * 获取系统提示词
     */
    String getSystemPrompt();

    /**
     * 更新AI配置
     */
    void updateConfig(String apiUrl, String apiKey, String model, String systemPrompt);

    /**
     * 检查AI配置是否完整
     */
    boolean isConfigured();
}
