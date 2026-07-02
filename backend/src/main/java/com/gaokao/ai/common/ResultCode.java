package com.gaokao.ai.common;

import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * 统一返回状态码枚举
 *
 * @author gaokao-ai
 * @since 1.0.0
 */
@Getter
@AllArgsConstructor
public enum ResultCode {

    // ==================== 成功 ====================
    SUCCESS(200, "操作成功"),

    // ==================== 客户端错误 4xx ====================
    BAD_REQUEST(400, "请求参数错误"),
    UNAUTHORIZED(401, "未认证，请先登录"),
    FORBIDDEN(403, "无权限访问"),
    NOT_FOUND(404, "请求资源不存在"),
    METHOD_NOT_ALLOWED(405, "请求方法不允许"),
    REQUEST_TIMEOUT(408, "请求超时"),
    CONFLICT(409, "数据冲突"),
    PARAM_ERROR(422, "参数校验失败"),

    // ==================== 服务端错误 5xx ====================
    INTERNAL_SERVER_ERROR(500, "服务器内部错误"),
    SERVICE_UNAVAILABLE(503, "服务暂不可用"),

    // ==================== 业务错误 1xxx ====================
    USER_NOT_FOUND(1001, "用户不存在"),
    USER_ALREADY_EXISTS(1002, "用户已存在"),
    PASSWORD_ERROR(1003, "密码错误"),
    ACCOUNT_DISABLED(1004, "账号已被禁用"),
    ACCOUNT_LOCKED(1005, "账号已被锁定"),
    TOKEN_EXPIRED(1006, "Token已过期"),
    TOKEN_INVALID(1007, "Token无效"),
    VERIFY_CODE_ERROR(1008, "验证码错误"),
    VERIFY_CODE_EXPIRED(1009, "验证码已过期"),

    // ==================== 数据错误 2xxx ====================
    DATA_NOT_FOUND(2001, "数据不存在"),
    DATA_ALREADY_EXISTS(2002, "数据已存在"),
    DATA_SAVE_FAILED(2003, "数据保存失败"),
    DATA_UPDATE_FAILED(2004, "数据更新失败"),
    DATA_DELETE_FAILED(2005, "数据删除失败"),

    // ==================== 业务模块错误 3xxx ====================
    UNIVERSITY_NOT_FOUND(3001, "院校不存在"),
    MAJOR_NOT_FOUND(3002, "专业不存在"),
    SCORE_NOT_FOUND(3003, "分数信息不存在"),
    VOLUNTEER_PLAN_NOT_FOUND(3004, "志愿方案不存在"),
    VOLUNTEER_PLAN_FULL(3005, "志愿方案已满"),

    // ==================== 第三方服务错误 4xxx ====================
    AI_SERVICE_ERROR(4001, "AI服务调用失败"),
    THIRD_PARTY_ERROR(4002, "第三方服务异常");

    /**
     * 状态码
     */
    private final int code;

    /**
     * 消息
     */
    private final String message;
}
