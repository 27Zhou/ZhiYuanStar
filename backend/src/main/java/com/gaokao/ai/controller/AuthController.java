package com.gaokao.ai.controller;

import com.gaokao.ai.common.Result;
import com.gaokao.ai.entity.User;
import com.gaokao.ai.service.UserService;
import com.gaokao.ai.utils.JwtUtils;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 认证控制器（简单版：用户名+密码）
 */
@Slf4j
@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
@Tag(name = "用户认证", description = "注册、登录、个人信息")
public class AuthController {

    private final UserService userService;
    private final JwtUtils jwtUtils;

    @PostMapping("/register")
    @Operation(summary = "用户注册", description = "用户名+密码注册")
    public Result<Map<String, Object>> register(@RequestBody Map<String, String> request) {
        try {
            String username = request.get("username");
            String password = request.get("password");

            Map<String, Object> result = userService.register(username, password);
            return Result.success(result);
        } catch (IllegalArgumentException e) {
            return Result.error(400, e.getMessage());
        }
    }

    @PostMapping("/login")
    @Operation(summary = "用户登录", description = "用户名+密码登录，返回JWT Token")
    public Result<Map<String, Object>> login(@RequestBody Map<String, String> request) {
        try {
            String username = request.get("username");
            String password = request.get("password");

            Map<String, Object> result = userService.login(username, password);
            return Result.success(result);
        } catch (IllegalArgumentException e) {
            return Result.error(400, e.getMessage());
        }
    }

    @GetMapping("/me")
    @Operation(summary = "获取当前用户信息", description = "需要在Header中传入Authorization: Bearer {token}")
    public Result<User> getCurrentUser(@RequestHeader(value = "Authorization", required = false) String authHeader) {
        try {
            String token = jwtUtils.extractToken(authHeader);
            if (token == null || !jwtUtils.validateToken(token)) {
                return Result.error(401, "未登录或Token已过期");
            }

            Long userId = jwtUtils.getUserId(token);
            User user = userService.getUserById(userId);
            if (user == null) {
                return Result.error(404, "用户不存在");
            }
            return Result.success(user);
        } catch (Exception e) {
            return Result.error(401, "Token无效");
        }
    }

    @PutMapping("/me")
    @Operation(summary = "更新个人信息", description = "需要Token认证")
    public Result<User> updateProfile(
            @RequestHeader(value = "Authorization", required = false) String authHeader,
            @RequestBody User user
    ) {
        try {
            String token = jwtUtils.extractToken(authHeader);
            if (token == null || !jwtUtils.validateToken(token)) {
                return Result.error(401, "未登录或Token已过期");
            }

            Long userId = jwtUtils.getUserId(token);
            User updated = userService.updateUser(userId, user);
            return Result.success(updated);
        } catch (IllegalArgumentException e) {
            return Result.error(400, e.getMessage());
        }
    }
}
