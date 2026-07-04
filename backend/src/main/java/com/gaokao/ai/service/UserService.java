package com.gaokao.ai.service;

import com.gaokao.ai.entity.User;

import java.util.Map;

/**
 * 用户服务接口（简单版：用户名+密码）
 */
public interface UserService {

    /**
     * 用户注册
     */
    Map<String, Object> register(String username, String password);

    /**
     * 用户登录
     */
    Map<String, Object> login(String username, String password);

    /**
     * 获取用户信息
     */
    User getUserById(Long userId);

    /**
     * 更新用户信息
     */
    User updateUser(Long userId, User user);

    /**
     * 检查用户名是否已存在
     */
    boolean existsByUsername(String username);
}
