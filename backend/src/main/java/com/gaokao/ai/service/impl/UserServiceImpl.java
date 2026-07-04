package com.gaokao.ai.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.gaokao.ai.entity.User;
import com.gaokao.ai.mapper.UserMapper;
import com.gaokao.ai.service.UserService;
import com.gaokao.ai.utils.JwtUtils;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;

/**
 * 用户服务实现（简单版：用户名+密码）
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class UserServiceImpl implements UserService {

    private final UserMapper userMapper;
    private final JwtUtils jwtUtils;
    private final PasswordEncoder passwordEncoder;

    private static final Pattern USERNAME_PATTERN = Pattern.compile("^[a-zA-Z0-9_]{4,20}$");
    private static final Pattern PASSWORD_PATTERN = Pattern.compile("^.{6,20}$");

    @Override
    public Map<String, Object> register(String username, String password) {
        // 参数校验
        if (username == null || !USERNAME_PATTERN.matcher(username).matches()) {
            throw new IllegalArgumentException("用户名须为4-20位字母、数字或下划线");
        }
        if (password == null || !PASSWORD_PATTERN.matcher(password).matches()) {
            throw new IllegalArgumentException("密码长度须为6-20位");
        }

        // 检查用户名是否已存在
        if (existsByUsername(username)) {
            throw new IllegalArgumentException("用户名已存在");
        }

        // 创建用户
        User user = new User();
        user.setUsername(username);
        user.setPassword(passwordEncoder.encode(password));
        user.setStatus(1);
        user.setDeleted(0);
        userMapper.insert(user);

        // 生成Token
        String token = jwtUtils.generateToken(user.getId(), user.getUsername());

        log.info("用户注册成功: id={}, username={}", user.getId(), username);

        Map<String, Object> result = new HashMap<>();
        result.put("userId", user.getId());
        result.put("username", user.getUsername());
        result.put("token", token);
        return result;
    }

    @Override
    public Map<String, Object> login(String username, String password) {
        if (username == null || username.isEmpty()) {
            throw new IllegalArgumentException("用户名不能为空");
        }
        if (password == null || password.isEmpty()) {
            throw new IllegalArgumentException("密码不能为空");
        }

        // 查找用户
        LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(User::getUsername, username)
               .eq(User::getDeleted, 0);
        User user = userMapper.selectOne(wrapper);

        if (user == null) {
            throw new IllegalArgumentException("用户名或密码错误");
        }

        if (user.getStatus() != null && user.getStatus() == 0) {
            throw new IllegalArgumentException("账号已被禁用");
        }

        // 验证密码
        if (!passwordEncoder.matches(password, user.getPassword())) {
            throw new IllegalArgumentException("用户名或密码错误");
        }

        // 更新最后登录时间
        user.setLastLoginTime(LocalDateTime.now());
        userMapper.updateById(user);

        // 生成Token
        String token = jwtUtils.generateToken(user.getId(), user.getUsername());

        log.info("用户登录成功: id={}, username={}", user.getId(), username);

        Map<String, Object> result = new HashMap<>();
        result.put("userId", user.getId());
        result.put("username", user.getUsername());
        result.put("token", token);
        return result;
    }

    @Override
    public User getUserById(Long userId) {
        LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(User::getId, userId)
               .eq(User::getDeleted, 0);
        User user = userMapper.selectOne(wrapper);
        if (user != null) {
            user.setPassword(null);
        }
        return user;
    }

    @Override
    public User updateUser(Long userId, User updateUser) {
        User existing = userMapper.selectById(userId);
        if (existing == null) {
            throw new IllegalArgumentException("用户不存在");
        }

        if (updateUser.getRealName() != null) existing.setRealName(updateUser.getRealName());
        if (updateUser.getGender() != null) existing.setGender(updateUser.getGender());
        if (updateUser.getAvatar() != null) existing.setAvatar(updateUser.getAvatar());
        if (updateUser.getProvinceId() != null) existing.setProvinceId(updateUser.getProvinceId());
        if (updateUser.getCityId() != null) existing.setCityId(updateUser.getCityId());
        if (updateUser.getScore() != null) existing.setScore(updateUser.getScore());
        if (updateUser.getRanking() != null) existing.setRanking(updateUser.getRanking());
        if (updateUser.getSubjectType() != null) existing.setSubjectType(updateUser.getSubjectType());
        if (updateUser.getGraduationYear() != null) existing.setGraduationYear(updateUser.getGraduationYear());

        userMapper.updateById(existing);
        log.info("用户信息更新: id={}", userId);

        existing.setPassword(null);
        return existing;
    }

    @Override
    public boolean existsByUsername(String username) {
        LambdaQueryWrapper<User> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(User::getUsername, username)
               .eq(User::getDeleted, 0);
        return userMapper.selectCount(wrapper) > 0;
    }
}
