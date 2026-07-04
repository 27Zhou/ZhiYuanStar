package com.gaokao.ai.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import java.util.Random;
import java.util.concurrent.TimeUnit;

/**
 * 邮箱验证码服务
 * 使用Redis存储验证码，5分钟过期
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class EmailService {

    private final StringRedisTemplate redisTemplate;

    private static final String CODE_PREFIX = "email:code:";
    private static final int CODE_LENGTH = 6;
    private static final int CODE_EXPIRE_MINUTES = 5;

    /**
     * 生成并存储验证码
     *
     * @param email 邮箱地址
     * @return 生成的验证码
     */
    public String sendVerificationCode(String email) {
        // 生成6位随机数字验证码
        String code = generateCode();

        // 存储到Redis，5分钟过期
        String key = CODE_PREFIX + email;
        redisTemplate.opsForValue().set(key, code, CODE_EXPIRE_MINUTES, TimeUnit.MINUTES);

        // TODO: 实际发送邮件（需要配置SMTP）
        // 目前只在日志中输出，方便测试
        log.info("=========================================");
        log.info("邮箱验证码: {} -> {}", email, code);
        log.info("有效期: {} 分钟", CODE_EXPIRE_MINUTES);
        log.info("=========================================");

        return code;
    }

    /**
     * 验证验证码
     *
     * @param email 邮箱地址
     * @param code  用户输入的验证码
     * @return 是否验证成功
     */
    public boolean verifyCode(String email, String code) {
        String key = CODE_PREFIX + email;
        String storedCode = redisTemplate.opsForValue().get(key);

        if (storedCode == null) {
            log.warn("验证码已过期或不存在: {}", email);
            return false;
        }

        if (storedCode.equals(code)) {
            // 验证成功，删除验证码
            redisTemplate.delete(key);
            log.info("验证码验证成功: {}", email);
            return true;
        }

        log.warn("验证码错误: {} (输入: {}, 正确: {})", email, code, storedCode);
        return false;
    }

    /**
     * 检查验证码是否存在（未过期）
     */
    public boolean hasPendingCode(String email) {
        String key = CODE_PREFIX + email;
        return redisTemplate.hasKey(key);
    }

    /**
     * 生成随机验证码
     */
    private String generateCode() {
        Random random = new Random();
        StringBuilder code = new StringBuilder();
        for (int i = 0; i < CODE_LENGTH; i++) {
            code.append(random.nextInt(10));
        }
        return code.toString();
    }
}
